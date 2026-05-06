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

                    if $run_all_tests; then
                        pytest -m run_all_tests -v
                    fi
                    if $add_a_new_phone; then
                        pytest -m add_a_new_phone
                    fi
                    if $change_existing_phone; then
                        pytest -m change_existing_phone -v
                    fi
                    if $deploy_phone; then
                        pytest -m deploy_phone -v
                    fi
                    if $undeploy_phone; then
                        pytest -m undeploy_phone -v
                    fi
                    if $remove_phone; then
                        pytest -m remove_phone -v
                    fi
                    if $show_phone_configuration; then
                        pytest -m show_phone_configuration -v
                    fi
                    if $display_phones; then
                        pytest -m display_phones -v
                    fi
                    if $display_bts; then
                        pytest -m display_bts -v
                    fi
                    if $display_biabs; then
                        pytest -m display_biabs -v
                    fi
                    if $display_prod_stage; then
                        pytest -m display_prod_stage -v
                    fi
                    if $display_dev_stage; then
                        pytest -m display_dev_stage -v
                    fi
                    if $display_not_deployed_phones; then
                        pytest -m display_not_deployed_phones -v
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
