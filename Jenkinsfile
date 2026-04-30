pipeline {
    agent any

    environment {
        // Define Python version and virtual environment path
        PYTHON = 'python3'
        VENV_DIR = '.venv'
    } options {
        skipStagesAfterUnstable()
    }

    stages {
        stage('Setup Python Environment') {
            steps {
                sh """
                    ls
                    ${PYTHON} -m venv ${VENV_DIR}
                    ls
                    source ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        } stage('Build') {
            steps {
                sh 'python3 -m py_compile app/manage_phones_CLI'
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