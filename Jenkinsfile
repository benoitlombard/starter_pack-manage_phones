pipeline {
    agent any
    stages {
        stage('Setup Python Environment') {
            steps {
                sh '''
                    ls
                    echo Installing Python...
                    python -m virtualenv venv_1
                    source venv_1/bin/activate
                    pip install --upgrade pip
                    '''
            }
        }
    }
}
