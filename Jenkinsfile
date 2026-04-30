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
                    python -m venv venv_1
                    ls
                    source venv_1/bin/activate
                    pip install --upgrade pip
                    '''
            }
        }
    }
}
