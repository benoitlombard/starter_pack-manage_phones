import sys
from manage_phones import yaml, file_name
from error_methods import error_printing
from decorators_file import decorator_timer

# change phone
@decorator_timer
def change_phone(*args, **kwargs)->None:
    """
    Allows user to change some information from 'phones' data by asking which phone and what value of attribute he want to change
    """
    yaml_d = kwargs['yaml_d'] # unpacking yaml_d to handle recently created phones
    new_data = {}
    keys = ['phone', 'release_type', 'user', 'fota', 'activitytracking', 'functional', 'performance', 'manufacturer', 'model', 'vendor', 'family', 'version', 'platform', 'ip', 'udid', 'deployed', 'status', 'hub', 'port', 'yaml_d', 'call_from_CLI']
    for key in keys:
        new_data[key] = kwargs[key] if kwargs.get(key) else ''

    while new_data['phone'] == '':
        dict_of_phones = {}
        print('Phone to change: ')
        for phone_index, phone in  enumerate(yaml_d['phones']):
            dict_of_phones[phone_index] = yaml_d['phones'][phone]['name']
            print(str(phone_index) + ': ' + yaml_d['phones'][phone]['name'])
            print('\t' + yaml_d['phones'][phone]['vendor'] + ' ' + yaml_d['phones'][phone]['family'] + ' ' + str(yaml_d['phones'][phone]['version']))
        indx = input('? ')
        try:
            new_data['phone'] = dict_of_phones[int(indx)]
        except ValueError as err:
            error_printing("ValueError: User input do not match selection.", False)
            if new_data['call_from_CLI']:
                raise err
            return
        except KeyError as err:
            error_printing("KeyError: User input do not match selection.", False)
            if new_data['call_from_CLI']:
                raise err
            return
    if new_data['call_from_CLI']:
        try:
            for attribute in ['release_type', 'user', 'manufacturer', 'model', 'vendor', 'family', 'version', 'platform', 'ip', 'udid', 'deployed']:
                yaml_d['phones'][new_data['phone']][attribute] = new_data[attribute] if new_data[attribute] != '' else yaml_d['phones'][new_data['phone']][attribute]
            if new_data['status'] != '' or new_data['hub'] != '' or new_data['port'] != '':
                for deployment_path_attribute in ['status', 'hub', 'port']:
                    yaml_d['phones'][new_data['phone']]['deployment_path'][deployment_path_attribute] = new_data[deployment_path_attribute] if new_data[deployment_path_attribute] != '' else yaml_d['phones'][new_data['phone']]['deployment_path'][deployment_path_attribute]
        except KeyError as err:
            error_printing(f"Phone {new_data['phone']} not found.", False)
            if new_data['call_from_CLI']:
                raise err
            return
        if new_data['fota'] != '' or new_data['activitytracking'] != '' or new_data['functional'] != '' or new_data['performance'] != '':
            if not 'testrun_ids' in yaml_d['phones'][new_data['phone']]:
                yaml_d['phones'][new_data['phone']]['testrun_ids'] = {}
                yaml_d['phones'][new_data['phone']]['testrun_ids']['fota'] = new_data['fota'] if new_data['fota'] != '' else None
                yaml_d['phones'][new_data['phone']]['testrun_ids']['activitytracking'] = new_data['activitytracking'] if new_data['activitytracking'] != '' else None
                yaml_d['phones'][new_data['phone']]['testrun_ids']['functional'] = new_data['functional'] if new_data['functional'] != '' else None
                yaml_d['phones'][new_data['phone']]['testrun_ids']['performance'] = new_data['performance'] if new_data['performance'] != '' else None
            else:
                if new_data['fota'] != '':
                    yaml_d['phones'][new_data['phone']]['testrun_ids']['fota'] = new_data['fota']
                if new_data['activitytracking'] != '':
                    yaml_d['phones'][new_data['phone']]['testrun_ids']['activitytracking'] = new_data['activitytracking']
                if new_data['functional'] != '':
                    yaml_d['phones'][new_data['phone']]['testrun_ids']['functional'] = new_data['functional']
                if new_data['performance'] != '':
                    yaml_d['phones'][new_data['phone']]['testrun_ids']['performance'] = new_data['performance']
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
            if ret == '1':
                release_type = 'PU1'
            elif ret == '2':
                release_type = 'PU100'
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
            testrun_ids = dict(fota = new_data['fota'], activitytracking = new_data['activitytracking'], functional = new_data['functional'], performance = new_data['performance'])
            yaml_d['phones'][new_data['phone']]['testrun_ids'] = testrun_ids
        else:
            error_printing("KeyError: User input do not match selection.", False)
            return
        
    with open(file_name, 'w') as w:
        yaml.dump(yaml_d, w)
        error_printing(f'{new_data['phone']} successfully changed.', True)
        return
    error_printing('Error when writing to the yaml file.', False)
