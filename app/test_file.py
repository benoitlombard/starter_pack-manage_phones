from manage_phones_CLI import add, change, deploy, undeploy, remove, show_config, lists, phone_management_app
import pytest
import ruamel.yaml


#######   WILL NEED TO BE IMPORTED   #######

file_name = 'test.yaml'
with open(file_name, 'r') as yaml_file:
    yaml = ruamel.yaml.YAML(typ='rt')
    yaml_d = yaml.load(yaml_file)



def test_001_deploy(capsys):
    exit_code = deploy(phone = "Chaos", stage = 'dev')
    captured = capsys.readouterr()
    print(captured)
    assert exit_code == 8
    return "001 fails"







