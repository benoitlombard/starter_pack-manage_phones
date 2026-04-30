from manage_phones_CLI import add, change, deploy, undeploy, remove, show_config, lists, phone_management_app
import pytest
import ruamel.yaml


#######   WILL NEED TO BE IMPORTED   #######

file_name = 'test.yaml'
with open(file_name, 'r') as yaml_file:
    yaml = ruamel.yaml.YAML(typ='rt')
    yaml_d = yaml.load(yaml_file)



def test_001_deploy():  # verifying deploy 
    exit_code = deploy(phone = "Chaos", stage = 'dev')
    assert exit_code == None






# test cqtching err
def test_002_deploy(capsys):                                            ###### !!!
    exit_code = deploy(phone = "wrong_phone_name", stage = 'dev')
    captured = capsys.readouterr()
    print(captured)
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


test_001_deploy()




