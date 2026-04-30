from manage_phones_CLI import add, change, deploy, undeploy, remove, show_config, lists, phone_management_app
import pytest
import ruamel.yaml



from manage_phones import yaml_d, yaml, file_name




def test001_undeploy_good_infos(capsys):  # verifying deploy 
    exit_code = undeploy(phone = "Chaos")
    hub = yaml_d['phones']['Chaos']['deployment_path']['hub']
    port = yaml_d['phones']['Chaos']['deployment_path']['port']

    captured = capsys.readouterr()
    print(captured.out)

    assert exit_code == None
    assert hub == None and port == None
    assert "Chaos successfully undeployed." in captured.out
    assert "Please unplug Chaos from port12 at hub tp_link_tlsg3424" in captured.out

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




