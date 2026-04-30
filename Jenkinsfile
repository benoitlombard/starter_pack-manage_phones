pipeline {
    agent any
    stages {
        stage('Setup Python Environment') {
            steps {
                sh'''
                    echo 'Installing Python...
                    python3 -m virtualenv venv_1
                    source venv_1/bin/activate
                    pip install --upgrade pip
                '''
            }
        }
    }
}
