from manage_phones_CLI import add, change, deploy, undeploy, remove, show_config, lists
import pytest
import sys

from manage_phones import yaml_d, yaml, file_name

""" The naming rule for test functions is:   'test_'  +  id(from 001)  +  __  +  function used  +  __  +  important parameters or 'ok' if normal use  +  __  +  asserted features
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

def test_007__deploy__incorrect_phone_name__output_and_error(capsys):
    phone, stage = "incorrect_name", "dev"

    with pytest.raises(KeyError):
        deploy(phone = phone, stage = stage)
    captured = capsys.readouterr()
    assert f'No phone named {phone}.' in captured.out

def test_008__undeploy__incorrect_phone_name__output_and_error(capsys):
    phone = "incorrect_name"

    with pytest.raises(KeyError):
        undeploy(phone = phone)
    captured = capsys.readouterr()
    assert "Key Error when writing to the yaml file.\nUndeployment failed, please verify phone name." in captured.out

def test_009__undeploy__not_deployed_phone__output(capsys):
    phone = "Hesperiden"
    undeploy(phone = phone)

    captured = capsys.readouterr()
    assert f"{phone} is not deployed.\nUndeployment is not possible." in captured.out

def test_010__add__ok_minimal_infos__output(capsys):
    vendor = 'apple'
    family = 'ios4'
    version = '5.6'
    udid = 'udid_1'
    release_type = 'PU100'
    add(vendor = vendor, family = family, version = version, udid = udid, release_type = release_type)

    captured = capsys.readouterr()
    assert "RTC device name: " in captured.out
    assert "Platform set to: " in captured.out
    assert "IP used: " in captured.out
    assert " successfully added." in captured.out

def test_011__add__ok_minimal_infos__yaml_attributes():
    vendor = 'apple'
    family = 'ios4'
    version = '5.6'
    udid = 'udid_2'
    release_type = 'PU100'
    add(vendor = vendor, family = family, version = version, udid = udid, release_type = release_type)

    dict_attributes_found_in_yaml = {'vendor': None, 'family': None, 'version': None, 'udid': None, 'release_type': None}
    for phone in yaml_d['phones']:
        if yaml_d['phones'][phone]['udid'] == udid:
            for attribute_key in dict_attributes_found_in_yaml.keys():
                dict_attributes_found_in_yaml[attribute_key] = yaml_d['phones'][phone][attribute_key]
    
    dict_attributes = {'vendor': vendor, 'family': family, 'version': version, 'udid': udid, 'release_type': release_type}
    for key, value_found_in_yaml in dict_attributes_found_in_yaml.items():
        assert value_found_in_yaml == dict_attributes[key]

def test_012__add__ok_with_testrun_ids__output(capsys):
    vendor = 'apple'
    family = 'ios4'
    version = '5.6'
    udid = 'udid_3'
    release_type = 'PU100'
    fota = 'fota_id'
    activitytracking = '3a4-e1c'
    functional = '65'
    performance = '124'
    add(vendor = vendor, family = family, version = version, udid = udid, release_type = release_type, fota = fota, activitytracking = activitytracking, functional = functional, performance = performance)

    captured = capsys.readouterr()
    assert "RTC device name: " in captured.out
    assert "Platform set to: " in captured.out
    assert "IP used: " in captured.out
    assert " successfully added." in captured.out

def test_013__add__ok_testrun_ids__yaml_attributes():
    vendor = 'apple'
    family = 'ios4'
    version = '5.6'
    udid = 'udid_4'
    release_type = 'PU100'
    fota = 'fota_id'
    activitytracking = 'activitytracking_id'
    functional = '65'
    performance = '124'
    add(vendor = vendor, family = family, version = version, udid = udid, release_type = release_type, fota = fota, activitytracking = activitytracking, functional = functional, performance = performance)

    dict_attributes_found_in_yaml = {'vendor': None, 'family': None, 'version': None, 'udid': None, 'release_type': None, 'fota': None, 'activitytracking': None, 'functional': None, 'performance': None}
    for phone in yaml_d['phones']:
        if yaml_d['phones'][phone]['udid'] == udid:
            print('trouve', yaml_d['phones'][phone])
            for attribute_key in ['vendor', 'family', 'version', 'udid', 'release_type']:
                dict_attributes_found_in_yaml[attribute_key] = yaml_d['phones'][phone][attribute_key]
            for attribute_key in ['fota', 'activitytracking', 'functional', 'performance']:
                dict_attributes_found_in_yaml[attribute_key] = yaml_d['phones'][phone]['testrun_ids'][attribute_key]
    
    dict_attributes = {'vendor': vendor, 'family': family, 'version': version, 'udid': udid, 'release_type': release_type, 'fota': fota, 'activitytracking': activitytracking, 'functional': functional, 'performance': performance}
    for key, value_found_in_yaml in dict_attributes_found_in_yaml.items():
        assert value_found_in_yaml == dict_attributes[key]


def _asserting_phone_informations_in_stdout(captured, phone: str):
    assert f"name: {phone}" in captured.out
    if 'testrun_ids' in yaml_d['phones'][phone]:
        list_of_attributes = {'release_type', 'user', 'fota', 'activitytracking', 'functional', 'performance', 'manufacturer',
                                'model', 'vendor','family','version', 'platform', 'ip', 'udid', 'hub', 'port'}
    else:
        list_of_attributes = {'release_type', 'user', 'manufacturer', 'model', 'vendor','family','version', 'platform', 'ip', 'udid', 'hub', 'port'}
    for attribute_key in list_of_attributes:
        if attribute_key in ['fota', 'activitytracking', 'functional', 'performance']:
            if yaml_d['phones'][phone]['testrun_ids'][attribute_key] is None:
                assert f"{attribute_key}:"
            else:
                if f"{attribute_key}: {yaml_d['phones'][phone]['testrun_ids'][attribute_key]}" in captured.out:
                    assert f"{attribute_key}: {yaml_d['phones'][phone]['testrun_ids'][attribute_key]}" in captured.out
                else:
                    assert f"{attribute_key}: '{yaml_d['phones'][phone]['testrun_ids'][attribute_key]}'" in captured.out

        elif attribute_key in ['hub', 'port']:
            if yaml_d['phones'][phone]['deployment_path'][attribute_key] is None:
                assert f"{attribute_key}:"
            else:
                if f"{attribute_key}: {yaml_d['phones'][phone]['deployment_path'][attribute_key]}" in captured.out:
                    assert f"{attribute_key}: {yaml_d['phones'][phone]['deployment_path'][attribute_key]}" in captured.out
                else:
                    assert f"{attribute_key}: '{yaml_d['phones'][phone]['deployment_path'][attribute_key]}'" in captured.out

        else:
            if yaml_d['phones'][phone][attribute_key] is None:
                assert f"{attribute_key}:"
            else:
                if f"{attribute_key}: {yaml_d['phones'][phone][attribute_key]}" in captured.out:
                    assert f"{attribute_key}: {yaml_d['phones'][phone][attribute_key]}" in captured.out
                else:
                    assert f"{attribute_key}: '{yaml_d['phones'][phone][attribute_key]}'" in captured.out

@pytest.mark.deploy_phone
@pytest.mark.parametrize("phone,stage", [("Hemera", "dev"), ("Chaos", "dev"), ("incorrect_phone", "dev"), ("Nyx", "incorrect_stage"), ("Nyx", "dev"), ("Nyx", "prod"), ("incorrect_phone", "incorrect_stage")])
def test_deploy_phone(capsys, phone: str, stage: str):

    if phone not in yaml_d['phones'] and stage in ['dev', 'prod']:                   # case: incorrect phone name
        with pytest.raises(KeyError):
            deploy(phone = phone, stage = stage)
        captured = capsys.readouterr()
        assert f'No phone named {phone}.' in captured.out

    else:
        deploy(phone = phone, stage = stage)
        captured = capsys.readouterr()
        if stage not in ['dev', 'prod']:                    # case: incorrect stage 
            assert "Please select a stage from" in captured.out
            return
        
        is_a_port_available = False
        for hub in yaml_d["stages"][stage]:
            for port, value in hub.items():
                if port.startswith("port") and value is None:
                    is_a_port_available = True

        if not is_a_port_available:                          # case: no port available
            assert f"Error when trying to find a free port:\nNo free port available in stage '{stage}'." in captured.out
            return

        elif yaml_d['phones'][phone]["deployment_path"]["hub"] is not None:
            assert f'{phone} is already deployed.' in captured.out
            return
        
        else:
            assert f'{phone} successfully deployed in {stage}.' in captured.out
            assert yaml_d['phones'][phone]["deployment_path"]["hub"] is not None
            assert yaml_d['phones'][phone]["deployment_path"]["port"] == port

            used_hub, used_port = None, None
            for hub_number in range(len(yaml_d['stages'][stage])):
                for port in yaml_d['stages'][stage][hub_number]:
                    if yaml_d['stages'][stage][hub_number][port] == yaml_d['phones'][phone]:   #changer
                        used_hub, used_port = hub_number, port

            assert used_hub is not None
            assert used_port is not None
            assert yaml_d['phones'][phone]['deployment_path']['hub'] == yaml_d['stages'][stage][hub_number]['name']
            assert yaml_d['phones'][phone]['deployment_path']['port'] != None

@pytest.mark.undeploy_phone
@pytest.mark.parametrize("phone", [("Hemera"), ("Chaos"), ("Chaos"), ("incorrect_phone")]) # Chaos appear 2 times for testing case where phone is not deployed
def test_undeploy_phone(capsys, phone: str):
    if phone not in yaml_d['phones']:                   # case: incorrect phone name
        with pytest.raises(KeyError):
            undeploy(phone = phone)
        captured = capsys.readouterr()
        assert "Key Error when writing to the yaml file.\nUndeployment failed, please verify phone name." in captured.out
    else:
        phone_deployment_hub = yaml_d['phones'][phone]['deployment_path']['hub']
        phone_deployment_port = yaml_d['phones'][phone]['deployment_path']['port']
        undeploy(phone = phone)
        captured = capsys.readouterr()
        if phone_deployment_hub is None:
            assert phone_deployment_port is None
            assert f"{phone} is not deployed.\nUndeployment is not possible." in captured.out
        else:
            assert f"{phone} successfully undeployed." in captured.out
            assert f'Please unplug {phone} from' in captured.out
            assert yaml_d['phones'][phone]['deployment_path']['hub'] == None
            assert yaml_d['phones'][phone]['deployment_path']['port'] == None
            for stage in yaml_d['stages']:
                for hub_number in range(len(yaml_d['stages'][stage])):
                    if yaml_d['stages'][stage][hub_number]['name'] == phone_deployment_hub:
                        if phone_deployment_port in yaml_d['stages'][stage][hub_number]:
                            assert yaml_d['stages'][stage][hub_number][phone_deployment_port] is None

@pytest.mark.remove_phone
@pytest.mark.parametrize("phone", [("Hemera"), ("Chaos"), ("incorrect_phone")])
def test_remove_phone(capsys, phone: str):
    phone_is_in_yaml = True if phone in yaml_d['phones'] else False
    if not phone_is_in_yaml:
        remove(phone = phone)
        captured = capsys.readouterr()
        assert f"Error: phone '{phone}' not found." in captured.out
    else:
        phone_deployment_hub = yaml_d['phones'][phone]['deployment_path']['hub']
        phone_deployment_port = yaml_d['phones'][phone]['deployment_path']['port']
        remove(phone = phone)
        captured = capsys.readouterr()
        for stage in yaml_d['stages']:
            for hub_number in range(len(yaml_d['stages'][stage])):
                if yaml_d['stages'][stage][hub_number]['name'] == phone_deployment_hub:
                    if phone_deployment_port in yaml_d['stages'][stage][hub_number]:
                        assert yaml_d['stages'][stage][hub_number][phone_deployment_port] is None
                            
            assert f'{phone} successfully removed.' in captured.out
        
@pytest.mark.change_existing_phone
@pytest.mark.parametrize("phone,release_type,user,fota,functional,activitytracking," \
                        "performance,manufacturer,model,vendor,family,version,platform," \
                        "ip,udid,hub,port", [("Hemera", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""),
                                             ("Chaos", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""),
                                             ("Chaos", "PU100", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""),
                                             ("Chaos", "PU1", "jean", "", "", "", "", "", "", "", "", "", "", "", "", "", ""),
                                             ("Chaos", "", "", "fota_id", "", "", "", "", "", "", "", "", "", "", "", "", ""),
                                             ("Chaos", "PU100", "", "fota_id", "1", "2", "3", "", "", "", "", "", "", "", "", "", ""),
                                             ("Chaos", "", "john", "fota_id", "", "", "", "Samsung", "", "", "", "", "", "", "udid_test", "", ""),
                                             ("Chaos", "whatever", "john", "fota_id", "", "", "", "Samsung", "", "whatever", "", "", "whatever", "", "udid_test", "", ""),
                                             ("Chaos", "", "whatever", "", "", "", "", "", "", "", "", "", "", "", "", "new_hub", "new_port"),
                                             ("Nyx", "", "whatever", "", "", "", "", "", "", "", "", "", "", "", "", "new_hub", "new_port"),
                                             ("Hemera", "", "whatever", "", "", "", "", "", "", "", "", "", "", "", "", "new_hub", "new_port"),
                                             ("incorrect_phone", "whatever", "john", "fota_id", "", "", "", "Samsung", "", "whatever", "", "", "whatever", "", "udid_test", "", ""),
                                             ("incorrect_phone", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""),
                                             ("incorrect_phone", "", "whatever", "", "", "", "", "", "", "", "", "", "", "", "", "", ""),
                                             ("incorrect_phone", "", "whatever", "", "", "", "", "", "", "", "", "", "", "", "", "new_hub", "new_port"),
                                             ("incorrect_phone", "whatever", "john", "fota_id", "whatever", "whatever", "", "Samsung", "", "whatever", "whatever", "whatever", "whatever", "", "udid_test", "", "")])
def test_change_phone(capsys, phone: str, release_type: str, user: str, fota: str, activitytracking: str,
           functional: str, performance: str, manufacturer: str, model: str,
           vendor: str, family: str, version: str, platform: str, ip: str,
           udid: str, hub: str, port: str):
    if all(attribute == '' for attribute in [release_type, user, fota, activitytracking, functional, performance, manufacturer, model, vendor, family, version, platform, ip, udid, hub, port]):
        change(phone = phone, release_type = release_type, user = user,
            fota = fota, functional = functional, activitytracking = activitytracking, performance = performance,
            manufacturer = manufacturer, model = model, vendor = vendor, family = family, version = version,
            platform = platform, ip = ip, udid = udid, hub = hub, port = port)
        captured = capsys.readouterr()
        assert 'No values to change !' in captured.out
    elif phone not in yaml_d['phones']:                   # case: incorrect phone name
        with pytest.raises(KeyError):
            change(phone = phone, release_type = release_type, user = user,
            fota = fota, functional = functional, activitytracking = activitytracking, performance = performance,
            manufacturer = manufacturer, model = model, vendor = vendor, family = family, version = version,
            platform = platform, ip = ip, udid = udid, hub = hub, port = port)
        captured = capsys.readouterr()
        assert f"Phone {phone} not found." in captured.out
    else:
        change(phone = phone, release_type = release_type, user = user,
            fota = fota, functional = functional, activitytracking = activitytracking, performance = performance,
            manufacturer = manufacturer, model = model, vendor = vendor, family = family, version = version,
            platform = platform, ip = ip, udid = udid, hub = hub, port = port)
        captured = capsys.readouterr()
        assert f"{phone} successfully changed." in captured.out

        dict_of_attributes = {'release_type':release_type, 'user':user, 'fota':fota, 'activitytracking':activitytracking,
                          'functional':functional, 'performance':performance, 'manufacturer':manufacturer, 'model':model, 'vendor':vendor,
                          'family':family,'version':version, 'platform':platform, 'ip':ip, 'udid':udid, 'hub':hub, 'port':port}
        for attribute_key, attribute_value in dict_of_attributes.items():
            if attribute_value != "":
                if attribute_key in ['fota', 'activitytracking', 'functional', 'performance']:
                    assert yaml_d['phones'][phone]['testrun_ids'][attribute_key] == attribute_value
                elif attribute_key in ['hub', 'port']:
                    assert yaml_d['phones'][phone]['deployment_path'][attribute_key] == attribute_value
                else:
                    assert yaml_d['phones'][phone][attribute_key] == attribute_value


@pytest.mark.add_a_new_phone
@pytest.mark.parametrize("vendor,family,version,udid,user,release_type,write,fota,activitytracking,functional,performance,manufacturer,model",
                         [("apple", "ios3", "4.2", "unique_udid_1", "user_n", "PU1", True, "", "", "", "", "", ""),                                                         # case: minimalist attributes and release_type overwritten
                          ("apple", "ios3", "4.2", "unique_udid_2", "user_n", "PU1", True, "", "", "", "", "", ""),                                                            # case: minimalist attributes and release_type default value
                          ("apple", "ios3", "4.2", "unique_udid_3", "user_n", "PU1", False, "", "", "", "", "", ""),                                                                # not saving phone to yaml
                          ("apple", "ios3", "4.2", "unique_udid_5", "user_n", "PU100", True, "", "", "", "", "apple", "model_2"),
                          ("samsung", "SS4", "17", "unique_udid_6", "user_n", "PU100", True, "fota_id", "activitytracking_id", "functional_id", "", "", ""),
                          ("apple", "ios3", "4.2", "unique_udid_7", "user_n", "PU1", True, "fota_id", "activitytracking_id", "functional_id", "performance_id", "", ""),
                          ("apple", "ios3", "4.2", "unique_udid_8", "user_n", "PU1", True, "fota_id", "activitytracking_id", "functional_id", "performance_id", "apple", "model_2"),
                          ("apple", "ios3", "4.2", "unique_udid_8", "user_n", "PU1", True, "fota_id", "", "", "", "", ""),                                          # case : udid already used
                          ("apple", "ios3", "4.2", "unique_udid_9", "user_n", "PU1", False, "fota_id", "", "", "", "", ""),
                          ("apple", "ios3", "4.2", "unique_udid_10", "user_n", "PU1", False, "fota_id", "", "", "", "", "model_n"),
                          ("apple", "ios3", "4.2", "unique_udid_11", "user_n", "PU1", False, "fota_id", "", "", "", "", ""),
                          ("samsung", "SG8", "20", "unique_udid_12", "user_n", "PU1", True, "fota_id", "", "", "", "", "model_2")])                      # case: not enough ips available
def test_add_phone(capsys, vendor: str, family: str, version: str, udid: str, user: str, release_type: str, write: bool, fota: str,
                   activitytracking: str, functional: str, performance: str, manufacturer: str, model: str):
    is_udid_used = False
    for phone in yaml_d['phones']:
        if yaml_d['phones'][phone]['udid'] == udid:
            is_udid_used = True
            break
    add(vendor = vendor, family = family, version = version, udid = udid, user = user, release_type = release_type, write = write, fota = fota,
        activitytracking = activitytracking, functional = functional, performance = performance, manufacturer = manufacturer, model = model)
    
    captured = capsys.readouterr()
    assert "RTC device name: " in captured.out
    if vendor.lower() == "apple":
        assert 'Platform set to: ios' in captured.out
    else:
        assert 'Platform set to: android' in captured.out
    last_digit_ip_chosen = None
    for last_digit_ip in range(yaml_d['rtc_params']['min_ip'], yaml_d['rtc_params']['max_ip']+1):
        found = False
        if not yaml_d["phones"]:
            return last_digit_ip
        for phone in yaml_d['phones']:
            if last_digit_ip == int(yaml_d['phones'][phone]['ip'].split('.')[-1]):
                found = True
                break
        if not found:
            last_digit_ip_chosen = last_digit_ip
            break
    if last_digit_ip_chosen is None:
        assert "Impossible to add a new phone:\nThere is no ip available at the moment" in captured.out
    else:
        assert 'IP used: 192.168.5.' in captured.out
        if is_udid_used:
            assert "Error when trying to add the phone:\nThis udid has already been used for phone " in captured.out
        elif write:
            assert "successfully added." in captured.out

            phone_name = None
            for phone in yaml_d['phones']:
                    if yaml_d['phones'][phone]['udid'] == udid:
                        phone_name = phone
                        break
            if any in [fota, activitytracking, functional, performance] is not None:
                dict_of_attributes = {'release_type':release_type, 'fota':fota, 'activitytracking':activitytracking,
                            'functional':functional, 'performance':performance, 'manufacturer':manufacturer, 'model':model, 'vendor':vendor,
                            'family':family, 'version':version, 'udid':udid}
            else:
                dict_of_attributes = {'release_type':release_type, 'fota':fota, 'activitytracking':activitytracking,
                            'functional':functional, 'performance':performance, 'manufacturer':manufacturer, 'model':model, 'vendor':vendor,
                            'family':family, 'version':version, 'udid':udid}
            for attribute_key, attribute_value in dict_of_attributes.items():
                if attribute_key in ['fota', 'activitytracking', 'functional', 'performance']:
                    assert yaml_d['phones'][phone_name]['testrun_ids'][attribute_key] == attribute_value
                elif attribute_key in ['hub', 'port']:
                    assert yaml_d['phones'][phone_name]['deployment_path'][attribute_key] == attribute_value
                else:
                    assert yaml_d['phones'][phone_name][attribute_key] == attribute_value
        else:
            assert "successfully added, but not saved in yaml file" in captured.out

@pytest.mark.show_phone_configuration
@pytest.mark.parametrize("phone", [("Nyx"), ("Chaos"), ("incorrect_phone")])
def test_show_config(capsys, phone: str):
    show_config(phone = phone)
    captured = capsys.readouterr()
    if phone not in yaml_d['phones']:                   # case: incorrect phone name
        assert f'{phone} not found.' in captured.out
    else:
        _asserting_phone_informations_in_stdout(captured, phone)


@pytest.mark.display
@pytest.mark.parametrize("item_to_show,stage_to_show", [("incorrect_item", ""), ("incorrect_item", "incorrect_stage"),("phones", "incorrect_stage"),
                                        ("phones", ""), ("bts", ""), ("biab", ""), ("stage", "dev"), ("stage", "prod"), ("undeployed_phones", ""),
                                        ("phones", "incorrect_stage"), ("bts", "incorrect_stage"), ("biab", "incorrect_stage"), ("stage", "incorrect_stage"),
                                        ("stage", "incorrect_stage"), ("undeployed_phones", "incorrect_stage")])
def test_lists_phones(capsys, item_to_show: str, stage_to_show: str):
    match item_to_show.lower():
        case 'stage':
            if stage_to_show not in yaml_d['stages']:                   # case: incorrect phone name
                with pytest.raises(KeyError):
                    lists(item_to_show = item_to_show, stage_to_show = stage_to_show)
                captured = capsys.readouterr()
                assert "KeyError: makes sure 'stage' value is either 'dev' or 'prod'." in captured.out
            else:
                lists(item_to_show = item_to_show, stage_to_show = stage_to_show)
                captured = capsys.readouterr()

        case 'phones':
            lists(item_to_show = item_to_show, stage_to_show = stage_to_show)
            captured = capsys.readouterr()
            for phone in yaml_d['phones']:
                _asserting_phone_informations_in_stdout(captured, phone)

        case 'bts' | 'biab':
            pass

        case 'undeployed_phones':
            lists(item_to_show = item_to_show, stage_to_show = stage_to_show)
            captured = capsys.readouterr()
            for phone in yaml_d['phones']:
                if yaml_d['phones'][phone]['deployment_path']['hub'] is None:
                    _asserting_phone_informations_in_stdout(captured, phone)



    
    