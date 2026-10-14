// Admin-reviewed Docker CI definition. No Kubernetes clouds or deployment access.
pipeline {
    agent { label 'host-ci' }
    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        timeout(time: 90, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20', artifactNumToKeepStr: '2'))
    }
    triggers { pollSCM('H/5 * * * *') }
    stages {
        stage('Checkout') {
            steps {
                script {
                    def revision = checkout([$class: 'GitSCM', branches: [[name: '*/main']],
                        userRemoteConfigs: [[url: 'https://github.com/fastapi-traefik-devops/fastapi-traefik-datascientest-project.git']]])
                    env.IMAGE_SHA = revision.GIT_COMMIT
                    if (!(env.IMAGE_SHA ==~ /[0-9a-f]{40}/)) { error('Full Git SHA required') }
                }
            }
        }
        stage('Validate Docker CI configuration') {
            steps { sh 'python3 ci/phase1.py config' }
        }
        stage('Secret scan: working tree and history') {
            steps { sh 'python3 ci/phase1.py secrets' }
        }
        stage('Backend dependencies') {
            steps { sh 'python3 ci/phase1.py backend-dependencies' }
        }
        stage('Backend lint') {
            steps { sh 'python3 ci/phase1.py backend-lint' }
        }
        stage('Backend unit tests') {
            steps { sh 'python3 ci/phase1.py backend-unit' }
        }
        stage('Backend API and integration tests') {
            steps { sh 'python3 ci/phase1.py backend-integration' }
        }
        stage('Frontend dependencies') {
            steps { sh 'python3 ci/phase1.py frontend-dependencies' }
        }
        stage('Frontend lint') {
            steps { sh 'python3 ci/phase1.py frontend-lint' }
        }
        stage('Frontend build') {
            steps { sh 'python3 ci/phase1.py frontend-build' }
        }
        stage('Frontend E2E tests') {
            steps { sh 'python3 ci/phase1.py frontend-tests' }
        }
        stage('Backend dependency security') {
            steps { sh 'python3 ci/phase1.py backend-security' }
        }
        stage('Frontend dependency security') {
            steps { sh 'python3 ci/phase1.py frontend-security' }
        }
        stage('Docker build backend') {
            steps { sh 'python3 ci/phase1.py backend-image' }
        }
        stage('Docker build frontend') {
            steps { sh 'python3 ci/phase1.py frontend-image' }
        }
        stage('Backend image health and non-root smoke') {
            steps { sh 'python3 ci/phase1.py backend-image-smoke' }
        }
        stage('Frontend image health and non-root smoke') {
            steps { sh 'python3 ci/phase1.py frontend-image-smoke' }
        }
        stage('Container security backend') {
            steps { sh 'python3 ci/phase1.py backend-image-security' }
        }
        stage('Container security frontend') {
            steps { sh 'python3 ci/phase1.py frontend-image-security' }
        }
        stage('Attest successful CI artifacts') {
            steps { sh 'python3 ci/phase1.py attest' }
        }
        stage('Archive verified images and reports') {
            steps {
                archiveArtifacts artifacts: '.ci-output/*-ci.tar,.ci-output/gates.json,.ci-output/source-sha.txt,.ci-output/*.json,.ci-output/*.xml', fingerprint: true
            }
        }
        stage('Schedule trusted registry publication') {
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
