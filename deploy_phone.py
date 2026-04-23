import ruamel.yaml
from error_methods import error_printing
from decorators_file import decorator_timer

def _find_free_port(stage: str, yaml_d: dict, call_from_CLI: bool = False)->dict[int, str]:
    """
    return path to the first port of value 'None' found by looping through 'stages'[stage] for a given 'stage'\n
    the values of 'stage' can only be 'dev' or 'prod'
    """
    try:
        for hub_id in range(len(yaml_d['stages'][stage])):
            test_source = yaml_d['stages'][stage][hub_id]['source_name']
            test_hub = yaml_d['stages'][stage][hub_id]['hub_name']
            for port in yaml_d['stages'][stage][hub_id]:
                if yaml_d[test_source][test_hub][port] is None:
                    return dict(hub_id = hub_id, port = port)
                
            error_printing(f"Error when trying to find a free port:\nNo free port available in stage '{stage}'.", False)
    except KeyError as err:
        error_printing(f"Error when trying to find a free port:\nPlease make sure the stage '{stage}' exists.", False)
        if call_from_CLI:
            raise err

# deploy phone
@decorator_timer
def deploy_phone(yaml_d: dict, yaml, file_name: str, phone: str = '', stage: str = '', call_from_CLI: bool = False)->None:
    """
    Deploy an existing phone by asking user for input\n
    1) Ask user for what stage he wants between 'dev' or 'prod' as deployment stage\n
    2) Search for a free port in 'stages'[stage][hubs]\n
    3) Ask user to chose a phone from list extracted from elements in 'phones' which ['deployed'] attribute is False\n
    4) Update 'deployed' and 'deploy_path' attributes from 'phones'[phone]\n
    5) Copy information of 'phones'[phone] in a new ruamel.yaml commented map\n
    6) Set a ruamel.yaml Anchor and store a reference to it in the free port found in 'stages'[stage][hubs]\n
    7) Update the yaml file according to previous changes.
    """
    while stage == '':
        print('Stage to deploy:')
        print('1: Production')
        print('2: Development')
        ret = input('? ')
        if ret == '1':
            stage = 'prod'
        elif ret == '2':
            stage = 'dev'
        else:
            print('User input do not match selection')
            stage = ''

    free_port = _find_free_port(stage, yaml_d, call_from_CLI)
    if free_port is not None:
        if phone == '':
            list_of_phones_deployed = set()
            print('Phone to deploy: ')
            for phone in yaml_d['phones']:
                if not yaml_d['phones'][phone]['deployed']:
                    list_of_phones_deployed.add(phone)

            list_of_phones_deployed = list(list_of_phones_deployed)
            for phone_index, phone in enumerate(list_of_phones_deployed):
                print(str(phone_index) + ': ' + yaml_d['phones'][phone]['name'])
                print('\t' + yaml_d['phones'][phone]['vendor'] + ' ' + yaml_d['phones'][phone]['family'] + ' ' + str(yaml_d['phones'][phone]['version']))
            indx = input('? ')
            try:
                selected_phone = list_of_phones_deployed[int(indx)]
            except ValueError as err:
                error_printing("ValueError: User input do not match selection.", False)
                if call_from_CLI:
                    raise err
                return
            except IndexError as err:
                error_printing("IndexError: User input do not match selection.", False)
                if call_from_CLI:
                    raise err
                return
        else:
            try:
                if yaml_d['phones'][phone]['deployed']:
                    error_printing(f'{phone} is already deployed.', False)
                    return
                selected_phone = phone
            except KeyError as err:
                error_printing(f'No phone named {phone}.', False)
                if call_from_CLI:
                    raise err
                return

        yaml_d['phones'][selected_phone]['deployment_path']['status'] = stage
        yaml_d['phones'][selected_phone]['deployment_path']['hub'] = free_port['hub_id']
        yaml_d['phones'][selected_phone]['deployment_path']['port'] = free_port['port']
        # defining the yaml commented map (one version if testrun_ids defined, and one version if testrun_ids not defined)
        full_phone_infos_as_ruamel_map = ruamel.yaml.CommentedMap(name = yaml_d['phones'][selected_phone]['name'],
                                            manufacturer = yaml_d['phones'][selected_phone]['manufacturer'],
                                            model =  yaml_d['phones'][selected_phone]['model'],
                                            vendor = yaml_d['phones'][selected_phone]['vendor'],
                                            family = yaml_d['phones'][selected_phone]['family'],
                                            version = yaml_d['phones'][selected_phone]['version'],
                                            platform = yaml_d['phones'][selected_phone]['platform'],
                                            release_type = yaml_d['phones'][selected_phone]['release_type'],
                                            ip = yaml_d['phones'][selected_phone]['ip'],
                                            udid = yaml_d['phones'][selected_phone]['udid'],
                                            user = yaml_d['phones'][selected_phone]['user'],
                                            deployed = yaml_d['phones'][selected_phone]['deployed'],
                                            deployment_path = yaml_d['phones'][selected_phone]['deployment_path']
                                            )

        if 'testrun_ids' in yaml_d['phones'][selected_phone]: # version with testrun_ids defined
            full_phone_infos_as_ruamel_map['testrun_ids'] = yaml_d['phones'][selected_phone]['testrun_ids']

        yaml_d['phones'][selected_phone] = full_phone_infos_as_ruamel_map
        yaml_d['phones'][selected_phone].yaml_set_anchor(selected_phone, always_dump=True)

        # Setting the reference to the phone :
        source_name = yaml_d['stages'][stage][free_port['hub_id']]['source_name']
        hub_name = yaml_d['stages'][stage][free_port['hub_id']]['hub_name']
        port_name = free_port['port']
        yaml_d[str(source_name)][str(hub_name)][str(port_name)] = yaml_d['phones'][selected_phone]

        yaml_d['phones'][selected_phone]['deployed'] = True

        error_printing(str(selected_phone) + ' deployed to ' + str(free_port['port']) + ' at hub ' + str(yaml_d['stages'][stage][free_port['hub_id']]['name']), True)
        print('Please connect phone as soon as possible')

        with open(file_name, 'w') as yaml_file:
            yaml.dump(yaml_d, yaml_file)
            error_printing(f'{selected_phone} successfully deployed in {stage}.', True)
