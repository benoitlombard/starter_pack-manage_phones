pipeline {
    agent any
    options {
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
                sh 'python3 -m py_compile app/manage_phones_CLI.py'
            }
        } stage('Run Tests') {
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