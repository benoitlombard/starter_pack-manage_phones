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
                    ls
                    rm -rf venv_1
                    rm -rf venv_new
                    rm -rf app/venv_new
                    ls



                    echo Installing Python...
                    python -m venv app/venv_new
                    ls
                    cd app
                    ls
                    cd venv_new
                    ls
                    cd bin
                    ls
                    pwd
                    pip install --upgrade pip
                    '''
            }
        }
    }
}
