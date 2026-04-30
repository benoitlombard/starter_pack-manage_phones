pipeline {

    agent {
        docker {
            image 'python:3.12-slim'
        }
    }


    stages {
        stage('Setup Python Environment') {
            steps {
                sh '''
                    echo deleting virtual envs:
                    rm -rf venv_1
                    rm -rf venv_new
                    rm -rf app/venv_new
                    rm -rf app/app

                    echo creating venv_new:
                    python -m venv app/venv_new

                    echo activating venv_new and pip upgrade:
                    cd app
                    . venv_new/bin/activate
                    pip install --upgrade pip

                    echo installing requirements:
                    cd ..
                    pip install -r requirements.txt


                    cd app
                    python manage_phones_CLI.py --help
                    python manage_phones_CLI.py add --help

                    pytest --junitxml=pytest-report.xml
                    '''
            }
            post {
                always {
                    junit 'pytest-report.xml'
                }
            }
        }
    }
}
