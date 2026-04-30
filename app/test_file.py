from manage_phones_CLI import add, change, deploy, undeploy, remove, show_config, lists, phone_management_app
import pytest

from manage_phones import yaml_d, yaml, file_name


"""
The chosen naming rule for test functions is:   'test'  +  id(from 001)  +  __  +  function used  +  __  +  important parameters or 'ok' if normal use  +  __  +  asserted features
                               exemples :       
                                            test001__undeploy__ok__yaml_attributes
                                            test002__deploy__ok__yaml_attributes
                                            test003__undeploy__ok__terminal_output
"""

def test001__undeploy__ok__yaml_attributes():
    exit_code = undeploy(phone = "Chaos")

    hub = yaml_d['phones']['Chaos']['deployment_path']['hub']
    port = yaml_d['phones']['Chaos']['deployment_path']['port']
    assert exit_code == None
    assert hub == None and port == None

def test002__deploy__ok__yaml_attributes():
    exit_code = deploy(phone = "Chaos", stage = 'dev')

    hub = yaml_d['phones']['Chaos']['deployment_path']['hub']
    port = yaml_d['phones']['Chaos']['deployment_path']['port']
    deployment_path = yaml_d['stage']['dev'][hub][port]
    assert exit_code == None
    assert hub != None and port != None
    assert deployment_path == yaml_d['phones']['Chaos']

def test003__undeploy__ok__output(capsys):
    undeploy(phone = "Chaos")

    captured = capsys.readouterr()
    assert "Chaos successfully undeployed." in captured.out
    assert "Please unplug Chaos from port12 at hub tp_link_tlsg3424" in captured.out

def test004__deploy__ok__output(capsys):
    deploy(phone = "Chaos", stage = 'dev')

    captured = capsys.readouterr()
    assert "Chaos successfully deployed in dev." in captured.out




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




