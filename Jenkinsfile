
pipeline {
    agent any

    stages {
        stage('Clean') {
            steps {
                deleteDir()
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test Docker') {
            steps {
                sh 'docker version'
            }
        }
    }
}
