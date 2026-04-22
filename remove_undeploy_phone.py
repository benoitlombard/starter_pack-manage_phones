from manage_phones import yaml_d, yaml, file_name
from error_methods import error_printing
from decorators_file import decorator_timer

# undeploy phone
@decorator_timer
def undeploy_phone(phone: str = '', yaml_d: dict = yaml_d, call_from_CLI: bool = False)->None:
    """
    Undeploy phone from 'stage', given his name\n
    It particular, values from his 'deployment_path' are set to none, 'deployed' attribute is set to false\n
    And the port his emptied from a reference of a yaml anchor of the phone's data
    """
    while phone == '':
        dict_of_phones = {}
        print('Phone to undeploy: ')
        for phone_index, inspected_phone in  enumerate(yaml_d['phones']):
            if yaml_d['phones'][inspected_phone]['deployed']:
                dict_of_phones[phone_index] = yaml_d['phones'][inspected_phone]['name']
                print(str(phone_index) + ': ' + yaml_d['phones'][inspected_phone]['name'])
        indx = input('? ')
        try:
            phone = dict_of_phones[int(indx)]
        except ValueError as err:
            error_printing("Error: User input do not match selection.", False)
            if call_from_CLI:
                raise err
            return
        except KeyError as err:
            error_printing("Error: User input do not match selection.", False)
            if call_from_CLI:
                raise err
            return
    try:
        if yaml_d['phones'][phone]['deployed']:
            phone_deployment_status = yaml_d['phones'][phone]['deployment_path']['status']
            phone_deployment_hub = yaml_d['phones'][phone]['deployment_path']['hub']
            phone_deployment_port = yaml_d['phones'][phone]['deployment_path']['port']
            source_name = yaml_d['stages'][phone_deployment_status][phone_deployment_hub]['source_name']
            hub_name = yaml_d['stages'][phone_deployment_status][phone_deployment_hub]['hub_name']
            yaml_d[str(source_name)][str(hub_name)][phone_deployment_port] = None

            yaml_d['phones'][phone]['deployment_path']['status'] = None
            yaml_d['phones'][phone]['deployment_path']['hub'] = None
            yaml_d['phones'][phone]['deployment_path']['port'] = None
            yaml_d['phones'][phone]['deployed'] = False
        else:
            error_printing(f"{phone} is not deployed.\nUndeployment is not possible.", False)
            return
    except KeyError as err:
        error_printing("Key Error when writing to the yaml file.\nUndeployment failed, please verify phone name.", False)
        if call_from_CLI:
            raise err
        return

    with open(file_name, 'w') as w:
        yaml.dump(yaml_d, w)
        error_printing(f"{phone} successfully undeployed.", True)
        error_printing('Please unplug ' + str(phone) + ' from ' + str(phone_deployment_port) + ' at hub ' + str(hub_name) + ' at stage ' + str(phone_deployment_status), True)

# remove phone
@decorator_timer
def remove_phone(phone: str = '', yaml_d: dict = yaml_d, call_from_CLI: bool = False)->None:
    """
    Remove an existing phone by asking user for input\n
    remove_phone will check if the phone is deployed and undeploy it if necessary before removing it 
    """
    while phone == '':
        print('Enter phone name')
        phone = input('? ')
    if phone in yaml_d['phones']:
        if not call_from_CLI:
            print('Sure to remove ' + phone + ' from test inventory?')
            print('You can just undeploy from test stages.')

        if call_from_CLI or input('enter yes if are sure: ').lower() == 'yes':
            if yaml_d['phones'][phone]['deployed']:
                undeploy_phone(phone, yaml_d, call_from_CLI)
            del yaml_d['phones'][phone]
            with open(file_name, 'w') as w:
                yaml.dump(yaml_d, w)
                error_printing(f'{phone} successfully removed.', True)
                return
        else:
            error_printing('User aborted phone removal.', False)
            return
    error_printing(f"Error: phone '{phone}' not found.", False)




