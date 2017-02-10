#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2017 by the NICOS contributors (see AUTHORS)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Georg Brandl <georg.brandl@frm2.tum.de>
#   Enrico Faulhaber <enrico.faulhaber@frm2.tum.de>
#   Alexander Lenz <alexander.lenz@frm2.tum.de>
#
# *****************************************************************************

"""NICOS Experiment devices."""

import os
import re
import time
from os import path
from textwrap import dedent

from nicos import session, config
from nicos.core import listof, anytype, oneof, \
    none_or, dictof, mailaddress, usermethod, Device, Measurable, Readable, \
    Param, NicosError, ConfigurationError, UsageError, SIMULATION, MASTER, \
    Attach
from nicos.core.params import subdir, nonemptystring, expanded_path
from nicos.core.acquire import DevStatistics
from nicos.utils import ensureDirectory, expandTemplate, disableDirectory, \
    enableDirectory, lazy_property, printTable, pwd, grp, DEFAULT_FILE_MODE, \
    createThread
from nicos.utils.ftp import ftpUpload
from nicos.utils.emails import sendMail
from nicos.utils.loggers import ELogHandler
from nicos.utils.compression import zipFiles
from nicos.commands.basic import run
from nicos.pycompat import string_types, from_maybe_utf8
from nicos.devices.sample import Sample
from nicos._vendor import rtfunicode  # for side effects - pylint: disable=W0611


class Experiment(Device):
    """A special singleton device to represent the experiment.

    This class is normally subclassed for specific instruments to e.g. select
    the data paths according to instrument standards.

    Several parameters configure special behavior:

    * `detlist` and `envlist` are lists of names of the currently selected
      standard detector and sample environment devices, respectively.  The
      Experiment object has `detectors` and `sampleenv` properties that return
      lists of the actual devices.
    * `scripts` is managed by the session and should contain a stack of code of
      user scripts currently executed.

    The experiment singleton is available at runtime as
    `nicos.session.experiment`.
    """

    parameters = {
        'title':          Param('Experiment title', type=str, settable=True,
                                category='experiment'),
        'proposal':       Param('Current proposal number or proposal string',
                                type=str, settable=True, category='experiment'),
        'proptype':       Param('Current proposal type', settable=False,
                                userparam=False,
                                type=oneof('service', 'user', 'other')),
        'propprefix':     Param('Prefix of the proposal if is a number',
                                type=str, settable=True, default='p'),
        'users':          Param('User names and emails for the proposal',
                                type=str, settable=True, category='experiment'),
        'localcontact':   Param('Local contact for current experiment',
                                type=mailaddress, settable=True,
                                category='experiment'),
        'remark':         Param('Current remark about experiment configuration',
                                type=str, settable=True, category='experiment'),
        'dataroot':       Param('Root data path under which all proposal '
                                'specific paths are created', mandatory=True,
                                type=expanded_path),
        'detlist':        Param('List of default detector device names',
                                type=listof(str), settable=True,
                                userparam=False),
        'envlist':        Param('List of default environment device names to '
                                'read at every scan point', type=listof(str),
                                settable=True, userparam=False),
        'elog':           Param('True if the electronic logbook should be '
                                'enabled', type=bool, default=True),
        'scripts':        Param('Currently executed scripts', type=listof(str),
                                settable=True, userparam=False),
        'templates':      Param('Name of the directory with script templates '
                                '(relative to dataroot)', type=str),
        'managerights':   Param('A dict of en/disableDir/FileMode to manage '
                                'access rights of data dirs on proposal change',
                                mandatory=False, settable=False, default={},
                                type=dictof(oneof('owner', 'group',
                                                  'enableOwner',
                                                  'enableGroup',
                                                  'disableOwner',
                                                  'disableGroup',
                                                  'enableDirMode',
                                                  'enableFileMode',
                                                  'disableDirMode',
                                                  'disableFileMode'),
                                            anytype),
                                userparam=False),
        'zipdata':        Param('Whether to zip up experiment data after '
                                'experiment finishes', type=bool, default=True),
        'sendmail':       Param('Whether to send proposal data via email after '
                                'experiment finishes', type=bool,
                                default=False),
        'mailserver':     Param('Mail server name', type=str, settable=True,
                                userparam=False),
        'mailsender':     Param('Mail sender address', settable=True,
                                type=none_or(mailaddress)),
        'mailtemplate':   Param('Mail template file name (in templates)',
                                type=str, default='mailtext.txt'),
        'reporttemplate': Param('File name of experimental report template '
                                '(in templates)',
                                type=str, default='experimental_report.rtf'),
        'serviceexp':     Param('Name of proposal to switch to after user '
                                'experiment', type=nonemptystring,
                                default='service'),
        'servicescript':  Param('Script to run for service time', type=str,
                                default='', settable=True),
        'pausecount':     Param('Reason for pausing the count loop', type=str,
                                settable=True, userparam=False),
        'propinfo':       Param('Dict of info for the current proposal',
                                type=dict, default={}, userparam=False),
        'proposalpath':   Param('Proposal prefix upon creation of experiment',
                                type=str, userparam=False, settable=True),
        'sampledir':      Param('Current sample-specific subdir', type=subdir,
                                default='', userparam=False, settable=True),
        'counterfile':    Param('Name of the file with data counters in '
                                'dataroot and datapath', default='counters',
                                userparam=False, type=subdir),
        'errorbehavior':  Param('Behavior on unhandled errors in commands',
                                type=oneof('abort', 'report'), settable=True,
                                default='report'),
        'lastscan':       Param('Last used value of the scan counter - '
                                'ONLY for display purposes', type=int),
        'lastpoint':      Param('Last used value of the point counter - '
                                'ONLY for display purposes', type=int),
        'samples':        Param('Information about all defined samples',
                                type=dictof(int, dictof(str, anytype)),
                                settable=True, userparam=False),
    }

    attached_devices = {
        'sample': Attach('The device object representing the sample', Sample),
    }

    #
    # hooks: may be overriden in derived classes to enhance functionality
    #

    def proposalpath_of(self, proposal):
        """Proposal path of a given proposal.

        Defaults to ``<dataroot>/<year>/<proposal>``, last component MUST be
        the *proposal*.
        """
        return path.join(self.dataroot, time.strftime('%Y'), proposal)

    @property
    def samplepath(self):
        """Path to current active sample, if used, defaults to proposalpath."""
        if self.sampledir:
            return path.join(self.proposalpath, self.sampledir)
        return self.proposalpath

    @property
    def scriptpath(self):
        """Path to the scripts of the curent experiment/sample."""
        return path.join(self.samplepath, 'scripts')

    @property
    def elogpath(self):
        """Path to the eLogbook of the curent experiment/sample."""
        return path.join(self.samplepath, 'logbook')

    @property
    def datapath(self):
        """Path to the data storage of the curent experiment/sample.

        Here scanfiles and images of image-type detectors will be stored.
        """
        return path.join(self.samplepath, 'data')

    @property
    def extrapaths(self):
        """If derived classes need more automatically created dirs, they can
        be put here.
        """
        return tuple()

    @property
    def allpaths(self):
        """Return a list of all autocreated paths.

        Needed to keep track of directory structure upon proposal change.
        """
        return [self.proposalpath, self.datapath,
                self.scriptpath, self.elogpath] + list(self.extrapaths)

    @property
    def templatepath(self):
        """Paths where all template files are stored."""
        return [path.abspath(path.join(self.dataroot, self.templates))] + \
            [path.join(config.custom_path, p.strip(), 'template')
             for p in config.setup_subdirs.split(',')]

    @property
    def proposalsymlink(self):
        """Dataroot based location of 'current' experiment symlink to maintain,
        or empty string.
        """
        return path.join(self.dataroot, 'current')

    @property
    def customproposalsymlink(self):
        """Path of a custom proposal symlink or empty string.
        If a path was specified, the symlink will be created automatically.
        """
        return ''

    @property
    def samplesymlink(self):
        """Dataroot based location of 'current' sample symlink to maintain,
        or empty string.
        """
        return self.proposalsymlink if self.sampledir else ''

    @lazy_property
    def skiptemplates(self):
        """List of template filenames which are to be ignored upon creating
        a new experiment.
        """
        return []

    def getProposalType(self, proposal):
        """Determine proposaltype of a given proposalstring."""
        if proposal in ('template', 'current'):
            raise UsageError(self, 'The proposal names "template" and "current"'
                             ' are reserved and cannot be used')
        # check for defines service 'proposal'
        if proposal == self.serviceexp:
            return 'service'
        # all proposals starting with the define prefix are user-type,
        # all others are service
        if self.propprefix:
            if proposal.startswith(self.propprefix):
                return 'user'
            return 'service'
        # if we have no prefix, all number-like proposals >0 are usertype,
        # else service
        try:
            if int(proposal) == 0:
                return 'service'
            return 'user'
        except ValueError:
            return 'service'

    def _newPropertiesHook(self, proposal, kwds):
        """Hook for querying a database for proposal related stuff

        Should return an updated kwds dictionary.
        """
        return kwds

    #
    # don't override any method defined below in derived classes!
    #

    #
    # other path handling stuff
    #

    def doWriteProposalpath(self, newproposalpath):
        # handle current symlink
        self._set_symlink(self.proposalsymlink, path.relpath(
            newproposalpath, path.dirname(self.proposalsymlink)))
        # HACK: we need the getters to provide the right values....
        self._setROParam('proposalpath', newproposalpath)
        # create all needed subdirs...
        for _dir in self.allpaths:
            ensureDirectory(_dir, **self.managerights)

        # tell elog
        if self.elog:
            instname = session._instrument and session.instrument.instrument or ''
            session.elogEvent('directory', (newproposalpath, instname,
                                            path.basename(newproposalpath)))

    def doWriteSampledir(self, newsampledir):
        # handle current symlink
        self._set_symlink(self.samplesymlink,
                          path.join(self.proposalpath, newsampledir))

        # HACK: we need the getters to provide the right values....
        self._setROParam('sampledir', newsampledir)
        # create all needed subdirs...
        for _dir in self.allpaths:
            ensureDirectory(_dir, **self.managerights)

    def _set_symlink(self, location, target):
        if not target or not location:
            return
        if hasattr(os, 'symlink'):
            if path.islink(location):
                self.log.debug('removing symlink %s', location)
                os.unlink(location)
            ensureDirectory(path.join(path.dirname(location), target),
                            **self.managerights)
            self.log.debug('setting symlink %s to %s', location, target)
            os.symlink(target, location)

    #
    # datafile stuff
    #

    def getDataDir(self, *subdirs):
        """Returns the current path for the data directory in subdir
        structure subdirs.

        Returned directory is created if it did not exist.
        """
        dirname = path.abspath(path.join(self.datapath, *subdirs))
        if self._mode != SIMULATION:
            ensureDirectory(dirname, **self.managerights)
        return dirname

    def getDataFilename(self, filename, *subdirs):
        """Returns the current path for given filename in subdir structure
        subdirs.

        If filename is an absolute path, ignore the subdirs and start at
        dataroot returned filename is usable 'as-is', i.e. the required
        directory structure is already created.
        """
        if path.isabs(filename):
            fullname = path.join(self.dataroot, filename[1:])
            dirname = path.dirname(fullname)
            if self._mode != SIMULATION:
                ensureDirectory(dirname, **self.managerights)
        else:
            fullname = path.join(self.getDataDir(*subdirs), filename)
        return fullname

    #
    # NICOS interface
    #

    def doInit(self, mode):
        # check that service proposal is actually resolved as service
        if self.propprefix:
            try:
                int(self.serviceexp)
            except ValueError:
                pass
            else:
                raise ConfigurationError(self, 'the serviceexp parameter '
                                         'must be set to %r, not just %r'
                                         % (self.propprefix + self.serviceexp,
                                            self.serviceexp))

        instname = session._instrument and session.instrument.instrument or ''
        if self._attached_sample.name != 'Sample':
            raise ConfigurationError(self, 'the sample device must now be '
                                     'named "Sample", please fix your system '
                                     'setup')
        if self.elog and mode != SIMULATION:
            if not self.proposalpath:
                self.log.warning('Proposalpath was not set, initiating a '
                                 'service experiment.')
                self._setROParam('proposalpath',
                                 self.proposalpath_of(self.serviceexp))
                self._setROParam('proptype', 'service')
            ensureDirectory(path.join(self.proposalpath, 'logbook'))
            session.elogEvent('directory', (self.proposalpath,
                                            instname, self.proposal))
            self._eloghandler = ELogHandler()
            # only enable in master mode, see below
            self._eloghandler.disabled = session.mode != MASTER
            session.addLogHandler(self._eloghandler)
        if self.templates == '':
            self._setROParam('templates',
                             path.abspath(path.join(config.nicos_root,
                                                    'template')))

    def doUpdateManagerights(self, mrinfo):
        """Check the managerights dict into values used later."""
        if pwd and self._mode != SIMULATION:
            for key, lookup in [('owner', pwd.getpwnam),
                                ('enableOwner', pwd.getpwnam),
                                ('disableOwner', pwd.getpwnam),
                                ('group', grp.getgrnam),
                                ('enableGroup', grp.getgrnam),
                                ('disableGroup', grp.getgrnam)]:
                value = mrinfo.get(key)
                if isinstance(value, string_types):
                    try:
                        lookup(value)
                    except Exception as e:
                        raise ConfigurationError(
                            self, 'managerights: illegal value for key '
                            '%r: %r (%s)' % (key, value, e), exc=1)
        for key in ['enableDirMode', 'enableFileMode',
                    'disableDirMode', 'disableFileMode']:
            value = mrinfo.get(key)
            if value is not None and not isinstance(value, int):
                raise ConfigurationError(
                    self, 'managerights: illegal value for key '
                    '%r: not an integer' % key, exc=1)

    #
    # Experiment handling: New&Finish
    #

    @property
    def mustFinish(self):
        """Return True if the current experiment must be finished before
        starting a new one.
        """
        return self.proptype == 'user'

    @usermethod
    def new(self, proposal, title=None, localcontact=None, user=None, **kwds):
        """Called by `.NewExperiment`."""
        if self._mode == SIMULATION:
            raise UsageError('Simulating switching experiments is not '
                             'supported!')

        if localcontact:
            try:
                mailaddress(localcontact)
            except ValueError:
                raise ConfigurationError('localcontact is not a valid '
                                         'email address')

        try:
            # if proposal can be converted to a number, use the canonical form
            # and prepend prefix
            proposal = '%s%d' % (self.propprefix, int(proposal))
        except ValueError:
            pass
        self.log.debug('new proposal real name is %s', proposal)

        if not proposal:
            raise UsageError('Proposal name/number cannot be empty')

        # check proposal type (can raise)
        proptype = self.getProposalType(proposal)
        self.log.debug('new proposal type is %s', proptype)

        # check if we should finish the experiment first
        if proptype == 'user' and self.mustFinish:
            self.log.error('cannot switch directly to new user experiment, '
                           'please use "FinishExperiment" first')
            return

        # allow instruments to override (e.g. from proposal DB)
        if title:
            kwds['title'] = title
        if user:
            kwds['user'] = user
        if localcontact:
            kwds['localcontact'] = localcontact
        kwds['proposal'] = proposal

        # need to enable before checking templated files...
        # if next proposal is of type 'user'
        if self.managerights and proptype == 'user':
            self.log.debug('managerights: %s', self.managerights)
            self.log.debug('enableDirectory: %s',
                           self.proposalpath_of(proposal))
            enableDirectory(self.proposalpath_of(proposal),
                            logger=self.log, **self.managerights)

        if proptype != 'service':
            if self.templates:
                try:
                    self.checkTemplates(proposal, kwds)  # may raise
                except Exception:
                    # restore previous state completely, thus disabling
                    if self.managerights:
                        disableDirectory(self.proposalpath_of(proposal),
                                         logger=self.log, **self.managerights)
                    raise

        # reset all experiment dependent parameters and values to defaults
        self.remark = ''
        try:
            self.sample.clear()
        except Exception:
            self.sample.log.warning('could not clear sample info', exc=1)
        self.samples = {}
        self.envlist = []
        for notifier in session.notifiers:
            try:
                notifier.reset()
            except Exception:
                notifier.log.warning('could not clear notifier info', exc=1)
        try:
            session.data.reset_all()
        except Exception:
            self.log.warning('could not clear data manager info', exc=1)

        # set new experiment properties given by caller
        self._setROParam('proptype', proptype)
        kwds = self._newPropertiesHook(proposal, kwds)
        self._setROParam('propinfo', kwds)
        self.title = kwds.get('title', '')
        self.users = kwds.get('user', '')
        default_local = session._instrument and session.instrument.responsible or ''
        self.localcontact = kwds.get('localcontact', default_local)

        # assignment to proposalpath/sampledir adjusts possible symlinks
        self.proposal = proposal
        # change proposalpath to new value
        self.proposalpath = self.proposalpath_of(proposal)
        # newSample also (re-)creates all needed dirs
        self.sample.new({'name': kwds.get('sample', '')})

        # debug output
        self.log.info('experiment directory is now %s', self.proposalpath)
        self.log.info('script directory is now %s', self.scriptpath)
        self.log.info('data directory is now %s', self.datapath)

        # notify logbook
        session.elogEvent('newexperiment', (proposal, title))
        session.elogEvent('setup', list(session.explicit_setups))

        # send 'experiment' change event before the last hooks
        # maybe better after the last hook?
        session.experimentCallback(self.proposal, proptype)

        # expand templates
        if proptype != 'service':
            if self.templates:
                kwds['proposal'] = self.proposal
                self.handleTemplates(proposal, kwds)
            self.log.info('New experiment %s started', proposal)
        else:
            if self.servicescript:
                run(self.servicescript)
            else:
                self.log.debug('not running service script, none configured')
            self.log.info('Maintenance time started')

        self._createCustomProposalSymlink()

    @usermethod
    def finish(self, *args, **kwds):
        """Called by `.FinishExperiment`. Returns the `FinishExperiment`
        Thread if applicable otherwise `None`.

        Default implementation is to finish the experiment, which means to save
        the data, set the access rights, zipping data, sending email to the
        user, and to call :meth:`doFinish` if present.

        .. method:: doFinish()

           This method is called as part of finish() before the data will be
           packed and/or send via email.
        """
        thd = None

        # update metadata
        propinfo = dict(self.propinfo)
        propinfo.setdefault('from_time', time.time())
        propinfo['to_time'] = time.time()
        self._setROParam('propinfo', propinfo)

        # zip up the experiment data if wanted
        if self.proptype == 'user':
            try:
                self._generateExpReport(**kwds)
            except Exception:
                self.log.warning('could not generate experimental report',
                                 exc=1)

            if self._mode != SIMULATION:
                if hasattr(self, 'doFinish'):
                    self.doFinish()
                pzip = None
                receivers = None
                if self.sendmail:
                    if args:
                        receivers = args
                    else:
                        receivers = self.propinfo.get('user_email', receivers)
                    receivers = kwds.get('receivers', kwds.get('email',
                                                               receivers))
                    if isinstance(receivers, string_types):  # convert to list
                        receivers = [receivers]
                if self.zipdata or self.sendmail:
                    pzip = path.join(self.proposalpath, '..', self.proposal +
                                     '.zip')
                try:
                    stats = self._statistics()
                except Exception:
                    self.log.exception('could not gather experiment statistics')
                    stats = {}
                stats.update(propinfo)
                # start separate thread for zipping and disabling old proposal
                self.log.debug('Start separate thread for zipping and '
                               'disabling proposal.')
                thd = createThread('FinishExperiment',
                                   target=self._finish,
                                   args=(pzip, self.proposalpath,
                                         self.proposal, self.proptype, stats,
                                         receivers),
                                   daemon=False)
                # wait up to 5 seconds
                thd.join(5)
                if thd.isAlive():
                    self.log.info('continuing finishing of proposal %s in '
                                  'background', self.proposal)
                else:
                    thd = None

        # switch to service experiment (will hide old data if configured)
        self.new(self.serviceexp, localcontact=self.localcontact)
        return thd

    #
    # template stuff
    #
    def getTemplate(self, tmplname):
        """returns the content of the requested template"""
        for tmpldir in self.templatepath:
            if path.isfile(path.join(tmpldir, tmplname)):
                with open(path.join(tmpldir, tmplname), 'r') as f:
                    return f.read()
        raise IOError('no such template found')

    def iterTemplates(self, only_dot_template=True):
        """iterator of all templates (and their content)..."""
        for tmpldir in self.templatepath[::-1]:  # reversed to keep priority
            if not path.isdir(tmpldir):
                continue
            filelist = os.listdir(tmpldir)
            for fn in filelist:
                if fn == 'README':
                    continue
                if self.mailtemplate and fn.startswith(self.mailtemplate):
                    continue
                if self.reporttemplate and fn.startswith(self.reporttemplate):
                    continue
                if fn in self.skiptemplates:
                    continue
                if only_dot_template and not fn.endswith('.template'):
                    continue
                yield (fn, self.getTemplate(fn))

    def checkTemplates(self, proposal, kwargs):
        """try to fill in all templates to see if some keywords are missing"""
        if self._mode == SIMULATION:
            return  # dont touch fs if in simulation!
        allmissing = []
        alldefaulted = []
        for fn, content in self.iterTemplates(only_dot_template=True):
            newfn = fn[:-9]  # strip ".template" from the name
            newfn, _, _ = expandTemplate(newfn, kwargs)

            finalname = path.join(self.proposalpath_of(proposal), self.sampledir,
                                  'scripts', newfn)

            if path.isfile(finalname):
                self.log.debug('skipping already translated file %r', newfn)
                continue

            self.log.debug('checking template %r', fn)
            _, defaulted, missing = expandTemplate(content, kwargs)
            if missing:
                allmissing.extend(missing)
            if defaulted:
                alldefaulted.extend(defaulted)

        if not allmissing and not alldefaulted:
            return

        # format nicely
        headers = ['missing keyword', 'defaultvalue', 'description']
        errkwds = [item['key'] for item in allmissing]

        items = [[item['key'], item['default'] or '', item['description'] or '']
                 for item in allmissing + alldefaulted]

        def myprintfunc(what):
            if what.strip().split(' ')[0] in errkwds:
                self.log.error(what)
            else:
                self.log.warning(what)

        printTable(headers, items, myprintfunc)
        if allmissing:
            raise NicosError('some keywords are missing, please provide them as '
                             'keyword arguments to `NewExperiment`')

    def handleTemplates(self, proposal, kwargs):
        if self._mode == SIMULATION:
            return  # dont touch fs if in simulation!
        for fn, content in self.iterTemplates(only_dot_template=False):
            istemplate = fn.endswith('.template')
            newfn = fn
            if istemplate:
                newfn = fn[:-9]  # remove '.template' at end
                newfn, _, _ = expandTemplate(newfn, kwargs)
                self.log.debug('%s -> %s', fn, newfn)
            else:
                self.log.debug('%s is no template, just copy it.', fn)

            finalname = path.join(self.scriptpath, newfn)
            if path.isfile(finalname):
                self.log.info('not overwriting existing file %s', newfn)
                continue

            if istemplate:
                self.log.debug('templating file content of %r', fn)
                try:
                    content, _, _ = expandTemplate(content, kwargs)
                except Exception:
                    self.log.warning('could not translate template file %s',
                                     fn, exc=1)
            # save result
            with open(finalname, 'w') as fp:
                fp.write(content)
            os.chmod(finalname, self.managerights.get('enableFileMode',
                                                      DEFAULT_FILE_MODE))

    #
    # various helpers
    #
    def _zip(self, pzip, proposalpath):
        """Zip all files in `proposalpath` folder into `pzip` (.zip) file."""
        self.log.info('zipping experiment data, please wait...')
        zipname = zipFiles(pzip, proposalpath)
        self.log.info('zipping done: stored as %s', zipname)
        return zipname

    def _upload(self, pzip):
        """Uploads the file `pzip` and returns additional mailbody content."""
        url = ftpUpload(pzip, logger=self.log)
        mailbody = dedent("""
        =====
        Due to size limitations, the attachment has been copied to a temporary
        storage where it will be kept for four weeks.

        Please download the data from:
        %s
        within the next four weeks.
        """) % url
        return mailbody

    def _mail(self, proposal, stats, receivers, zipname,
              maxAttachmentSize=10000000):
        """Send a mail with the experiment data"""

        if self._mode == SIMULATION:
            return  # dont touch fs if in simulation!
        # check parameters
        if not self.mailserver:
            raise NicosError('%s.mailserver parameter is not set' % self)
        if not self.mailsender:
            raise NicosError('%s.mailsender parameter is not set' % self)
        for email in receivers:
            try:
                mailaddress(email)
            except ValueError:
                raise NicosError('need valid email address(es)')

        # read and translate mailbody template
        self.log.debug('looking for template in %r', self.templatepath)
        try:
            mailbody = self.getTemplate(self.mailtemplate)
        except IOError:
            self.log.warning('reading mail template %s failed',
                             self.mailtemplate, exc=1)
            mailbody = 'See data in attachment.'

        mailbody, _, _ = expandTemplate(mailbody, stats)

        instname = session._instrument and session.instrument.instrument or '?'
        topic = 'Your recent experiment %s on %s from %s to %s' % \
                (proposal, instname, stats.get('from_date'), stats.get('to_date'))

        self.log.info('Sending data files via eMail to %s', receivers)
        if os.stat(zipname).st_size < maxAttachmentSize:
            # small enough -> send directly
            sendMail(self.mailserver, receivers, self.mailsender, topic, mailbody,
                     [zipname], 1 if self.loglevel == 'debug' else 0)
        else:
            # not small enough -> upload and send link
            self.log.info('Zipfile is too big to send via email and will be '
                          'uploaded to a temporary storage for download.')
            mailbody += self._upload(zipname)
            sendMail(self.mailserver, receivers, self.mailsender, topic, mailbody,
                     [], 1 if self.loglevel == 'debug' else 0)

    def _finish(self, pzip, proposalpath, proposal, proptype, stats, receivers):
        if pzip:
            try:
                pzipfile = self._zip(pzip, proposalpath)
            except Exception:
                self.log.warning('could not zip up experiment data', exc=1)
            else:
                if receivers:
                    try:
                        self._mail(proposal, stats, receivers, pzipfile)
                    except Exception:
                        self.log.warning('could not send the data via email',
                                         exc=1)
                # "hide" compressed file by moving it into the
                # proposal directory
                self.log.info('moving compressed file to %s', proposalpath)
                try:
                    os.rename(pzipfile, path.join(proposalpath,
                                                  path.basename(pzipfile)))
                except Exception:
                    self.log.warning('moving compressed file into proposal '
                                     'dir failed', exc=1)
                    # at least withdraw the access rights
                    os.chmod(pzipfile,
                             self.managerights.get('disableFileMode',
                                                   0o400))
        # remove access rights to old proposal if wanted
        if self.managerights and proptype == 'user':
            disableDirectory(proposalpath, logger=self.log,
                             **self.managerights)
            self.log.debug('disabled directory %s'
                           % proposalpath)

    def _setMode(self, mode):
        if self.elog:
            self._eloghandler.disabled = mode != MASTER
        Device._setMode(self, mode)

    def _createCustomProposalSymlink(self):
        if not self.customproposalsymlink:
            return

        # create symlink
        ensureDirectory(path.dirname(self.customproposalsymlink))
        try:
            self.log.debug('create custom proposal symlink %r -> %r',
                           self.customproposalsymlink, self.proposalpath)
            os.symlink(os.path.basename(self.proposalpath),
                       self.customproposalsymlink)
        except OSError:
            self.log.warning('creation of custom proposal symlink failed, '
                             'already existing?')

    @usermethod
    def addUser(self, name, email=None, affiliation=None):
        """Called by `.AddUser`."""
        if email:
            user = '%s <%s>' % (name, email)
        else:
            user = name
        if affiliation is not None:
            user += ' (' + affiliation + ')'
        if not self.users:
            self.users = user
        else:
            self.users = self.users + ', ' + user
        self.log.info('User "%s" added', user)

    def newSample(self, parameters):
        """Hook called by the sample object to notify of new sample name.

        By default, (re-) creates all needed (sub)dirs that might change
        depending on the sample name/number.
        """
        for _dir in self.allpaths:
            ensureDirectory(_dir, **self.managerights)

    def _statistics(self):
        """Return some statistics about the current experiment in a dict.
        May need improvements.
        """

        # get start of proposal from cache history
        hist, d = [], 7
        # default to 'exp not yet started times'
        to_time = from_time = time.time()
        while not hist and d < 60:
            hist = self.history('proposal', -d * 24)
            d += 7
        if hist:
            from_time = hist[-1][0]
        from_date = time.strftime('%a, %d. %b %Y', time.localtime(from_time))
        to_date = time.strftime('%a, %d. %b %Y', time.localtime(to_time))

        # check number of (scan) data files
        # maybe this should be live collected in propinfo and not
        # after the experiment by scanning the filesystem.
        numscans = 0
        firstscan = 99999999
        lastscan = 0
        scanfilepattern = re.compile(r'%s_(\d{8})\.dat$' % self.proposal)
        for fn in os.listdir(self.datapath):
            m = scanfilepattern.match(fn)
            if m:
                firstscan = min(firstscan, int(m.group(1)))
                lastscan = max(lastscan, int(m.group(1)))
                numscans += 1

        d = {
            'proposal':     self.proposal,
            'from_date':    from_date,
            'to_date':      to_date,
            'firstfile':    '%08d' % firstscan,
            'lastfile':     '%08d' % lastscan,
            'numscans':     str(numscans),
            'title':        self.title,
            'users':        self.users,
            'samplename':   self.sample.samplename,
            'localcontact': self.localcontact,
            'instrument':   session._instrument and session.instrument.instrument or '',
        }
        d.update(self.propinfo)
        return d

    def _generateExpReport(self, **kwds):
        if self._mode == SIMULATION:
            return  # dont touch fs if in simulation!
        if not self.reporttemplate:
            return
        # read and translate ExpReport template
        self.log.debug('looking for template in %r', self.templatepath)
        try:
            data = self.getTemplate(self.reporttemplate)
        except IOError:
            self.log.warning('reading experimental report template %s failed, '
                             'please fetch a copy from the User Office',
                             self.reporttemplate)
            return  # nothing to do about it.

        # prepare template....
        # can not do this directly in rtf as {} have special meaning....
        # KEEP IN SYNC WHEN CHANGING THE TEMPLATE!
        # reminder: format is {{key:default#description}},
        # always specify default here !
        #
        # first clean up template
        data = data.replace('\\par Please replace the place holder in the upper'
                            ' part (brackets <>) by the appropriate values.', '')
        data = data.replace('\\par Description', '\\par\n\\par '
                            'Please check all pre-filled values carefully! '
                            'They were partially read from the proposal and '
                            'might need correction.\n'
                            '\\par\n'
                            '\\par Description')
        # replace placeholders with templating markup
        data = data.replace('<your title as mentioned in the submission form>',
                            '"{{title:The title of your proposed experiment}}"')
        data = data.replace('<proposal No.>', 'Proposal {{proposal:0815}}')
        data = data.replace('<your name> ', '{{users:A. Guy, A. N. Otherone}}')
        data = data.replace('<coauthor, same affilation> ', 'and coworkers')
        data = data.replace('<other coauthor> ', 'S. T. Ranger')
        data = data.replace('<your affiliation>, }',
                            '{{affiliation:affiliation of main proposer and '
                            'coworkers}}, }\n\\par ')
        data = data.replace('<other affiliation>', 'affiliation of coproposers '
                            'other than 1')
        data = data.replace('<Instrument used>',
                            '{{instrument:<The Instrument used>}}')
        data = data.replace('<date of experiment>', '{{from_date:01.01.1970}} '
                            '- {{to_date:12.03.2038}}')
        data = data.replace('<local contact>', '{{localcontact:L. Contact '
                            '<l.contact@frm2.tum.de>}}')

        # collect info
        stats = self._statistics()
        stats.update(self.propinfo)
        stats.update(kwds)
        # encode all text that may be Unicode into RTF \u escapes
        for key in stats:
            if isinstance(stats[key], string_types):
                stats[key] = from_maybe_utf8(stats[key]).encode('rtfunicode')

        # template data
        newcontent, _, _ = expandTemplate(data, stats)
        newfn, _, _ = expandTemplate(self.reporttemplate, stats)

        with open(path.join(self.proposalpath, newfn), 'w') as fp:
            fp.write(newcontent)
        self.log.info('An experimental report template was created at %r for '
                      'your convenience.', path.join(self.proposalpath, newfn))

    def doWriteRemark(self, remark):
        if remark:
            session.elogEvent('remark', remark)

    @property
    def sample(self):
        return self._attached_sample

    #
    # Detectorlist
    #
    @property
    def detectors(self):
        if self._detlist is not None:
            return self._detlist[:]
        detlist = []
        all_created = True
        for detname in self.detlist:
            try:
                det = session.getDevice(detname, source=self)
            except Exception:
                self.log.warning('could not create %r detector device',
                                 detname, exc=1)
                all_created = False
            else:
                if not isinstance(det, Measurable):
                    self.log.warning('cannot use device %r as a '
                                     'detector: it is not a Measurable', det)
                    all_created = False
                else:
                    detlist.append(det)
        if all_created:
            self._detlist = detlist
        return detlist[:]

    def setDetectors(self, detectors):
        dlist = []
        for det in detectors:
            if isinstance(det, Device):
                det = det.name
            if det not in dlist:
                dlist.append(det)
        self.detlist = dlist
        # try to create them right now
        self.detectors  # pylint: disable=W0104
        session.elogEvent('detectors', dlist)

    def doUpdateDetlist(self, detectors):
        self._detlist = None  # clear list of actual devices

    #
    # Environment devicelist
    #
    @property
    def sampleenv(self):
        if self._envlist is not None:
            return self._envlist[:]
        devlist = []
        all_created = True
        for devname in self.envlist:
            try:
                if ':' in devname:
                    devname, stat = devname.split(':')
                    dev = session.getDevice(devname, source=self)
                    dev = DevStatistics.subclasses[stat](dev)
                else:
                    dev = session.getDevice(devname, source=self)
            except Exception:
                self.log.warning('could not create %r environment device',
                                 devname, exc=1)
                all_created = False
            else:
                if not isinstance(dev, (Readable, DevStatistics)):
                    self.log.warning('cannot use device %r as '
                                     'environment: it is not a Readable', dev)
                    all_created = False
                else:
                    devlist.append(dev)
        if all_created:
            self._envlist = devlist
        return devlist[:]

    def setEnvironment(self, devices):
        dlist = []
        for dev in devices:
            if isinstance(dev, Device):
                dev = dev.name
            elif isinstance(dev, DevStatistics):
                dev = str(dev)
            if dev not in dlist:
                dlist.append(dev)
        self.envlist = dlist
        # try to create them right now
        self.sampleenv  # pylint: disable=W0104
        session.elogEvent('environment', dlist)

    def doUpdateEnvlist(self, devices):
        self._envlist = None  # clear list of actual devices

    def _scrubDetEnvLists(self):
        """Remove devices from detlist and envlist that don't exist anymore
        after a setup change.
        """
        newlist = []
        for devname in self.detlist:
            if devname not in session.configured_devices:
                self.log.warning('removing device %r from detector list, it '
                                 'does not exist in any loaded setup', devname)
            else:
                newlist.append(devname)
        self.detlist = newlist
        newlist = []
        for devname in self.envlist:
            if ':' in devname:
                devname = devname.split(':')[0]
            if devname not in session.configured_devices:
                self.log.warning('removing device %r from environment, it '
                                 'does not exist in any loaded setup', devname)
            else:
                newlist.append(devname)
        self.envlist = newlist


class ImagingExperiment(Experiment):
    """General experiment device for all imaging instruments.

    This specific experiment takes care about some common data
    (dark images, open beam images) and behaviour for imaging instruments.
    """

    parameters = {
        # for display purposes....
        'lastdarkimage':     Param('Last dark image', type=str, settable=False,
                                   default='', category='general'),
        'lastopenbeamimage': Param('Last Open Beam image', type=str,
                                   settable=False, default='',
                                   category='general'),
    }

    @property
    def darkimagedir(self):
        return path.join(self.datapath, 'di')

    @property
    def openbeamdir(self):
        return path.join(self.datapath, 'ob')

    @property
    def photodir(self):
        return path.join(self.proposalpath, 'photos')

    @property
    def extrapaths(self):
        paths = set(Experiment.extrapaths.fget(self))

        paths.add(self.darkimagedir)
        paths.add(self.openbeamdir)
        paths.add(self.photodir)

        return tuple(paths)

    def _clearImgPaths(self):
        # clear state info
        self._setROParam('lastdarkimage', '')
        self._setROParam('lastopenbeamimage', '')

    def new(self, *args, **kwargs):
        Experiment.new(self, *args, **kwargs)
        self._clearImgPaths()


class SXtalExperiment(Experiment):
    parameters = {
        'centeredrefs': Param('List of centered reflections',
                              type=list, settable=True,
                              category='experiment'),
        'checkrefs':    Param('List of reflections to re-check regularly',
                              type=list, settable=True,
                              category='experiment'),
    }
