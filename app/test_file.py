from manage_phones_CLI import add, change, deploy, undeploy, remove, show_config, lists, phone_management_app
import pytest
import ruamel.yaml


#######   MAY NEED TO BE IMPORTED   #######
file_name = 'test.yaml'
with open(file_name, 'r') as yaml_file:
    yaml = ruamel.yaml.YAML(typ='rt')
    yaml_d = yaml.load(yaml_file)
###########################################






def test001_undeploy_good_infos(capsys):  # verifying deploy 
    exit_code = undeploy(phone = "Chaos")
    hub = yaml_d['phones']['Chaos']['deployment_path']['hub']
    port = yaml_d['phones']['Chaos']['deployment_path']['port']

    captured = capsys.readouterr()
    print(captured.out)

    assert exit_code == None and hub == None and port == None

def test002_deploy_good_infos():  # verifying deploy 
    exit_code = deploy(phone = "Chaos", stage = 'dev')
    assert exit_code == None






def greet(name):
    print(f"Hello, {name}!")

def test_greet_output(capsys):
    # Call the function that prints
    greet("Alice")

    # Capture the output
    captured = capsys.readouterr()

    # Assert on stdout
    assert captured.out == "Hello, Alice!\n"
    # Assert stderr if needed
    assert captured.err == ""




