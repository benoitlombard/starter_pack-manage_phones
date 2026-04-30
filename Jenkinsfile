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
                    deactivate
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
                    . app/venv_new/bin/activate.psl
                    pip install --upgrade pip
                    '''
            }
        }
    }
}
