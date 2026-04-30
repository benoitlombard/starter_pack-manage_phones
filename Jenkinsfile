pipeline {
    agent any
    stages {
        stage {
            steps {
                sh {
                    echo 'Installing Python...'
                    sh 'python3 -m virtualenv venv_1'
                    sh 'source venv_1/bin/activate'
                    sh 'pip install --upgrade pip'
                }
            }
        }
    }
}
