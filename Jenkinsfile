pipeline {
    agent {
        kubernetes {
            namespace 'dev'
            yaml '''
apiVersion: v1
kind: Pod
metadata:
  labels:
    component: jenkins-agent
spec:
  automountServiceAccountToken: false
  volumes:
  - name: ghcr-auth
    secret:
      secretName: ghcr-creds
      items:
      - key: .dockerconfigjson
        path: config.json
  containers:
  - name: python-tester
    image: ghcr.io/astral-sh/uv:0.5.11-python3.10-bookworm-slim
    command:
      - /bin/sh
      - -c
      - sleep infinity
    tty: true
    resources:
      requests:
        cpu: 250m
        memory: 256Mi
      limits:
        cpu: "1"
        memory: 1Gi

  - name: node-tester
    image: node:20
    command:
      - /bin/sh
      - -c
      - sleep infinity
    tty: true
    resources:
      requests:
        cpu: 250m
        memory: 256Mi
      limits:
        cpu: "1"
        memory: 1Gi

  - name: buildkit
    image: moby/buildkit:v0.24.0
    env:
    - name: DOCKER_CONFIG
      value: /run/ghcr-auth
    volumeMounts:
    - name: ghcr-auth
      mountPath: /run/ghcr-auth
      readOnly: true
    command:
      - /bin/sh
      - -c
      - sleep infinity
    tty: true
    resources:
      requests:
        cpu: 250m
        memory: 512Mi
      limits:
        cpu: "2"
        memory: 2Gi
    securityContext:
      privileged: true

  # Disposable database: loopback-only, no Service or persistent volume.
  - name: postgres-test
    image: postgres:16
    args: ["-c", "listen_addresses=127.0.0.1"]
    env:
    - name: POSTGRES_DB
      value: app_ci
    # Disposable CI password, never used for an application database.
    - name: POSTGRES_PASSWORD
      value: ci-only-postgres-password
    resources:
      requests:
        cpu: 250m
        memory: 256Mi
      limits:
        cpu: "1"
        memory: 1Gi
'''
        }
    }

    options {
        skipDefaultCheckout(true)
        timeout(time: 45, unit: 'MINUTES')
        disableConcurrentBuilds()
        timestamps()
    }

    parameters {
        booleanParam(name: 'PUSH_IMAGES', defaultValue: false,
            description: 'Publish both images to GHCR after checks pass (main branch only).')
        string(name: 'PUBLISH_API_URL', defaultValue: '',
            description: 'Browser-accessible API URL embedded in published frontend images; required when PUSH_IMAGES is enabled.')
    }

    environment {
        REGISTRY_NAMESPACE = 'ghcr.io/fastapi-traefik-devops'
        CI = 'true'
        // Test-only settings. PostgreSQL is isolated inside this agent Pod.
        ENVIRONMENT = 'local'
        PROJECT_NAME = 'FastAPI CI'
        POSTGRES_SERVER = '127.0.0.1'
        POSTGRES_PORT = '5432'
        POSTGRES_DB = 'app_ci'
        POSTGRES_USER = 'postgres'
        POSTGRES_PASSWORD = 'ci-only-postgres-password'
        FIRST_SUPERUSER = 'ci-admin@example.com'
        EMAIL_TEST_USER = 'test@example.com'
        EMAILS_FROM_EMAIL = 'ci@example.com'
        EMAILS_FROM_NAME = 'ci@example.com'
        SMTP_HOST = '127.0.0.1'
        SMTP_PORT = '1025'
        SMTP_TLS = 'false'
        SMTP_SSL = 'false'
        BACKEND_CORS_ORIGINS = 'http://localhost:5173'
        FRONTEND_HOST = 'http://localhost:5173'
        VITE_API_URL = "${params.PUSH_IMAGES ? params.PUBLISH_API_URL.trim() : 'http://localhost:8000'}"
    }

    stages {

        stage('Checkout') {
            steps {
                script {
                    def revision = checkout scm
                    env.IMAGE_TAG = revision.GIT_COMMIT
                    env.CHECKED_OUT_BRANCH = revision.GIT_BRANCH
                    env.PUBLISH_IMAGES = params.PUSH_IMAGES ? 'true' : 'false'
                    if (params.PUSH_IMAGES) {
                        if (env.CHANGE_ID || !(env.CHECKED_OUT_BRANCH in ['main', 'origin/main']) ||
                            (env.BRANCH_NAME && env.BRANCH_NAME != 'main')) {
                            error('Image publishing is allowed only from main, never from pull requests.')
                        }
                        if (!params.PUBLISH_API_URL?.trim()) {
                            error('Set PUBLISH_API_URL before publishing frontend images.')
                        }
                    }
                }
            }
        }

        stage('Backend Checks and Tests') {
            steps {
                container('python-tester') {
                    sh '''
                        set -eu
                        # Jenkins sh normally enables tracing; keep ephemeral keys out of logs.
                        set +x
                        cd backend
                        uv sync --frozen
                        SECRET_KEY="$(uv run --frozen python -c 'import secrets; print(secrets.token_urlsafe(32))')"
                        FIRST_SUPERUSER_PASSWORD="$(uv run --frozen python -c 'import secrets; print(secrets.token_urlsafe(24))')"
                        export SECRET_KEY FIRST_SUPERUSER_PASSWORD
                        uv run --frozen bash scripts/lint.sh
                        uv run --frozen bash scripts/prestart.sh
                        test_status=0
                        uv run --frozen coverage run --source=app -m pytest --junitxml=test-results.xml || test_status=$?
                        # Preserve reports on test failure without hiding pytest's exit status.
                        report_status=0
                        uv run --frozen coverage report --show-missing || report_status=$?
                        uv run --frozen coverage xml -o coverage.xml || report_status=$?
                        if [ "$test_status" -ne 0 ]; then
                            exit "$test_status"
                        fi
                        exit "$report_status"
                    '''
                }
            }
            post {
                always {
                    junit testResults: 'backend/test-results.xml', allowEmptyResults: true
                    archiveArtifacts artifacts: 'backend/coverage.xml', allowEmptyArchive: true
                }
            }
        }

        stage('Frontend Check') {
            steps {
                container('node-tester') {
                    sh '''
                        set -eu
                        echo "--- Verifying Frontend Dependencies ---"
                        cd frontend
                        npm ci
                        npm run build
                    '''
                }
            }
        }

        stage('Build and Optionally Push Images') {
            steps {
                container('buildkit') {
                    sh '''
                        set -eu
                        buildkitd --addr unix:///tmp/buildkitd.sock > /tmp/buildkitd.log 2>&1 &
                        BUILDKIT_PID=$!
                        trap 'kill "${BUILDKIT_PID}" 2>/dev/null || true; wait "${BUILDKIT_PID}" 2>/dev/null || true' EXIT

                        ready=false
                        for i in $(seq 1 60); do
                            if buildctl --addr unix:///tmp/buildkitd.sock debug workers > /dev/null 2>&1; then
                                ready=true
                                break
                            fi
                            if ! kill -0 "${BUILDKIT_PID}" 2>/dev/null; then
                                cat /tmp/buildkitd.log
                                exit 1
                            fi
                            sleep 1
                        done
                        if [ "$ready" != true ]; then
                            cat /tmp/buildkitd.log
                            echo "BuildKit did not become ready within 60 seconds"
                            exit 1
                        fi

                        # Verify both image builds before any registry writes.
                        buildctl --addr unix:///tmp/buildkitd.sock build \
                          --frontend dockerfile.v0 \
                          --local context="${WORKSPACE}/backend" \
                          --local dockerfile="${WORKSPACE}/backend" \
                          --output type=oci,dest=/tmp/backend-ci.tar \
                          --progress=plain

                        buildctl --addr unix:///tmp/buildkitd.sock build \
                          --frontend dockerfile.v0 \
                          --local context="${WORKSPACE}/frontend" \
                          --local dockerfile="${WORKSPACE}/frontend" \
                          --opt "build-arg:VITE_API_URL=${VITE_API_URL}" \
                          --output type=oci,dest=/tmp/frontend-ci.tar \
                          --progress=plain

                        if [ "${PUBLISH_IMAGES}" = true ]; then
                            # Reuse the completed builds from this daemon's local cache.
                            # Commit tags identify the source; do not overwrite latest.
                            buildctl --addr unix:///tmp/buildkitd.sock build \
                              --frontend dockerfile.v0 \
                              --local context="${WORKSPACE}/backend" \
                              --local dockerfile="${WORKSPACE}/backend" \
                              --output "type=image,name=${REGISTRY_NAMESPACE}/fastapi-backend:${IMAGE_TAG},push=true" \
                              --progress=plain

                            buildctl --addr unix:///tmp/buildkitd.sock build \
                              --frontend dockerfile.v0 \
                              --local context="${WORKSPACE}/frontend" \
                              --local dockerfile="${WORKSPACE}/frontend" \
                              --opt "build-arg:VITE_API_URL=${VITE_API_URL}" \
                              --output "type=image,name=${REGISTRY_NAMESPACE}/fastapi-frontend:${IMAGE_TAG},push=true" \
                              --progress=plain
                        else
                            echo "Image publishing disabled; both images built locally."
                        fi
                    '''
                }
            }
        }
    }

    post {
        always {
            // Tool containers create root-owned files; clean them in the same
            // container before the inbound agent removes the workspace.
            container('python-tester') {
                sh '''
                    set -eu
                    test -n "${WORKSPACE}"
                    test "${WORKSPACE}" != /
                    cd "${WORKSPACE}"
                    find . -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +
                '''
            }
            deleteDir()
        }
    }
}
