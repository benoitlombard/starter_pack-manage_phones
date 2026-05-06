pipeline {
    agent any
    parameters {
        booleanParam(name: 'run full test', defaultValue: true, description: '   Other parameters will be ignored if this parameter is checked.')
        string(name: 'COMMANDS', defaultValue: 'python manage_phones_CLI.py change --phone Chaos --release-type PU100 --user jean', description: '   Additional commands to execute (separator = ",")')
        booleanParam(name: 'add a new phone', defaultValue: false, description: '')
        booleanParam(name: 'change existing phone', defaultValue: false, description: '')
        booleanParam(name: 'deploy phone', defaultValue: false, description: '')
        booleanParam(name: 'undeploy phone', defaultValue: false, description: '')
        booleanParam(name: 'remove phone', defaultValue: false, description: '')
        booleanParam(name: 'show phone configuration', defaultValue: false, description: '')
        booleanParam(name: 'display phones', defaultValue: false, description: '')
        booleanParam(name: 'display bts', defaultValue: false, description: '')
        booleanParam(name: 'display biabs', defaultValue: false, description: '')
        booleanParam(name: 'display prod stage', defaultValue: false, description: '')
        booleanParam(name: 'display dev stage', defaultValue: false, description: '')
        booleanParam(name: 'display not deployed phones', defaultValue: false, description: '')

    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Setup Python Environment') {
            steps {
                sh '''
                    echo deleting virtual envs:
                    rm -rf venv_new
                    rm -rf app/venv_new

                    echo creating venv_new:
                    python3 -m venv app/venv_new

                    echo activating venv_new and pip upgrade:
                    cd app
                    . venv_new/bin/activate
                    pip install --upgrade pip

                    echo installing requirements:
                    cd ..
                    pip install -r requirements.txt
                    '''
            }
        }
        stage('Linting') {
            steps {
                sh '''
                    cd app
                    . venv_new/bin/activate

                    ruff check add_phone.py
                    ruff check change_phone.py
                    ruff check deploy_phone.py
                    ruff check display_infos.py
                    ruff check remove_undeploy_phone.py
                    ruff check manage_phones_CLI.py
                    ruff check decorators_file.py
                    ruff check error_methods.py

                    python manage_phones_CLI.py --help
                    python manage_phones_CLI.py add --help
                    '''
            }
        }
        stage('Unit tests') {
            steps {
                sh '''
                    VARS_FILE="test_requirements.txt"
                    while IFS='=' read -r key value; do
                        [[ -z "$key" || "$key" =~ ^# ]] && continue
                        export "$key=$value"

                    done < "$VARS_FILE"
                    echo "full_test: $full_test"

                    cd app
                    . venv_new/bin/activate

                    pytest --junitxml=pytest-report.xml
                    '''
            }
            post {
                always {
                    junit 'app/pytest-report.xml'
                }
            }
        }
    }
}
