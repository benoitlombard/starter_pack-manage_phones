pipeline {
    agent any  // Run on any available agent

    stages {
        stage('Hello') {
            steps {
                echo 'Hello World' // Print to Jenkins console log



            }
        }

        stage('Setup Virtual Environment') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv venv
                            source venv/bin/activate
                            pip install --upgrade pip setuptools wheel
                        '''
                    } else {
                        bat '''
                            python -m venv venv
                            call venv\\Scripts\\activate.bat
                            pip install --upgrade pip setuptools wheel
                        '''
                    }
                }
            }
        }
        stage('Build') {
            steps {
                echo 'build part'





            }
        }
    }
}