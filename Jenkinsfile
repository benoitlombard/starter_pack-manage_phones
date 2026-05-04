pipeline {
    agent {
        docker {
            image 'python:3.12-slim'
            reuseNode true
        }
    }

    stages {
        stage('Setup and Test') {
            steps {
                sh '''
                    set -e
                    
                    echo "Installing dependencies..."
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    
                    echo "Testing CLI help commands..."
                    python manage_phones_CLI.py --help
                    python manage_phones_CLI.py add --help
                    
                    echo "Running tests..."
                    pytest --junitxml=pytest-report.xml
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'pytest-report.xml'
                }
            }
        }
    }
}
