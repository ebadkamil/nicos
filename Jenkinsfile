#!groovy

//*** job setup */
properties([
    buildDiscarder(logRotator(artifactDaysToKeepStr: '',
                              artifactNumToKeepStr: '',
                              daysToKeepStr: '',
                              numToKeepStr: '50')),
    parameters([
        string(defaultValue: 'frm2/nicos/nicos-core',
               description: '', name: 'GERRIT_PROJECT'),
        string(defaultValue: 'refs/heads/master',
               description: '', name: 'GERRIT_BRANCH'),
        string(defaultValue: 'refs/heads/master',
               description: '', name: 'GERRIT_REFSPEC'),
        choice(choices: '''\
patchset-created
ref-updated
change-merged''',
        description: '', name: 'GERRIT_EVENT'),
        choice(choices: '''\
patchset-created
ref-updated
change-merged''',
        description: '', name: 'GERRIT_EVENT_TYPE')]),
        [$class: 'ScannerJobProperty', doNotScan: false],
        [$class: 'RebuildSettings', autoRebuild: false, rebuildDisabled: false],
        [$class: 'ThrottleJobProperty', categories: [],
            limitOneJobWithMatchingParams: false,
            maxConcurrentPerNode: 0,
            maxConcurrentTotal: 4,
            paramsToUseForLimit: '',
            throttleEnabled: false,
            throttleOption: 'project'],
        pipelineTriggers([gerrit(commentTextParameterMode: 'PLAIN',
                                 commitMessageParameterMode: 'PLAIN',
                                 customUrl: '',
                                 gerritProjects: [
                                     [pattern: 'frm2/nicos/nicos-core',
                                      compareType: 'PLAIN',
                                      disableStrictForbiddenFileVerification: false,
                                      branches: [[compareType: 'PLAIN', pattern: 'master'],
                                                 [compareType: 'PLAIN', pattern: 'newprotocol'],
                                                 [compareType: 'PLAIN', pattern: 'release-2.12'],
                                                 [compareType: 'PLAIN', pattern: 'release-2.11']],
                                     ]
                                 ],
                                 serverName: 'defaultServer',
                                 triggerOnEvents: [
                                        patchsetCreated(excludeDrafts: false,
                                                        excludeNoCodeChange: false,
                                                        excludeTrivialRebase: false),
                                        changeMerged(),
                                        commentAddedContains('@recheck')
                                        ]
                                    )])
    ])


// ********************************/


this.verifyresult = [:]

// ************* Function defs ***/
def prepareNode() {
    echo(GERRIT_PROJECT)
    deleteDir()
    unstash 'source'
}

def parseLogs(parserConfigurations) {
    step([$class: 'WarningsPublisher',
          parserConfigurations: parserConfigurations,
          canComputeNew: false,
          canResolveRelativePaths: false,
          canRunOnFailed: true,
          defaultEncoding: 'UTF-8',
          excludePattern: '',
          includePattern: '',
          messagesPattern: '',
          healthy: '',
          unHealthy: '',
          failedTotalAll: '0',
          failedTotalHigh: '0',
          failedTotalLow: '0',
          failedTotalNormal: '0',
          unstableTotalAll: '0',
          unstableTotalHigh: '0',
          unstableTotalLow: '0',
          unstableTotalNormal: '0'])
}

def runPylint() {
    verifyresult.put('pylint',0)
    try {
        withCredentials([string(credentialsId: 'GERRITHTTP', variable: 'GERRITHTTP')]) {
            sh '''\
#! /bin/bash
. ~/pythonvenvs/nicos-w-sys-site-packs2/bin/activate
echo $PATH
set +x

# map instrument libs into nicos tree (pylint does not use the nicos path magic :( )
pushd custom
for d in *;do test -d $d && (ln -s $PWD/$d/lib ../nicos/$d);  done
popd
set -x

set +e
PYFILESCHANGED=$(git diff --name-status `git merge-base HEAD HEAD^` | sed -e '/^D/d' | sed -e 's/R[0-9]*\t[^\t]*\\(.*\\)/R\\1/' | sed -e 's/.\t//' |grep '.py$')
if [[ -n "$PYFILESCHANGED" ]] ; then
    PYTHONPATH=.:${PYTHONPATH} pylint --rcfile=./pylintrc $PYFILESCHANGED | tee pylint_all.txt
else
    echo 'no python files changed'
fi

res=$?
set -e

# switch to the tools venv for running the pylint uploader
. ~/toolsvenv/bin/activate
~/tools/pylint2gerrit.py

# cleanup
set +x
pushd custom
for d in *;do test -d $d && rm -f ../nicos/$d  ;done
popd
set -x
exit $res
'''
            verifyresult.put('pylint', 1)
        }
    }
    catch (all) {
        verifyresult.put('pylint',-1)
    }
    echo "pylint: result=" + verifyresult['pylint']
    gerritverificationpublisher([
        verifyStatusValue: verifyresult['pylint'],
        verifyStatusCategory: 'test ',
        verifyStatusName: 'pylint',
        verifyStatusReporter: 'jenkins',
        verifyStatusRerun: '!recheck'
    ])

    if (verifyresult['pylint'] < 0) {
        error('Failure in pylint')
    }
}

def runSetupcheck() {
    verifyresult.put('sc', 0)
    try {
        withCredentials([string(credentialsId: 'GERRITHTTP',
                                variable: 'GERRITHTTP')]) {
            ansiColor('xterm') {
                sh '''\
#! /bin/bash
. ~/pythonvenvs/nicos-w-sys-site-packs2/bin/activate

tools/check_setups -o setupcheck.log -s custom/*/setups || ((res++)) || /bin/true
# */
# switch to the tools venv for running the setupcheck uploader
. ~/toolsvenv/bin/activate
~/tools/sc2gerrit.py

exit $((res))
'''
            }
            verifyresult.put('sc', 1)
        }
    }
    catch (all) {
        verifyresult.put('sc', -1)
    }
    echo "setupcheck: result=" + verifyresult['sc']
    gerritverificationpublisher([
        verifyStatusValue: verifyresult['sc'],
        verifyStatusCategory: 'test ',
        verifyStatusName: 'setupcheck',
        verifyStatusReporter: 'jenkins',
        verifyStatusRerun: '!recheck'
    ])

    if (verifyresult['sc'] < 0) {
         error('Failure in setupcheck')
    }
}

def runTests(venv, pyver, withcov) {

    writeFile file: 'setup.cfg', text: """
[tool:pytest]
addopts = --junit-xml=pytest.xml
  --junit-prefix=$pyver""" + (withcov ? """
  --cov
  --cov-config=.coveragerc
  --cov-report=html:cov-$pyver
  --cov-report=term
""" : "")

    verifyresult.put(pyver, 0)
    try {
        portallocator([plainports:['NICOS_DAEMON_PORT',
                                   'NICOS_CACHE_PORT',
                                   'NICOS_CACHE_ALT_PORT']]) {
            timeout(10) {
               withEnv(["VENV=$venv"]) {
                  sh '''\
#! /bin/bash
echo $VENV
set +x
. ~/pythonvenvs/$VENV/bin/activate
set -x

pytest -v test'''
verifyresult.put(pyver, 1)
                } // withEnv
            } // timeout
        } // wrap
    } catch(all) {
        verifyresult.put(pyver, -1)
    }

    echo "Test $pyver: result=" + verifyresult[pyver]
    gerritverificationpublisher([
        verifyStatusValue: verifyresult[pyver],
        verifyStatusCategory: 'test ',
        verifyStatusName: 'pytest-'+pyver,
        verifyStatusReporter: 'jenkins',
        verifyStatusRerun: '!recheck'
    ])

    junit([allowEmptyResults: true,
           keepLongStdio: true,
           testResults: 'pytest.xml'])
    if (withcov) {
        archiveArtifacts([allowEmptyArchive: true,
                          artifacts: "cov-$pyver/*"])
        publishHTML([allowMissing: true,
                     alwaysLinkToLastBuild: false,
                     keepAll: true,
                     reportDir: "cov-$pyver/",
                     reportFiles: 'index.html',
                     reportName: "Coverage ($pyver)"])
    }

    if (verifyresult[pyver] < 0) {
        error('Failure in test with ' + pyver)
    }
}

def runDocTest() {
    verifyresult.put('doc', 0)
    try {
        sh '''\
#!/bin/bash
set +x
. ~/pythonvenvs/nicos-w-sys-site-packs/bin/activate
echo $PATH

export doc_changed=`git diff --name-status \\`git merge-base HEAD HEAD^\\` | sed -e '/^D/d' | sed -e 's/.\t//' | grep doc`
if [[ -n "$doc_changed" ]]; then

    cd doc
    make html
    make latexpdf
else
    echo 'no changes in doc/'
fi
'''

        archiveArtifacts([allowEmptyArchive: true,
                          artifacts: 'doc/build/latex/NICOS.*'])
        publishHTML([allowMissing: true,
                     alwaysLinkToLastBuild: true,
                     keepAll: true,
                     reportDir: 'doc/build/html',
                     reportFiles: 'index.html',
                     reportName: 'Nicos Doc (test build)'])

        verifyresult.put('doc', 1)
    } catch (all) {
        verifyresult.put('doc',-1 )
    }
    echo "Docs: result=" + verifyresult['doc']

    gerritverificationpublisher([
        verifyStatusValue: verifyresult['doc'],
        verifyStatusCategory: 'test ',
        verifyStatusName: 'doc',
        verifyStatusReporter: 'jenkins',
        verifyStatusRerun: '!recheck'
    ])

    if (verifyresult['doc'] < 0) {
        error('Failure in doc test')
    }
}

// *************End Function defs ***/

// ************* Start main script ***/
timestamps {

stage(name: 'checkout code: ' + GERRIT_PROJECT) {
    node('master') {
        echo(GERRIT_PROJECT)
        deleteDir()
        checkout(
            changelog: true, poll: false,
            scm: [$class: 'GitSCM',
                  branches: [[name: "$GERRIT_BRANCH"]],
                  doGenerateSubmoduleConfigurations: false, submoduleCfg: [],
                  userRemoteConfigs: [
                      [refspec: GERRIT_REFSPEC,
                       // use local mirror via git
                       url: 'file:///home/git/' + GERRIT_PROJECT
                       // use gerrit directly
                       //credentialsId: 'jenkinsforge',
                       //url: 'ssh://forge.frm2.tum.de:29418/' + GERRIT_PROJECT,
                      ]
                  ],
                  extensions: [
                      [$class: 'CleanCheckout'],
                      [$class: 'hudson.plugins.git.extensions.impl.BuildChooserSetting',
                       buildChooser: [$class: "com.sonyericsson.hudson.plugins.gerrit.trigger.hudsontrigger.GerritTriggerBuildChooser"]],
                  ]
                 ])
        sh '''git describe'''
        stash(name: 'source', includes: '**, .git, .git/**', useDefaultExcludes: false)
    }
}

stage(name: 'prepare') {
    def params = [
        string(name: 'GERRIT_PROJECT', value: GERRIT_PROJECT),
        string(name: 'GERRIT_BRANCH', value: GERRIT_BRANCH),
        string(name: 'GERRIT_REFSPEC', value: GERRIT_REFSPEC),
        string(name: 'GERRIT_EVENT_TYPE', value: GERRIT_EVENT_TYPE),
        string(name: 'GERRIT_CHANGE_SUBJECT', value: GERRIT_CHANGE_SUBJECT),
        string(name: 'GERRIT_CHANGE_URL', value: GERRIT_CHANGE_URL),
    ]
    if (GERRIT_EVENT == 'ref-updated') {  // only set for ref-updated
        params << string(name: 'GERRIT_REFNAME', value: GERRIT_REFNAME)
    }
    if (GERRIT_EVENT != 'ref-updated') {  // these are not set for ref-updated
        params << string(name: 'GERRIT_PATCHSET_NUMBER', value: GERRIT_PATCHSET_NUMBER)
        params << string(name: 'GERRIT_PATCHSET_REVISION', value: GERRIT_PATCHSET_REVISION)
    }
    build ([job: 'NicosUpdateRedminePre',
            parameters: params])
}

//
parallel pylint: {
    stage(name: 'pylint') {
        node('ubuntu12.04') {
            prepareNode()
            runPylint()
            parseLogs([[parserName: 'PyLint', pattern: 'pylint_*.txt']])
        }
    }
}, setup_check: {
    stage(name: 'Nicos Setup check') {
        node('ubuntu12.04') {
            prepareNode()
            timeout(5) {
                runSetupcheck()
            }
            parseLogs([
                [parserName: 'nicos-setup-check-syntax-errors', pattern: 'setupcheck.log'],
                [parserName: 'nicos-setup-check-errors-file', pattern: 'setupcheck.log'],
                [parserName: 'nicos-setup-check-warnings', pattern: 'setupcheck.log'],
            ])
        }
    }
}, test_python2: {
    stage(name: 'Python2 tests')  {
        node('ubuntu12.04') {
            prepareNode()
            runTests( 'nicos-w-sys-site-packs2', 'python2', GERRIT_EVENT_TYPE == 'change-merged')
        }
    }
}, test_python2centos: {
    stage(name: 'Python2(centos) tests') {
        if (GERRIT_EVENT_TYPE == 'change-merged') {
            node('CentOS && jenkins && !i386') {
                prepareNode()
                runTests('nicos-w-sys-site-packs2', 'python2-centos', false)
            }
        }
    }
}, test_python3: {
    stage(name: 'Python3 tests') {
        node('ubuntu14.04') {
            prepareNode()
            runTests('nicos-py3-new', 'python3', GERRIT_EVENT_TYPE == 'change-merged')
        }
    }
}, test_docs: {
    stage(name: 'Test docs') {
        node('ubuntu-12-2') {
            prepareNode()
            runDocTest()
        }
    }
},
failFast: false

/*** set final vote **/
setGerritReview()
}
