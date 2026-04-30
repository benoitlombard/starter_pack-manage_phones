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
                    echo Installing Python...
                    python -m venv app/venv_new
                    ls
                    source app/venv_new/bin/activate
                    pip install --upgrade pip
                    '''
            }
        }
    }
}
