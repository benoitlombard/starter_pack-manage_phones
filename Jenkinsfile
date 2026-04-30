pipeline {        }
    }

    environment {
        VENV_DIR = '.venv'
        HOME = "${WORKSPACE}"
        PIP_CACHE_DIR = "${WORKSPACE}/.pip-cache"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    set -e

                    python --version
                    mkdir -p "$PIP_CACHE_DIR"
                    mkdir -p reports

                    python -m venv "$VENV_DIR"
                    . "$VENV_DIR/bin/activate"

                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    set -e

                    . "$VENV_DIR/bin/activate"
                    pytest --junitxml=reports/results.xml
                '''
            }
        }

        stage('Publish Test Results') {
            steps {
                junit 'reports/results.xml'
            }
        }
    }

    post {
        always {
            sh 'rm -rf "$VENV_DIR" "$PIP_CACHE_DIR"'
            echo 'Pipeline finished.'
        }
        failure {
            echo '❌ Tests failed. Check the Jenkins test report.'
        }
        success {
            echo '✅ All tests passed successfully.'
        }
    }
}

    agent {
        docker {
            image 'python:3.11-slim'
            reuseNode true
