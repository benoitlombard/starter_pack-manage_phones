pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Setup Python Environment') {
            steps {
                sh '''
                    echo deleting virtual envs:
                    rm -rf venv_new
                    rm -rf app/venv_new

                    echo creating venv_new:
                    python3 -m venv app/venv_new

                    echo activating venv_new and pip upgrade:
                    cd app
                    . venv_new/bin/activate
                    pip install --upgrade pip

                    echo installing requirements:
                    cd ..
                    pip install -r requirements.txt
                    '''
            }
        }
        stage('Linting') {
            steps {
                sh '''
                    pwd
                    ls
                    cd app
                    ls
                    python manage_phones_CLI.py --help
                    python manage_phones_CLI.py add --help

                    ruff check add_phone.py
                    ruff check change_phone.py
                    ruff check deploy_phone.py
                    ruff check display_infos.py
                    ruff check remove_undeploy_phone.py
                    ruff check manage_phones_CLI.py
                    ruff check decorators_file.py
                    ruff check error_methods.py
                    '''
            }
        }
        stage('Unit tests') {
            steps {
                sh '''
                    pytest --junitxml=pytest-report.xml
                    '''
            }
            post {
                always {
                    junit 'app/pytest-report.xml'
                }
            }
        }
    }
}