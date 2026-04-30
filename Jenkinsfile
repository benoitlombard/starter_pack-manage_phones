pipeline {
    agent true    agent {
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                sh '''
                    python -m venv .venv
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    mkdir -p reports
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest --junitxml=reports/results.xml
                '''
            }
        }

        stage('Results') {
            steps {
                junit 'reports/results.xml'
            }
        }
    }

    post {
        always {
            sh 'rm -rf .venv .pip-cache'
        }
    }
}
        docker {
            image 'python:3.11-slim'
