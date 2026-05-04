pipeline {
    agent any

    stages {
        stage('Setup and Test') {
            steps {
                sh '''
                    set -e
                    
                    echo "Creating virtual environment..."
                    python3 -m venv venv
                    . venv/bin/activate
                    
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
                    junit 'pytest-report.xml'
                }
            }
        }
    }
}
