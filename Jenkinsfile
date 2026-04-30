pipeline {
    agent any  // Run on any available agent
    environment {
            PYTHON_VERSION = "3.12"
            VIRTUAL_ENV = "myVirtualEnv"
    }
    stages {
        stage("Clone Code") {
            steps {
                echo "Cloning the code"
                git url: "https://github.com/benoitlombard/starter_pack-manage_phones", branch: "main"
            }
        }
        stage('Setup vritual Environment') {
            steps {
                sh '''
                    ls
                    python3 -m venv myVirtualEnv
                    source ${VIRTUAL_ENV}/bin/activate
                    pip install --upgrade pip
                '''
            }
        }
        stage('Install Dependencies') {
            steps {
                script {
                    sh '''
                        source venv/bin/activate
                        pip install -r typer
                    '''
                    echo "typer installed"
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