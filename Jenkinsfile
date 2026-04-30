pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            reuseNode true
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python --version
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    mkdir -p reports
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
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