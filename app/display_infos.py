import sys
from error_methods import send_custom_msg_success_fail
from decorators_file import decorator_timer

### Print only name or important info when listing phones

# printing bts or biabs
@decorator_timer
def list_from_yaml(yaml_d: dict, yaml, yaml_list_key: str)->None:
    """
    Function dedicated to print information in the yaml file that are available with a single key entry: 'biab'/'bts'
    """
    yaml.dump(yaml_d[yaml_list_key], sys.stdout)

# printing stages ('dev' or 'prod')
@decorator_timer
def show_stage(yaml_d: dict, yaml, stage: str)->None:
    """
    Display the content of ['stages']['dev'] or ['stages']['prod'] entry in yaml file
    """
    for hub in yaml_d['stages'][stage]:
        print(hub)
        for port in hub:
            if port == 'name':
                print(f"name: {hub[port]}")
            else:
                print(f"{port}:")
                if hub[port] is not str and hub[port] is not None:
                    for attribute in hub[port]:
                        if hub[port][attribute] is dict:
                            for element in hub[port][attribute]:
                                print(f"  {element}: {hub[port][attribute][element]}")
                        else:
                            if type(hub[port][attribute]) is not str and hub[port][attribute] is not None:
                                print(f"  {attribute}:")
                                for element in hub[port][attribute]:
                                    try:
                                        print(f"    {element}: '{float(hub[port][attribute][element])}'")    # mettre assert int OU float
                                    except ValueError:
                                        if hub[port][attribute][element] in ["", "false", "true", None]:
                                            print(f"    {element}: '{hub[port][attribute][element]}'") # mettre assert "" OU ___ (rien du tout)
                                        else:
                                            print(f"    {element}: {hub[port][attribute][element]}")  
                            else:
                                if hub[port][attribute] in ["", "false", "true", None]:
                                    print(f"  {attribute}: '{hub[port][attribute]}'")    # mettre assert "" OU ___ (rien du tout)
                                else:
                                    try:
                                        print(f"  {attribute}: '{float(hub[port][attribute])}'")      # mettre assert int OU float
                                    except ValueError:
                                        print(f"  {attribute}: {hub[port][attribute]}")
                                
                            

                                


    for hub in yaml_d['stages'][stage]:
        yaml.dump(hub, sys.stdout)

def _list_phones(yaml_d: dict, yaml)->None:
    """
    Display phone information ordered and filtered by asking user choices of sorting and filtering
    """
    print('1: all')
    print('2: by vendor')
    print('3: by platform')
    ret = input('? ')
    if ret == '1':
        yaml.dump(yaml_d['phones'], sys.stdout)
        return
    elif ret == '2':
        dict_of_phones_grouped_by_vendor: dict[str, list] = {} # dict_of_phones_grouped_by_vendor = {vendor_1 : [phone_1, phone_2, ...], vendor_2 : [...]}
        list_of_vendors: list = []
        for phone in yaml_d['phones']:
            dict_of_phones_grouped_by_vendor.setdefault(yaml_d['phones'][phone]['vendor'], [])
            dict_of_phones_grouped_by_vendor[yaml_d['phones'][phone]['vendor']].append(yaml_d['phones'][phone]['name'])
            if yaml_d['phones'][phone]['vendor'] not in list_of_vendors:
                list_of_vendors.append(yaml_d['phones'][phone]['vendor'])

        for indx, unique_vendor in enumerate(list_of_vendors):
            print(str(indx) + ": " + unique_vendor) # list_of_vendors is only used to display each unique vendor, for asking user to choose
        print(str(len(list_of_vendors)) + ': All') # case: user want to print all phones
        ret = input('Select vendor: ')

        try:
            ret = int(ret)
        except ValueError:
            send_custom_msg_success_fail("Error: User input do not match selection.", False)
            return

        if ret == len(list_of_vendors):
            yaml.dump(yaml_d['phones'], sys.stdout)

        elif ret < len(list_of_vendors) and ret >= 0:
            selected_vendor = list_of_vendors[ret]
            dict_of_phones_filtered_by_vendor_grouped_by_family: dict[str, list] = {} # dict_of_phones_filtered_by_vendor_grouped_by_family = {family_1 : [phone_4, phone_7, ...], family_2 : [...]}
            list_of_families: list = []
            for phone in dict_of_phones_grouped_by_vendor[selected_vendor]:
                dict_of_phones_filtered_by_vendor_grouped_by_family.setdefault(yaml_d['phones'][phone]['family'], [])
                dict_of_phones_filtered_by_vendor_grouped_by_family[yaml_d['phones'][phone]['family']].append(yaml_d['phones'][phone]['name'])
                if yaml_d['phones'][phone]['family'] not in list_of_families:
                    list_of_families.append(yaml_d['phones'][phone]['family'])

            for indx, unique_family in enumerate(list_of_families):
                print(str(indx) + ": " + unique_family) # list_of_families is only used to display each unique family, asking user to choose
            print(str(len(list_of_families)) + ': All') # case: user want to print all phones of previously chosen vendor
            ret = input('Select family: ')

            try:
                ret = int(ret)
            except ValueError:
                send_custom_msg_success_fail("Error: User input do not match selection.", False)
                return

            if ret == len(list_of_families):
                for phone in dict_of_phones_grouped_by_vendor[selected_vendor]:
                    yaml.dump(yaml_d['phones'][phone], sys.stdout) # case: printing all phones of previously chosen vendor
                return

            elif ret < len(list_of_families) and ret >= 0:
                selected_family = list_of_families[ret]
                dict_of_phones_filtered_by_vendor_and_family_grouped_by_version: dict[str, list] = {} # dict_of_phones_filtered_by_vendor_and_family_grouped_by_version = {version_1 : [phone_4, phone_12, ...], version_2 : [...]}
                list_of_versions: list = []
                for phone in dict_of_phones_filtered_by_vendor_grouped_by_family[selected_family]:
                    dict_of_phones_filtered_by_vendor_and_family_grouped_by_version.setdefault(yaml_d['phones'][phone]['version'], [])
                    dict_of_phones_filtered_by_vendor_and_family_grouped_by_version[yaml_d['phones'][phone]['version']].append(yaml_d['phones'][phone]['name'])
                    if yaml_d['phones'][phone]['version'] not in list_of_versions:
                        list_of_versions.append(yaml_d['phones'][phone]['version'])

                for indx, unique_version in enumerate(list_of_versions):
                    print(str(indx) + ": " + unique_version) # list_of_versions is only used to display each unique version, allowing user to choose
                print(str(len(list_of_versions)) + ': All') # case: user want to print all phones of previously chosen family
                ret = input('Select version: ')

                try:
                    ret = int(ret)
                except ValueError:
                    send_custom_msg_success_fail("Error: User input do not match selection.", False)
                    return

                if ret == len(list_of_versions):
                    for phone in dict_of_phones_filtered_by_vendor_grouped_by_family[selected_family]:
                        yaml.dump(yaml_d['phones'][phone], sys.stdout) # case: printing all phones of previously chosen family
                    return

                elif ret < len(list_of_vendors) and ret >= 0:
                    selected_version = list_of_versions[ret]
                    for phone in dict_of_phones_filtered_by_vendor_and_family_grouped_by_version[selected_version]:
                        yaml.dump(yaml_d['phones'][phone], sys.stdout) # printing all phones of Selected_vendor, Selected_family, Selected_version
                    return

    elif ret == '3': # printing by platform
        list_of_platform = []
        for phone in yaml_d['phones']:
            if yaml_d['phones'][phone]['platform'] not in list_of_platform:
                list_of_platform.append(yaml_d['phones'][phone]['platform'])

        for indx, unique_platform in enumerate(list_of_platform):
            print(str(indx) + ": " + unique_platform)
        ret = input('Select platform: ')

        try:
            ret = int(ret)
            selected_platform =  list_of_platform[ret]
        except ValueError:
            send_custom_msg_success_fail("Error: User input do not match selection.", False)
            return

        for phone in yaml_d['phones']:
            if selected_platform == yaml_d['phones'][phone]['platform']:
                yaml.dump(yaml_d['phones'][phone], sys.stdout)
        return

    send_custom_msg_success_fail("Error: User input do not match selection.", False) # handling every case of 'input > max' with this single line and by returning after yaml.dump

def display(yaml_d: dict, yaml)->None:
    """
    Display a sub menu dedicated to allow user to list and print information stored in the yaml file
    """
    print('1: List phones')
    print('2: List all bts')
    print('3: List all biab')
    print('4: List production stage')
    print('5: List development stage')
    print('6: Show undeployed phones')
    print('7: Show configuration of phone')
    ret = input('? ')
    match ret:
        case '1':
            _list_phones(yaml_d = yaml_d,
                         yaml = yaml)
        case '2':
            list_from_yaml(yaml_d = yaml_d,
                        yaml = yaml,
                        yaml_list_key = 'bts') # new function
        case '3':
            list_from_yaml(yaml_d = yaml_d,
                        yaml = yaml,
                        yaml_list_key = 'biab') # new function (same as previous)
        case '4':
            show_stage(yaml_d = yaml_d,
                        yaml = yaml,
                        stage = 'prod')
        case '5':
            show_stage(yaml_d = yaml_d,
                        yaml = yaml,
                        stage = 'dev')
        case '6':
            print('Not deployed phones:')
            for phone in yaml_d['phones']:
                if yaml_d['phones'][phone]['deployment_path']['hub'] is not None:
                    yaml.dump(yaml_d['phones'][phone], sys.stdout)
        case '7':                # new function
            print('Phone to show: ')
            ret = input('? ')
            try:
                yaml.dump(yaml_d['phones'][ret], sys.stdout)
            except KeyError:
                send_custom_msg_success_fail(f"Error: phone '{ret}' not found.", False)
        case _:
            send_custom_msg_success_fail("User input do not match selection.", False)
