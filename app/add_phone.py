import ruamel.yaml
from error_methods import send_custom_msg_success_fail
from decorators_file import decorator_timer
from ruamel.yaml.comments import CommentedMap

# Add phone
def _get_unused_name(yaml_d: CommentedMap)->str:
    """
    Loop through gods in gods.txt file to return the first unused name in 'phones' from gods.txt
    """
    with open('gods.txt', 'r') as gods_txt:
        for god in gods_txt:
            god_name = god.rstrip()
            if not yaml_d["phones"]:
                return god_name
            if god_name not in list(yaml_d["phones"].keys()):
                return god_name

def _get_unused_ip(yaml_d: CommentedMap)->int:
    """
    Loop through values from 'rtc_params'['min_ip'], 'rtc_params'['max_ip']\n
    And return the first 3 digits number unused as ip's last triple in 'phones'
    """
    for last_digit_ip in range(yaml_d['rtc_params']['min_ip'], yaml_d['rtc_params']['max_ip']+1):
        found = False
        if not yaml_d["phones"]:
            return last_digit_ip
        for phone in yaml_d['phones']:
            if last_digit_ip == int(yaml_d['phones'][phone]['ip'].split('.')[-1]):
                found = True
                break
        if not found :
            return last_digit_ip

@decorator_timer
def add_phone(yaml_d: CommentedMap, yaml, file_name: str, vendor: str = '', family: str = '', version: str = '', udid: str = '', user: str = '', release_type: str = '', write: str = bool, fota: str = None, activitytracking: str = None,  functional: str = None, performance: str = None, manufacturer: str = None, model: str = None, call_from_CLI: bool = False)->None:
    """
    Allows the user to add a new phone by writing phone information\n
    The information will be stored in the yaml file
    """
    yaml_phone_name = _get_unused_name(yaml_d)
    send_custom_msg_success_fail("RTC device name: " + yaml_phone_name, True)

    while vendor == '':
        print('Vendor must be set')
        vendor = input('? ')

    while family == '':
        print('Family must be set')
        family = input('? ')

    while version == '':
        print('Version must be set')
        version = input('? ')

    platform = "ios" if vendor.lower() == "apple" else "android"
    send_custom_msg_success_fail('Platform set to: ' + platform, True)

    if release_type == '':
        print('Release type:')
        print('1: PU1')
        print('2: PU100')
        ret = input('? ')
        while ret != "1" and ret != "2":
            print('Please select 1 for PU1 or 2 for PU100')
            ret = input('? ')

        release_type = "PU1" if ret == "1" else "PU100"

    ip = _get_unused_ip(yaml_d)
    if ip is None:
        send_custom_msg_success_fail("Impossible to add a new phone:\nThere is no ip available at the moment", False)
        return
    ip = '192.168.5.' + str(ip)
    send_custom_msg_success_fail('IP used: ' + ip, True)

    while udid == '':
        print('UDID must be set')
        udid = input('? ')

    while True:
        if not yaml_d["phones"]:
            break
        for phone in yaml_d['phones']:
            if yaml_d['phones'][phone]['udid'] == udid:
                send_custom_msg_success_fail(f"Error when trying to add the phone:\nThis udid has already been used for phone '{phone}'.", False)
                print(f"Select new udid different than {udid}")
                udid = input('? ')
                break
        else:
            break

    user = 'rtc-' + yaml_phone_name + '@cobi.bike'

    deployment_path = dict(hub = None, port = None)

    if call_from_CLI:
        if fota is not None or activitytracking  is not None or functional is not None or performance is not None:
            testrun_ids = dict(fota = fota, activitytracking = activitytracking, functional = functional, performance = performance)
            new_phone_record = ruamel.yaml.CommentedMap(name = yaml_phone_name, manufacturer = manufacturer, model = model, vendor = vendor, family = family, version = version, platform = platform, release_type = release_type, ip = ip, udid = udid, user = user, deployment_path = deployment_path, testrun_ids = testrun_ids)
        else:
            new_phone_record = ruamel.yaml.CommentedMap(name = yaml_phone_name, manufacturer = manufacturer, model = model, vendor = vendor, family = family, version = version, platform = platform, release_type = release_type, ip = ip, udid = udid, user = user, deployment_path = deployment_path)
    else:
        print('Add testrun ids?')
        if input('y|n ').lower() == 'y':
            fota = input('fota: ')
            activitytracking = input('activitytracking: ')
            functional = input('functional: ')
            performance = input('performance: ')
            testrun_ids = dict(fota = fota, activitytracking = activitytracking, functional = functional, performance = performance)
            new_phone_record = ruamel.yaml.CommentedMap(name = yaml_phone_name, manufacturer = manufacturer, model = model, vendor = vendor, family = family, version = version, platform = platform, release_type = release_type, ip = ip, udid = udid, user = user, deployment_path = deployment_path, testrun_ids = testrun_ids)
        else:
            new_phone_record = ruamel.yaml.CommentedMap(name = yaml_phone_name, manufacturer = manufacturer, model = model, vendor = vendor, family = family, version = version, platform = platform, release_type = release_type, ip = ip, udid = udid, user = user, deployment_path = deployment_path)

    new_phone_record.yaml_set_anchor(yaml_phone_name, always_dump=True)

    if write or input('add entry to yaml? y|n ').lower() == 'y':
        if yaml_d["phones"] is None:
            yaml_d["phones"] = ruamel.yaml.CommentedMap()

        yaml_d['phones'][yaml_phone_name] = new_phone_record
        with open(file_name, 'w') as yaml_file:
            yaml.dump(yaml_d, yaml_file)
            send_custom_msg_success_fail(f"{yaml_phone_name} successfully added.", True)
            return

        # Does this is executed? Try except
        send_custom_msg_success_fail('Error when writing to the yaml file.', False)
        return

    send_custom_msg_success_fail(f"{yaml_phone_name} successfully added, but not saved in yaml file", True)
