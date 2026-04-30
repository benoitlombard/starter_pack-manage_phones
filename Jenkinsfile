pipeline {
    agent any
    stages {
        stage {
            name: 'Install Python',
            steps {
                sh {
                    echo 'Installing Python...'
                    sh 'python3 -m virtualenv ${VIRTUAL_ENV}'
                    sh 'source ${VIRTUAL_ENV}/bin/activate'
                    sh 'pip install --upgrade pip'
                }
            }
        }
    }
}
