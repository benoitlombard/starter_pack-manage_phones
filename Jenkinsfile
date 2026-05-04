pipeline {
    agent any

    stages {
        stage('Install Python') {
            steps {
                sh '''
                    sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv
                '''
            }
        }
        
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
