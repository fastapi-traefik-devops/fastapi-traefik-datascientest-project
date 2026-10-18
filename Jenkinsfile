// CI for the multibranch job app-ci: main and pull requests. No Kubernetes clouds or deployment access.
// The gates and their profiles are defined once in ci/phase1.py:
//   pull request, nightly run on main -> "full" (all 18 gates plus GitOps validation)
//   merge to main                     -> "release" (artifact gates and attestation), then trusted/publish
pipeline {
    agent { label 'host-ci' }
    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        timeout(time: 90, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20', artifactNumToKeepStr: '2'))
        // Only the trusted registry publisher may copy the verified image archives.
        // Absolute name: relative names resolve from this job's folder (app-ci/).
        copyArtifactPermission('/trusted/publish')
    }
    // Branch and pull request changes come from the multibranch scan; only main also runs nightly.
    triggers { cron(env.BRANCH_NAME == 'main' ? 'H 2 * * *' : '') }
    stages {
        stage('Checkout') {
            steps {
                script {
                    def revision = checkout scm
                    env.IMAGE_SHA = revision.GIT_COMMIT
                    if (!(env.IMAGE_SHA ==~ /[0-9a-f]{40}/)) { error('Full Git SHA required') }
                    def nightly = !currentBuild.getBuildCauses('hudson.triggers.TimerTrigger$TimerTriggerCause').isEmpty()
                    env.CI_PROFILE = (env.CHANGE_ID || nightly) ? 'full' : 'release'
                    env.PUBLISH = (env.BRANCH_NAME == 'main' && env.CI_PROFILE == 'release') ? 'true' : 'false'
                    env.GITOPS_ONLY = 'false'
                    if (env.PUBLISH == 'true') {
                        // GitOps promotion commits only change deploy/overlays/; rebuilding and
                        // republishing for them would promote again and loop forever.
                        def previous = revision.GIT_PREVIOUS_SUCCESSFUL_COMMIT
                        if (previous ==~ /[0-9a-f]{40}/ && previous != env.IMAGE_SHA) {
                            def appChange = sh(returnStatus: true,
                                script: "git diff --name-only ${previous} ${env.IMAGE_SHA} | grep -qv '^deploy/overlays/'") == 0
                            if (!appChange) { env.GITOPS_ONLY = 'true' }
                        }
                    }
                    currentBuild.description = env.GITOPS_ONLY == 'true' ?
                        'GitOps-only change: CI gates and publication skipped' :
                        "Profile ${env.CI_PROFILE}${nightly ? ' (nightly)' : ''}${env.PUBLISH == 'true' ? ', publishes to GHCR' : ''}"
                }
            }
        }
        stage('CI gates') {
            when { expression { env.GITOPS_ONLY != 'true' } }
            steps {
                script {
                    def gates = sh(returnStdout: true, script: "python3 ci/phase1.py steps --profile ${env.CI_PROFILE}").trim().split('\n')
                    for (gate in gates) {
                        stage(gate) { sh "python3 ci/phase1.py ${gate}" }
                    }
                }
            }
        }
        stage('Archive verified images and reports') {
            when { expression { env.PUBLISH == 'true' && env.GITOPS_ONLY != 'true' } }
            steps {
                archiveArtifacts artifacts: '.ci-output/*-ci.tar,.ci-output/gates.json,.ci-output/source-sha.txt,.ci-output/*.json,.ci-output/*.xml', fingerprint: true
            }
        }
        stage('Schedule trusted registry publication') {
            when { expression { env.PUBLISH == 'true' && env.GITOPS_ONLY != 'true' } }
            steps {
                script {
                    build job: '/trusted/publish', wait: false,
                        parameters: [string(name: 'CI_BUILD', value: env.BUILD_NUMBER)]
                }
            }
        }
    }
    post {
        always {
            script {
                if (fileExists('.ci-output/backend-unit.xml')) { junit '.ci-output/backend-unit.xml' }
                if (fileExists('.ci-output/backend-integration.xml')) { junit '.ci-output/backend-integration.xml' }
                if (fileExists('.ci-output/frontend-tests.xml')) { junit '.ci-output/frontend-tests.xml' }
                archiveArtifacts artifacts: '.ci-output/*.json,.ci-output/*.xml', allowEmptyArchive: true
                if (fileExists('ci/phase1.py')) { sh 'python3 ci/phase1.py cleanup' }
            }
            deleteDir()
        }
    }
}
