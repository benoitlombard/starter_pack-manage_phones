import ruamel.yaml
from manage_phones import yaml_d, yaml, file_name
from error_methods import error_printing
from decorators_file import decorator_timer

# Add phone
def _get_unused_name(yaml_d: dict = yaml_d, call_from_CLI: bool = False)->str:
    """
    Loop through gods in gods.txt file to return the first unused name in 'phones' from gods.txt
    """
    list_of_used_names = []
    for phone_name in yaml_d['phones']:
        list_of_used_names.append(yaml_d['phones'][phone_name]['name'])
    with open('gods.txt', 'r') as gods_txt:
        for god in gods_txt:
            god_name = god.rstrip()
            if god_name not in list_of_used_names:
                unused_name = god_name
                break
    return unused_name

def _get_ip(yaml_d: dict = yaml_d, call_from_CLI: bool = False)->int|None:
    """
    Loop through values from 'rtc_params'['min_ip'], 'rtc_params'['max_ip']\n
    And return the first 3 digits number unused as ip's last triple in 'phones'
    """
    for last_digit_ip in range(yaml_d['rtc_params']['min_ip'], yaml_d['rtc_params']['max_ip']+1):
        found = False
        for phone in yaml_d['phones']:
            if last_digit_ip == int(yaml_d['phones'][phone]['ip'].split('.')[-1]):
                found = True
                break
        if not found :
            return last_digit_ip

@decorator_timer
def add_phone(vendor: str = '', family: str = '', version: str = '', udid: str = '', user: str = '', releasetype: str = '', write: str = True, fota: str = None, activitytracking: str = None,  functional: str = None, performance: str = None, manufacturer: str = None, model: str = None, yaml_d: dict = yaml_d, call_from_CLI: bool = False)->tuple[str,bool]:
    """
    Allows the user to add a new phone by writing phone informations\n
    The informations will be stored in the yaml file
    """
    yaml_phone_name = _get_unused_name(yaml_d, call_from_CLI)
    error_printing('RTC device name: ' + yaml_phone_name, True)
    if not call_from_CLI:
        print('Vendor:')
        vendor = input('? ')
    while vendor == '':
        print('Vendor must be set')
        vendor = input('? ')
    if not call_from_CLI:
        print('Family:')
        family = input('? ')
    while family == '':
        print('Family must be set')
        family = input('? ')
    if not call_from_CLI:
        print('Version:')
        version = input('? ')
    while version == '':
        print('Version must be set')
        version = input('? ')
    if vendor.lower() == 'apple':
        platform = 'ios'
    else:
        platform = 'android'
    error_printing('Platform set to: ' + platform, True)
    if releasetype == '':
        print('Release type:')
        print('1: PU1')
        print('2: PU100')
        ret = input('? ')
    while releasetype == '' and (ret != '1' and ret != '2'):
        print('Please select 1 for PU1 or 2 for PU100')
        ret = input('? ')
    if releasetype == '':
        if ret == '1':
            releasetype = 'PU1'
        elif ret == '2':
            releasetype = 'PU100'
    ip = _get_ip(yaml_d, call_from_CLI)
    if ip is None:
        error_printing("Impossible to add a new phone:\nThere is no ip available at the moment", False)
        return False
    ip = '192.168.5.' + str(ip)
    error_printing('IP used: ' + ip, True)
    if not call_from_CLI:
        print('UDID:')
        udid = input('? ')
    while udid == '':
        print('UDID must be set')
        udid = input('? ')
    for phone in yaml_d['phones']:
        if yaml_d['phones'][phone]['udid'] == udid:
            error_printing("Error when trying to add the phone:\nThis udid has already been used for another phone.", False)
            return False
    user = 'rtc-' + yaml_phone_name + '@cobi.bike'
    """
    New infos in yaml file's 'phone' section: 
        
                            deployed: True/False
                            deployment_path:
                                status: 'dev' / 'prod' / None
                                hub:    str / None
                                port: str / None
    """
    deployed = False #This condition is always verified because of 'print('Phone with ' + udid + ' already exists')' verification
    deployment_path = dict(status = None, hub = None, port = None)

    if call_from_CLI:
        if fota is not None or activitytracking  is not None or functional is not None or performance is not None:
            testrun_ids = dict(fota = fota, activitytracking = activitytracking, functional = functional, performance = performance)
            new_phone_record = ruamel.yaml.CommentedMap(name = yaml_phone_name, manufacturer = manufacturer, model = model, vendor = vendor, family = family, version = version, platform = platform, release_type = releasetype, ip = ip, udid = udid, user = user, deployed = deployed, deployment_path = deployment_path, testrun_ids = testrun_ids)
        else:
            new_phone_record = ruamel.yaml.CommentedMap(name = yaml_phone_name, manufacturer = manufacturer, model = model, vendor = vendor, family = family, version = version, platform = platform, release_type = releasetype, ip = ip, udid = udid, user = user, deployed = deployed, deployment_path = deployment_path)
    else:
        print('Add testrun ids?')
        if input('y|n ').lower() == 'y':
            fota = input('fota: ')
            activitytracking = input('activitytracking: ')
            functional = input('functional: ')
            performance = input('performance: ')
            testrun_ids = dict(fota = fota, activitytracking = activitytracking, functional = functional, performance = performance)
            new_phone_record = ruamel.yaml.CommentedMap(name = yaml_phone_name, manufacturer = manufacturer, model = model, vendor = vendor, family = family, version = version, platform = platform, release_type = releasetype, ip = ip, udid = udid, user = user, deployed = deployed, deployment_path = deployment_path, testrun_ids = testrun_ids)
        else:
            new_phone_record = ruamel.yaml.CommentedMap(name = yaml_phone_name, manufacturer = manufacturer, model = model, vendor = vendor, family = family, version = version, platform = platform, release_type = releasetype, ip = ip, udid = udid, user = user, deployed = deployed, deployment_path = deployment_path)
    new_phone_record.yaml_set_anchor(yaml_phone_name, always_dump=True)

    if write or input('add entry to yaml? y|n ').lower() == 'y':
        yaml_d['phones'][yaml_phone_name] = new_phone_record
        with open(file_name, 'w') as yaml_file:
            yaml.dump(yaml_d, yaml_file)
            error_printing(f"{yaml_phone_name} successfully added.", True)
            return True
        error_printing('Error when writing to the yaml file.', False)
        return False
    error_printing(f"{yaml_phone_name} successfully added, but not saved in yaml file", True)
    return True

