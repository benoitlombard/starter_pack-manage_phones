pipeline {
    agent any

    environment {
        // Define Python version and virtual environment path
        PYTHON = 'python3'
        VENV_DIR = '.venv'
    }

    stages {
        stage('Checkout') {
            steps {
                // Pull the latest code from the repository
                checkout scm
            }
        }

        stage('Setup Python Environment') { //python3 venv venv
            steps {
                sh """
                    ls
                    venv venv --distribute
                    . venv/bin/activate 

                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                // Run pytest with JUnit XML output for Jenkins
                sh """
                    source ${VENV_DIR}/bin/activate
                    pytest --junitxml=reports/results.xml
                """
            }
        }

        stage('Publish Test Results') {
            steps {
                // Publish JUnit test results in Jenkins
                junit 'reports/results.xml'
            }
        }
    }

    post {
        always {
            // Clean up virtual environment after build
            sh "rm -rf ${VENV_DIR}"
        }
        failure {
            echo '❌ Tests failed. Check the Jenkins test report.'
        }
        success {
            echo '✅ All tests passed successfully.'
        }
    }
}