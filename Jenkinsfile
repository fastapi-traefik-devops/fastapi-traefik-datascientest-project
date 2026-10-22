// Prepared source only. Jobs remain disabled until an explicit live activation checkpoint.
pipeline {
    agent { label 'host-ci' }
    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        timeout(time: 90, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20', artifactNumToKeepStr: '2'))
        copyArtifactPermission('/trusted/publish')
    }
    // The operator installs the main job's SCM poll only after the first live
    // cycle passes. Keep trigger ownership in job configuration so this first
    // controlled run cannot enable polling early. No cron or folder indexing.
    stages {
        stage('Checkout') {
            steps {
                script {
                    def revision = checkout scm
                    env.IMAGE_SHA = revision.GIT_COMMIT
                    if (!(env.IMAGE_SHA ==~ /[0-9a-f]{40}/)) { error('Full Git SHA required') }
                    env.PUBLISH = (env.BRANCH_NAME == 'main' && !env.CHANGE_ID) ? 'true' : 'false'
                    currentBuild.description = "Functional CI ${env.IMAGE_SHA}; security scans deferred"
                }
            }
        }
        stage('Functional gates') {
            steps {
                script {
                    def gates = sh(returnStdout: true, script: 'python3 ci/phase1.py steps --profile migration').trim().split('\n')
                    for (gate in gates) { stage(gate) { sh "python3 ci/phase1.py ${gate}" } }
                }
            }
        }
        stage('Export tested images') {
            when { expression { env.PUBLISH == 'true' } }
            steps {
                sh 'python3 ci/phase1.py export-images'
                archiveArtifacts artifacts: '.ci-output/*-ci.tar,.ci-output/candidate.json,.ci-output/source-sha.txt,.ci-output/*.xml', fingerprint: true
            }
        }
        stage('Request trusted STAGE publication') {
            when { expression { env.PUBLISH == 'true' } }
            steps {
                build job: '/trusted/publish', wait: false, parameters: [
                    string(name: 'CI_BUILD', value: env.BUILD_NUMBER),
                    string(name: 'SOURCE_JOB', value: 'app-ci/main'),
                    string(name: 'ACTION', value: 'stage')]
            }
        }
    }
    post {
        always {
            script {
                try {
                    if (fileExists('ci/phase1.py')) { sh 'python3 ci/phase1.py migration-report' }
                    for (report in ['backend-unit', 'backend-integration', 'frontend-tests']) {
                        if (fileExists(".ci-output/${report}.xml")) { junit ".ci-output/${report}.xml" }
                    }
                } finally {
                    try { archiveArtifacts artifacts: '.ci-output/*.json,.ci-output/*.xml', allowEmptyArchive: true }
                    finally {
                        try { if (fileExists('ci/phase1.py')) { sh 'python3 ci/phase1.py cleanup' } }
                        finally { deleteDir() }
                    }
                }
            }
        }
    }
}
