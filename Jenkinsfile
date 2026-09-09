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
  containers:
  - name: python-tester
    image: ghcr.io/astral-sh/uv:python3.10-bookworm-slim
    command: ['cat']
    tty: true

  - name: node-tester
    image: node:20
    command: ['cat']
    tty: true

  - name: buildkit
    image: moby/buildkit:v0.24.0
    command: ['cat']
    tty: true
    securityContext:
      privileged: true
    volumeMounts:
    - name: docker-config
      mountPath: /root/.docker
      readOnly: true

  volumes:
  - name: docker-config
    secret:
      secretName: ghcr-creds
      items:
      - key: .dockerconfigjson
        path: config.json
'''
        }
    }

    environment {
        REGISTRY     = 'ghcr.io/fastapi-traefik-devops'
        BACKEND_IMG  = "${REGISTRY}/fastapi-backend"
        FRONTEND_IMG = "${REGISTRY}/fastapi-frontend"
        TAG          = "${BUILD_NUMBER}-${GIT_COMMIT[0..7]}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend Tests') {
            steps {
                container('python-tester') {
                    sh '''
                        set -eu
                        echo "--- Testing Backend with UV ---"
                        cd backend
                        uv sync --frozen
                    '''
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
                    '''
                }
            }
        }

        stage('Build & Push Backend') {
            steps {
                container('buildkit') {
                    sh '''
                        set -eu

                        echo "--- Starting BuildKit Daemon ---"
                        rm -f /tmp/buildkitd.sock

                        buildkitd \
                          --addr unix:///tmp/buildkitd.sock \
                          > /tmp/buildkitd.log 2>&1 &

                        BUILDKIT_PID=$!
                        trap 'kill ${BUILDKIT_PID} 2>/dev/null || true' EXIT

                        echo "--- Waiting for BuildKit ---"
                        until buildctl \
                          --addr unix:///tmp/buildkitd.sock \
                          debug workers > /dev/null 2>&1
                        do
                            sleep 1
                        done

                        echo "--- BuildKit is ready ---"
                        test -f /root/.docker/config.json

                        echo "--- Building Backend Image via BuildKit ---"
                        buildctl \
                          --addr unix:///tmp/buildkitd.sock \
                          build \
                          --frontend dockerfile.v0 \
                          --local context="${WORKSPACE}/backend" \
                          --local dockerfile="${WORKSPACE}/backend" \
                          --output "type=image,name=${BACKEND_IMG}:${TAG},name=${BACKEND_IMG}:latest,push=true" \
                          --progress=plain

                        echo "--- Backend image pushed successfully ---"
                    '''
                }
            }
        }

        stage('Build & Push Frontend') {
            steps {
                container('buildkit') {
                    sh '''
                        set -eu

                        echo "--- Starting BuildKit Daemon ---"
                        rm -f /tmp/buildkitd.sock

                        buildkitd \
                          --addr unix:///tmp/buildkitd.sock \
                          > /tmp/buildkitd.log 2>&1 &

                        BUILDKIT_PID=$!
                        trap 'kill ${BUILDKIT_PID} 2>/dev/null || true' EXIT

                        echo "--- Waiting for BuildKit ---"
                        until buildctl \
                          --addr unix:///tmp/buildkitd.sock \
                          debug workers > /dev/null 2>&1
                        do
                            sleep 1
                        done

                        echo "--- BuildKit is ready ---"
                        test -f /root/.docker/config.json

                        echo "--- Building Frontend Image via BuildKit ---"
                        buildctl \
                          --addr unix:///tmp/buildkitd.sock \
                          build \
                          --frontend dockerfile.v0 \
                          --local context="${WORKSPACE}/frontend" \
                          --local dockerfile="${WORKSPACE}/frontend" \
                          --opt build-arg:VITE_API_URL=https://api.localhost \
                          --output "type=image,name=${FRONTEND_IMG}:${TAG},name=${FRONTEND_IMG}:latest,push=true" \
                          --progress=plain

                        echo "--- Frontend image pushed successfully ---"
                    '''
                }
            }
        }

        stage('Validate K8s Manifests') {
            steps {
                sh '''
                    echo "--- Dry-run validation of k8s/ manifests ---"
                    kubectl apply --dry-run=client -n dev -f k8s/
                '''
            }
        }
    }

    post {
        always {
            container('python-tester') {
                sh '''
                    echo "--- Cleaning UV virtual environment ---"
                    rm -rf "${WORKSPACE}/backend/.venv" || true
                '''
            }
            cleanWs()
        }
    }
}
