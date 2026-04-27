from error_methods import send_custom_msg_success_fail
from decorators_file import decorator_timer
from ruamel.yaml.comments import CommentedMap

def _find_free_port(data: CommentedMap, stage: str) -> tuple[str, CommentedMap]:
    """
    return path to the first port of value 'None' found by looping through 'stages'[stage] for a given 'stage'\n
    the values of 'stage' can only be 'dev' or 'prod'
    """
    stage_list = data["stages"][stage]

    for hub in stage_list:
        for port, value in hub.items():
            if port.startswith("port") and value is None:
                return port, hub

    send_custom_msg_success_fail(f"Error when trying to find a free port:\nNo free port available in stage '{stage}'.", False)

# deploy phone
@decorator_timer
def deploy_phone(yaml_d: CommentedMap, yaml, file_name: str, phone: str = '', stage: str = '', call_from_CLI: bool = False)->None:
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
    stages = ["prod", "dev"]
    while stage == '':
        print('Stage to deploy:')
        print('1: Production')
        print('2: Development')
        ret = input('? ')
        while ret != "1" and ret != "2":
            print('Please select 1 for Production or 2 for Development')
            ret = input('? ')
        stage = "prod" if ret == "1" else "dev"

    if stage not in stages:
        send_custom_msg_success_fail(f"Please select a stage from {stages}.", False)
        return

    port, hub = _find_free_port(yaml_d, stage)
    if port is None:
        return

    if phone == '':
        phones_not_deployed: list = []
        for phone in yaml_d['phones']:
            if not yaml_d['phones'][phone]["deployment_path"]["hub"]:
                phones_not_deployed.append(phone)

        if not phones_not_deployed:
            send_custom_msg_success_fail(f"No phones available for deployment", False)
            return

        print('Phones available to deploy: ')
        for phone_index, phone in enumerate(phones_not_deployed):
            phone_name = yaml_d['phones'][phone]['name']
            phone_vendor = yaml_d['phones'][phone]['vendor']
            phone_family = yaml_d['phones'][phone]['family']
            phone_version = str(yaml_d['phones'][phone]['version'])
            print(str(phone_index) + ': ' + phone_name)
            print('\t' + phone_vendor + ' ' + phone_family + ' ' + phone_version)

        print("Select phone to deploy")
        while True:
            selected_idx = input('? ')
            if int(selected_idx) > len(phones_not_deployed):
                send_custom_msg_success_fail("IndexError: User input do not match options.", False)
            else:
                break

        selected_phone = phones_not_deployed[int(selected_idx)]

    else:
        if phone not in yaml_d['phones']:
            send_custom_msg_success_fail(f'No phone named {phone}.', False)
            if call_from_CLI:
                raise KeyError
            return

        if yaml_d['phones'][phone]["deployment_path"]["hub"]:
            send_custom_msg_success_fail(f'{phone} is already deployed.', False)
            return

        selected_phone = phone

    yaml_d["phones"][selected_phone].yaml_set_anchor(selected_phone, always_dump=True)
    hub[port] = yaml_d["phones"][selected_phone]
    yaml_d['phones'][selected_phone]["deployment_path"]["hub"] = hub.anchor.value
    yaml_d['phones'][selected_phone]["deployment_path"]["port"] = port
    with open(file_name, 'w') as yaml_file:
        yaml.dump(yaml_d, yaml_file)

    send_custom_msg_success_fail(f'{selected_phone} successfully deployed in {stage}.', True)
