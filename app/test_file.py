from manage_phones_CLI import add, change, deploy, undeploy, remove, show_config, lists, phone_management_app
import pytest

from manage_phones import yaml_d, yaml, file_name

"""
The naming rule for test functions is:   'test_'  +  id(from 001)  +  __  +  function used  +  __  +  important parameters or 'ok' if normal use  +  __  +  asserted features
                            exemples :       
                                            test001__undeploy__ok__yaml_attributes
                                            test002__deploy__ok__yaml_attributes
                                            test003__undeploy__ok__terminal_output
                                            test004__deploy__ok__output
"""

def test_001__undeploy__ok__yaml_attributes():
    exit_code = undeploy(phone = "Chaos")

    hub = yaml_d['phones']['Chaos']['deployment_path']['hub']
    port = yaml_d['phones']['Chaos']['deployment_path']['port']
    assert exit_code == None
    assert hub == None and port == None

def test_002__deploy__ok__yaml_attributes():
    phone, stage = "Chaos", 'dev'
    exit_code = deploy(phone = phone, stage = stage)

    hub = yaml_d['phones'][phone]['deployment_path']['hub']
    port = yaml_d['phones'][phone]['deployment_path']['port']
    assert exit_code == None
    assert hub != None and port != None

    hub_nb = 0
    for hub_number in range(len(yaml_d['stages'][stage])):
        if yaml_d['stages'][stage][hub_number]['name'] == hub:
            hub_nb = hub_number
    deployment_path = yaml_d['stages'][stage][hub_nb][port]
    assert deployment_path == yaml_d['phones'][phone]

def test_003__undeploy__ok__output(capsys):
    undeploy(phone = "Chaos")

    captured = capsys.readouterr()
    assert "Chaos successfully undeployed." in captured.out
    assert "Please unplug Chaos from port01 at hub exsys_ex_1116hmvs_1" in captured.out

def test_004__deploy__ok__output(capsys):
    phone, stage = "Chaos", 'dev'
    deploy(phone = phone, stage = stage)

    captured = capsys.readouterr()
    assert "Chaos successfully deployed in dev." in captured.out

def test_005__deploy__incorrect_stage__yaml_attributes_and_output(capsys):
    phone, stage = "Chaos", 'incorrect_stage'
    undeploy(phone = phone)
    exit_code = deploy(phone = phone, stage = stage)

    hub = yaml_d['phones']['Chaos']['deployment_path']['hub']
    port = yaml_d['phones']['Chaos']['deployment_path']['port']
    assert exit_code == None
    assert hub == None and port == None

    phone_found_in_stages = False
    for stage in ['dev', 'prod']:
        for hub_number in range(len(yaml_d['stages'][stage])):
            for port in yaml_d['stages'][stage][hub_number]:
                if yaml_d['stages'][stage][hub_number][port] == yaml_d['phones'][phone]:
                    phone_found_in_stages = True
    assert not phone_found_in_stages
    captured = capsys.readouterr()
    assert "Please select a stage from" in captured.out

def test_006__deploy__phone_already_deployed__output(capsys):
    phone, stage = "Chaos", "dev"
    deploy(phone = phone, stage = stage)
    deploy(phone = phone, stage = stage)

    captured = capsys.readouterr()
    assert f'{phone} is already deployed.' in captured.out

def test_007__deploy__incorrect_phone_name__output(capsys):
    phone, stage = "incorrect_name", "dev"
    deploy(phone = phone, stage = stage)

    captured = capsys.readouterr()
    assert f'No phone named {phone}.' in captured.out
    print('out:', captured.out)
    print('err:', captured.err)
    assert KeyError in captured.err







#####      TO    BE    DELETED    BUT     NEED    IT    FOR     capsys.readouterr()   ////     captured.err   lecture d erreur
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


