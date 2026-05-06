pipeline {
    agent any
    parameters {
        booleanParam(name: 'run_all_tests', defaultValue: true, description: '   Other parameters will be ignored if this parameter is checked.')
        string(name: 'COMMANDS', defaultValue: 'python manage_phones_CLI.py change --phone Chaos --release-type PU100 --user jean, ', description: '   Additional commands to execute (separator = ",")')
        booleanParam(name: 'add_a_new_phone', defaultValue: false, description: '')
        booleanParam(name: 'change_existing_phone', defaultValue: false, description: '')
        booleanParam(name: 'deploy_phone', defaultValue: false, description: '')
        booleanParam(name: 'undeploy_phone', defaultValue: false, description: '')
        booleanParam(name: 'remove_phone', defaultValue: false, description: '')
        booleanParam(name: 'show_phone_configuration', defaultValue: false, description: '')
        booleanParam(name: 'display_phones', defaultValue: false, description: '')
        booleanParam(name: 'display_bts', defaultValue: false, description: '')
        booleanParam(name: 'display_biabs', defaultValue: false, description: '')
        booleanParam(name: 'display_prod_stage', defaultValue: false, description: '')
        booleanParam(name: 'display_dev_stage', defaultValue: false, description: '')
        booleanParam(name: 'display_not_deployed_phones', defaultValue: false, description: '')

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
                    cd app
                    . venv_new/bin/activate

                    echo "AVANT CONDITION 1"
                    if $add_a_new_phone || $run_all_tests; then
                        pytest -m add_a_new_phone
                    fi

                    echo "ENTRE LES CONDITIONS"
                    if $deploy_phone || $run_all_tests; then
                        pytest -m deploy_phone -v
                    fi






                    echo "ON EST GOOD"
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
