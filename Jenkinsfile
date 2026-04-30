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
                    ls
                    python -m venv app/venv_new
                    cd app
                    ls
                    . venv_new/bin/activate
                    pip install --upgrade pip
                    '''
            }
        }
    }
}
