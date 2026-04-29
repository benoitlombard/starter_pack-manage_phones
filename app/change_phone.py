import sys
from error_methods import send_custom_msg_success_fail
from decorators_file import decorator_timer
from ruamel.yaml.comments import CommentedMap

# change phone
@decorator_timer
def change_phone(yaml_d: CommentedMap, yaml, **kwargs)->None:
    """
    Allows user to change some information from 'phones' data by asking which phone and what value of attribute he want to change
    """
    file_name = kwargs['file_name']

    new_data = {}
    keys = ['phone', 'release_type', 'user', 'fota', 'activitytracking', 'functional', 'performance', 'manufacturer', 'model', 'vendor', 'family', 'version', 'platform', 'ip', 'udid', 'hub', 'port', 'call_from_CLI']
    for key in keys:
        new_data[key] = kwargs[key] if kwargs.get(key) else ''

    cli = new_data['call_from_CLI']
    while new_data['phone'] == '':
        dict_of_phones: list = []
        print('Phone to change: ')
        for phone_index, phone in  enumerate(yaml_d['phones']):
            dict_of_phones.append(yaml_d['phones'][phone]['name'])
            print(str(phone_index) + ': ' + yaml_d['phones'][phone]['name'])
            print('\t' + yaml_d['phones'][phone]['vendor'] + ' ' + yaml_d['phones'][phone]['family'] + ' ' + str(yaml_d['phones'][phone]['version']))
        indx = input('? ')
        try:
            new_data['phone'] = dict_of_phones[int(indx)]
        except ValueError as err:
            send_custom_msg_success_fail("ValueError: User input do not match selection.", False)
            if cli:
                raise err
            return
        except KeyError as err:
            send_custom_msg_success_fail("KeyError: User input do not match selection.", False)
            if cli:
                raise err
            return

    if cli:
        try:
            for attribute in ['release_type', 'user', 'manufacturer', 'model', 'vendor', 'family', 'version', 'platform', 'ip', 'udid']:
                yaml_d['phones'][new_data['phone']][attribute] = new_data[attribute] if new_data[attribute] != '' else yaml_d['phones'][new_data['phone']][attribute]
            if new_data['hub'] != '' or new_data['port'] != '':
                for deployment_path_attribute in ['hub', 'port']:
                    yaml_d['phones'][new_data['phone']]['deployment_path'][deployment_path_attribute] = new_data[deployment_path_attribute] if new_data[deployment_path_attribute] != '' else yaml_d['phones'][new_data['phone']]['deployment_path'][deployment_path_attribute]
        except KeyError as err:
            send_custom_msg_success_fail(f"Phone {new_data['phone']} not found.", False)
            if cli:
                raise err
            return

        testrun_keys = ("fota", "activitytracking", "functional", "performance")
        updates = {key: new_data[key] for key in testrun_keys if new_data[key] != ""}
        if updates:
            yaml_d["phones"][new_data["phone"]].setdefault("testrun_ids", {})
            yaml_d["phones"][new_data["phone"]]["testrun_ids"].update(updates)

    else:
        yaml.dump(new_data['phone'], sys.stdout)
        print('What to change')
        print('1: Release type')
        print('2: User')
        print('3: Testrun id\'s')
        ret = input('? ')
        if ret == '1':
            print('Release type:')
            print('1: PU1')
            print('2: PU100')
            ret = input('? ')
            while ret != '1' and ret != '2':
                print('Please select a for PU1 or b for PU100')
                ret = input('? ')
            release_type = "PU1" if ret == "1" else "PU100"
            yaml_d['phones'][new_data['phone']]['release_type'] = release_type

        elif ret == '2':
            print('New user: (complete string)')
            user = input('? ')
            yaml_d['phones'][new_data['phone']]['user'] = user

        elif ret == '3':
            new_data['fota'] = input('fota: ')
            new_data['activitytracking'] = input('activitytracking: ')
            new_data['functional'] = input('functional: ')
            new_data['performance'] = input('performance: ')

            testrun_ids = dict(fota = new_data['fota'], activitytracking = new_data['activitytracking'],
                               functional = new_data['functional'], performance = new_data['performance'])

            yaml_d['phones'][new_data['phone']]['testrun_ids'] = testrun_ids

        else:
            send_custom_msg_success_fail("KeyError: User input do not match selection.", False)
            return

    with open(file_name, 'w') as w:
        yaml.dump(yaml_d, w)
        send_custom_msg_success_fail(f"{new_data['phone']} successfully changed.", True)
        return
