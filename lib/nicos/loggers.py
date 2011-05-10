#  -*- coding: utf-8 -*-
# *****************************************************************************
# Module:
#   $Id$
#
# Author:
#   Georg Brandl <georg.brandl@frm2.tum.de>
#
# NICOS-NG, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2011 by the NICOS-NG contributors (see AUTHORS)
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
# *****************************************************************************

"""
Logging utilities specific to NICOS.
"""

__author__  = "$Author$"
__date__    = "$Date$"
__version__ = "$Revision$"

import os
import sys
import time
import codecs
import traceback
from logging import setLoggerClass, addLevelName, Logger, \
     Formatter, FileHandler, StreamHandler, DEBUG, INFO, WARNING, ERROR
from logging.handlers import BaseRotatingHandler

from nicos.errors import NicosError
from nicos.utils import colorize, formatExtendedTraceback


LOGFMT = '%(name)-10s : %(asctime)s : %(levelname)-7s : %(message)s'
USERLOGFMT = '%(asctime)s | %(name)-10s %(levelname)-7s : %(message)s'
DATEFMT = '%H:%M:%S'
LONGDATEFMT = '%Y-%m-%d %H:%M:%S'
DATESTAMP_FMT = '%Y-%m-%d'
SECONDS_PER_DAY = 60 * 60 * 24

ACTION = INFO + 1
OUTPUT = INFO + 5
INPUT  = INFO + 6

loglevels = {'debug': DEBUG, 'info': INFO, 'action': ACTION, 'warning': WARNING,
             'error': ERROR, 'input': INPUT, 'output': OUTPUT}


class NicosLogger(Logger):
    """
    Nicos logger class with special method behavior.
    """

    def __init__(self, name, *args):
        Logger.__init__(self, name, *args)
        self.globalprefix = ''

    def exception(self, *msgs, **kwds):
        kwds['exc'] = True
        self.error(*msgs, **kwds)

    def _process(self, msgs, kwds):
        # standard logging keyword arg
        exc_info = kwds.pop('exc_info', None)
        # nicos easy keyword arg
        exc = kwds.pop('exc', None)
        if not exc_info:
            if isinstance(exc, Exception):
                exc_info = (type(exc), exc, None)
            elif exc:
                exc_info = sys.exc_info()
        if exc_info:
            if msgs:
                msgs += ('-',)
            if issubclass(exc_info[0], NicosError):
                msgs += (exc_info[0].category + ' -', exc_info[1],)
            else:
                msgs += (exc_info[0].__name__ + ' -', exc_info[1],)
        msg = ' '.join(map(str, msgs))
        return msg, exc_info

    def error(self, *msgs, **kwds):
        msg, exc_info = self._process(msgs, kwds)
        Logger.error(self, msg, exc_info=exc_info, extra=kwds)

    def warning(self, *msgs, **kwds):
        msg, exc_info = self._process(msgs, kwds)
        Logger.warning(self, msg, exc_info=exc_info, extra=kwds)

    def info(self, *msgs, **kwds):
        msg, exc_info = self._process(msgs, kwds)
        Logger.info(self, msg, exc_info=exc_info, extra=kwds)

    def debug(self, *msgs, **kwds):
        msg, exc_info = self._process(msgs, kwds)
        Logger.debug(self, msg, exc_info=exc_info, extra=kwds)

    def action(self, msg):
        Logger.log(self, ACTION, msg)

    def _log(self, level, msg, args, exc_info=None, extra=None):
        record = self.makeRecord(self.name, level, self.globalprefix,
                                 0, msg, args, exc_info, '', extra)
        self.handle(record)



class NicosConsoleFormatter(Formatter):
    """
    A lightweight formatter for the interactive console, with optional
    colored output.
    """

    def __init__(self, fmt=None, datefmt=None, colorize=None):
        Formatter.__init__(self, fmt, datefmt)
        if colorize:
            self.colorize = colorize
        else:
            self.colorize = lambda c, s: s

    def formatException(self, exc_info):
        return traceback.format_exception_only(*exc_info[0:2])[-1]

    def formatTime(self, record, datefmt=None):
        return time.strftime(datefmt or DATEFMT,
                             self.converter(record.created))

    def format(self, record):
        levelno = record.levelno
        datefmt = self.colorize('lightgray', '[%(asctime)s] ')
        if record.name == 'nicos':
            namefmt = ''
        else:
            namefmt = '%(name)-10s: '
        if levelno == ACTION:
            # special behvaior for ACTION messages: use them as terminal title
            fmtstr = '\033]0;%s%%(message)s\007' % namefmt
        else:
            if levelno <= DEBUG:
                fmtstr = self.colorize('darkgray', '%s%%(message)s' % namefmt)
            elif levelno <= OUTPUT:
                fmtstr = '%s%%(message)s' % namefmt
            elif levelno == INPUT:
                # do not display input again
                return ''
            elif levelno <= WARNING:
                fmtstr = self.colorize('fuchsia', '%s%%(levelname)s: %%(message)s'
                                       % namefmt)
            else:
                fmtstr = self.colorize('red', '%s%%(levelname)s: %%(message)s'
                                       % namefmt)
            fmtstr = '%(filename)s' + datefmt + fmtstr
            if not getattr(record, 'nonl', False):
                fmtstr += '\n'
        record.message = record.getMessage()
        record.asctime = self.formatTime(record, self.datefmt)
        s = fmtstr % record.__dict__
        # never output more exception info -- the exception message is already
        # part of the log message because of our special logger behavior
        #if record.exc_info:
        #    # *not* caching exception text on the record, since it's
        #    # only a short version
        #    s += self.formatException(record.exc_info)
        return s


class ColoredConsoleHandler(StreamHandler):
    """
    A handler class that writes colorized records to standard output.
    """

    def __init__(self):
        StreamHandler.__init__(self, sys.stdout)
        self.setFormatter(NicosConsoleFormatter(
            datefmt=DATEFMT, colorize=colorize))

    def emit(self, record):
        msg = self.format(record)
        self.stream.write(msg)
        self.stream.flush()


class NicosLogfileFormatter(Formatter):
    """
    The standard Formatter does not support milliseconds with an explicit
    datestamp format.  It also doesn't show the full traceback for exceptions.
    """

    extended_traceback = True

    def formatException(self, ei):
        if self.extended_traceback:
            s = formatExtendedTraceback(*ei)
        else:
            s = ''.join(traceback.format_exception(ei[0], ei[1], ei[2],
                                                   sys.maxint))
            if s.endswith('\n'):
                s = s[:-1]
        return s

    def formatTime(self, record, datefmt=None):
        res = time.strftime(DATEFMT, self.converter(record.created))
        res += ',%03d' % record.msecs
        return res


class NicosLogfileHandler(BaseRotatingHandler):
    """
    Logs to log files with a date stamp appended, and rollover on midnight.
    """

    def __init__(self, directory, filenameprefix='nicos', dayfmt=DATESTAMP_FMT):
        if not os.path.isdir(directory):
            os.makedirs(directory)
        self._filenameprefix = filenameprefix
        self._pathnameprefix = os.path.join(directory, filenameprefix)
        self._dayfmt = dayfmt
        # today's logfile name
        basefn = self._pathnameprefix + '-' + time.strftime(dayfmt) + '.log'
        BaseRotatingHandler.__init__(self, basefn, 'a')
        # determine time of first midnight from now on
        t = time.localtime()
        self.rollover_at = time.mktime((t[0], t[1], t[2], 0, 0, 0,
                                        t[6], t[7], t[8])) + SECONDS_PER_DAY
        self.setFormatter(NicosLogfileFormatter(LOGFMT, DATEFMT))

    def emit(self, record):
        if record.levelno == ACTION:
            # do not write ACTIONs to logfiles, they're only informative
            return
        try:
            t = int(time.time())
            if t >= self.rollover_at:
                self.doRollover()
            FileHandler.emit(self, record)
        except Exception:
            self.handleError(record)

    def doRollover(self):
        self.stream.close()
        self.baseFilename = self._pathnameprefix + '-' + \
                            time.strftime(self._dayfmt) + '.log'
        if hasattr(self, 'encoding') and self.encoding:
            self.stream = codecs.open(self.baseFilename, 'w', self.encoding)
        else:
            self.stream = open(self.baseFilename, 'w')
        self.rollover_at += SECONDS_PER_DAY

    def changeDirectory(self, directory):
        self._pathnameprefix = os.path.join(directory, self._filenameprefix)
        self.doRollover()
        t = time.localtime()
        self.rollover_at = time.mktime((t[0], t[1], t[2], 0, 0, 0,
                                        t[6], t[7], t[8])) + SECONDS_PER_DAY


class UserLogfileFormatter(Formatter):

    def format(self, record):
        record.message = record.getMessage()
        if '%(asctime)s' in self._fmt:
            record.asctime = self.formatTime(record, self.datefmt)
        return self._fmt % record.__dict__


class UserLogfileHandler(NicosLogfileHandler):

    def __init__(self, directory):
        NicosLogfileHandler.__init__(self, directory)
        self.setFormatter(UserLogfileFormatter(USERLOGFMT, DATEFMT))
        self.disabled = False

    def filter(self, record):
        return not self.disabled


def initLoggers():
    addLevelName(ACTION, 'ACTION')
    addLevelName(OUTPUT, 'OUTPUT')
    addLevelName(INPUT, 'INPUT')
