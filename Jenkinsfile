pipeline {
    agent any  // Run on any available agent

    stages {
        stage("Clone Code") {
            steps {
                echo "Cloning the code"
                git url: "https://github.com/benoitlombard/starter_pack-manage_phones", branch: "main"
            }
        }
        stage('Install Dependencies') {
            steps {
                script {
                    def requirements = [
                        'requirements.txt'
                    ]
                    for (req in requirements) {
                        if (fileExists(req)) {
                            sh """
                            source venv/bin/activate
                            pip install -r ${req}
                            """
                        }
                    }
                }
            }
        }
/*
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
*/
        stage("Build") {
            steps {
                echo "Building the Docker image"
                sh "docker build -t pipeline ."
            }
        }
    }
}