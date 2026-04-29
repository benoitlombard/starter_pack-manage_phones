from error_methods import send_custom_msg_success_fail
from decorators_file import decorator_timer
from ruamel.yaml.comments import CommentedMap

# undeploy phone
@decorator_timer
def undeploy_phone(yaml_d: CommentedMap, yaml, file_name: str, phone: str = '', call_from_CLI: bool = False)->None:
    """
    Undeploy phone from 'stage', given his name\n
    It particular, values from his 'deployment_path' are set to none, 'deployed' attribute is set to false\n
    And the port his emptied from a reference of a yaml anchor of the phone's data
    """
    while phone == '':
        dict_of_phones = {}
        print('Phone to undeploy: ')
        for phone_index, inspected_phone in  enumerate(yaml_d['phones']):
            if yaml_d['phones'][inspected_phone]['deployment_path']["hub"]:
                dict_of_phones[phone_index] = yaml_d['phones'][inspected_phone]['name']
                print(str(phone_index) + ': ' + yaml_d['phones'][inspected_phone]['name'])
        indx = input('? ')
        try:
            phone = dict_of_phones[int(indx)]
        except ValueError as err:
            send_custom_msg_success_fail("Error: User input do not match selection.", False)
            if call_from_CLI:
                raise err
            return
        except KeyError as err:
            send_custom_msg_success_fail("Error: User input do not match selection.", False)
            if call_from_CLI:
                raise err
            return
    try:
        hubs = ["switch", "usb_hub"]
        phone_deployment_hub = ""
        phone_deployment_port = ""
        if yaml_d['phones'][phone]["deployment_path"]["hub"]:
            phone_deployment_hub = yaml_d['phones'][phone]['deployment_path']['hub']
            phone_deployment_port = yaml_d['phones'][phone]['deployment_path']['port']
            for hub in hubs:
                if yaml_d[hub].get(phone_deployment_hub):
                    hub_deployed = yaml_d[hub][phone_deployment_hub]

            hub_deployed[phone_deployment_port] = None
            yaml_d['phones'][phone]['deployment_path']['hub'] = None
            yaml_d['phones'][phone]['deployment_path']['port'] = None

        else:
            send_custom_msg_success_fail(f"{phone} is not deployed.\nUndeployment is not possible.", False)
            return

    except KeyError as err:
        send_custom_msg_success_fail("Key Error when writing to the yaml file.\nUndeployment failed, please verify phone name.", False)
        if call_from_CLI:
            raise err
        return

    with open(file_name, 'w') as w:
        yaml.dump(yaml_d, w)
        send_custom_msg_success_fail(f"{phone} successfully undeployed.", True)
        send_custom_msg_success_fail('Please unplug ' + str(phone) + ' from ' + str(phone_deployment_port) + ' at hub ' + str(phone_deployment_hub), True)

# remove phone
@decorator_timer
def remove_phone(yaml_d: CommentedMap, yaml, file_name: str, phone: str = '', call_from_CLI: bool = False)->None:
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
            if yaml_d['phones'][phone]['deployment_path']["hub"]:
                undeploy_phone(yaml_d, yaml, file_name, phone, call_from_CLI)
            del yaml_d['phones'][phone]
            with open(file_name, 'w') as w:
                yaml.dump(yaml_d, w)
                send_custom_msg_success_fail(f'{phone} successfully removed.', True)
                return
        else:
            send_custom_msg_success_fail('User aborted phone removal.', False)
            return

    send_custom_msg_success_fail(f"Error: phone '{phone}' not found.", False)
