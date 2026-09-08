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
  - name: kaniko
    image: gcr.io/kaniko-project/executor:debug
    command: ['cat']
    tty: true
    volumeMounts:
    - name: docker-config
      mountPath: /kaniko/.docker
  volumes:
  - name: docker-config
    secret:
      secretName: ghcr-creds
'''
        }
    }

    environment {
        REGISTRY    = 'ghcr.io/fastapi-traefik-devops'
        BACKEND_IMG = "${REGISTRY}/fastapi-backend"
        FRONTEND_IMG= "${REGISTRY}/fastapi-frontend"
        TAG         = "${BUILD_NUMBER}-${GIT_COMMIT[0..7]}"
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
                        echo "--- Testing Backend with UV ---"
                        cd backend
                        uv sync --frozen
                        # uv run pytest
                    '''
                }
            }
        }

        stage('Frontend Check') {
            steps {
                container('node-tester') {
                    sh '''
                        echo "--- Verifying Frontend Dependencies ---"
                        cd frontend
                        npm ci
                    '''
                }
            }
        }

        stage('Build & Push Backend') {
            steps {
                container('kaniko') {
                    sh '''
                        echo "--- Building Backend Image via Kaniko ---"
                        /kaniko/executor \
                          --context=dir://backend \
                          --dockerfile=backend/Dockerfile \
                          --destination=${BACKEND_IMG}:${TAG} \
                          --destination=${BACKEND_IMG}:latest
                    '''
                }
            }
        }

        stage('Build & Push Frontend') {
            steps {
                container('kaniko') {
                    sh '''
                        echo "--- Building Frontend Image via Kaniko ---"
                        /kaniko/executor \
                          --context=dir://frontend \
                          --dockerfile=frontend/Dockerfile \
                          --destination=${FRONTEND_IMG}:${TAG} \
                          --destination=${FRONTEND_IMG}:latest
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
            deleteDir()
        }
    }
}
