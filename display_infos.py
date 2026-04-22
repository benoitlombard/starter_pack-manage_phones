import sys
from error_methods import error_printing
from decorators_file import decorator_timer

# printing bts or biabs
@decorator_timer
def _list_from_yaml(yaml_d: dict, yaml, yaml_list_key: str)->None:
    """
    Function dedicated to print information in the yaml file that are available with a single key entry: 'biab'/'bts'
    """
    yaml.dump(yaml_d[yaml_list_key], sys.stdout)

# printing stages ('dev' or 'prod')
@decorator_timer
def _show_stage(yaml_d: dict, yaml, stage: str)->None:
    """
    Display the content of ['stages']['dev'] or ['stages']['prod'] entry in yaml file
    """
    for hub in yaml_d['stages'][stage]:
        yaml.dump(hub, sys.stdout)

def _ask_user_for_sorting_parameters(yaml_d: dict, yaml, phone_attribute: str, selected_vendor: str = '', selected_family: str = '')-> str | None: ####### change
    """
    Ask user for sorting and filtering parameters and print information of phones that match the filtering and sorting
    """
    list_of_selected_attribute = []
    for phone in yaml_d['phones']:
        if (phone_attribute == 'vendor' and yaml_d['phones'][phone]['vendor'] not in list_of_selected_attribute) or (phone_attribute == 'platform' and yaml_d['phones'][phone]['platform'] not in list_of_selected_attribute):
            list_of_selected_attribute.append(yaml_d['phones'][phone][phone_attribute])
        elif phone_attribute == 'family' and selected_vendor == yaml_d['phones'][phone]['vendor']:
            list_of_selected_attribute.append(yaml_d['phones'][phone][phone_attribute])
        elif phone_attribute == 'version' and selected_vendor == yaml_d['phones'][phone]['vendor'] and selected_family == yaml_d['phones'][phone]['family']:
            list_of_selected_attribute.append(yaml_d['phones'][phone][phone_attribute])

    for atttribute_index in range(len(list_of_selected_attribute)):
        print(str(atttribute_index) + ': ' + str(list_of_selected_attribute[atttribute_index]))
    if phone_attribute in ['family', 'version']:
        print(str(atttribute_index + 1) + ': All')
    ret = input('Select ' + phone_attribute + ': ')

    try:
        ret = int(ret)
    except ValueError:
        error_printing("Error: User input do not match selection.", False)
        return
    if ret == atttribute_index + 1:
        for phone in yaml_d['phones']:
            if (phone_attribute == 'family' and selected_vendor == yaml_d['phones'][phone]['vendor']) or (phone_attribute == 'version' and selected_vendor == yaml_d['phones'][phone]['vendor'] and selected_family == yaml_d['phones'][phone]['family']):
                yaml.dump(yaml_d['phones'][phone], sys.stdout)
        return
    elif ret <= atttribute_index:
        if phone_attribute == 'version':
            for phone in yaml_d['phones']:
                if selected_vendor == yaml_d['phones'][phone]['vendor'] and selected_family == yaml_d['phones'][phone]['family'] and list_of_selected_attribute[ret] == yaml_d['phones'][phone]['version']:
                    yaml.dump(yaml_d['phones'][phone], sys.stdout)
            return
        elif phone_attribute == 'platform':
            for phone in yaml_d['phones']:
                if list_of_selected_attribute[ret] == yaml_d['phones'][phone]['platform']:
                    yaml.dump(yaml_d['phones'][phone], sys.stdout)
        return list_of_selected_attribute[ret]
    else:
        error_printing("Error: User input do not match selection.", False)

def _list_phones(yaml_d: dict, yaml)->None: ####### change
    """
    Display phone information ordered and filtered by asking user choices of sorting and filtering
    """
    print('1: all')
    print('2: by model')
    print('3: by platform')
    ret = input('? ')
    try:
        if ret == '1':
            yaml.dump(yaml_d['phones'], sys.stdout)
        elif ret == '2':
                sel_vendor = _ask_user_for_sorting_parameters(yaml_d = yaml_d, yaml = yaml,
                                                              phone_attribute = 'vendor', 
                                                              selected_vendor = '',
                                                              selected_family = '')
                if sel_vendor is not None:
                    sel_family = _ask_user_for_sorting_parameters(yaml_d = yaml_d, yaml = yaml,
                                                                  phone_attribute = 'family',
                                                                  selected_vendor = sel_vendor,
                                                                  selected_family = '')
                    if sel_family is not None:
                        return _ask_user_for_sorting_parameters(yaml_d = yaml_d, yaml = yaml,
                                                                  phone_attribute = 'version',
                                                                  selected_vendor = sel_vendor,
                                                                  selected_family = sel_family)
        elif ret == '3':
            return _ask_user_for_sorting_parameters(yaml_d = yaml_d, yaml = yaml,
                                                    phone_attribute = 'platform',
                                                    selected_vendor = '',
                                                    selected_family = '')
        else:
            error_printing("Error: User input do not match selection.", False)
    except:
        error_printing("Error in the function", False)

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
            _list_from_yaml(yaml_d = yaml_d, 
                        yaml = yaml, 
                        yaml_list_key = 'bts') # new function
        case '3':
            _list_from_yaml(yaml_d = yaml_d,
                        yaml = yaml,
                        yaml_list_key = 'biab') # new function (same as previous)
        case '4':
            _show_stage(yaml_d = yaml_d,
                        yaml = yaml,
                        stage = 'prod')
        case '5':
            _show_stage(yaml_d = yaml_d,
                        yaml = yaml,
                        stage = 'dev')
        case '6':
            print('Not deployed phones:')
            for phone in yaml_d['phones']:
                if not yaml_d['phones'][phone]['deployed']:
                    print(yaml_d['phones'][phone])
        case '7':                # new function
            print('Phone to show: ')
            ret = input('? ')
            try:
                yaml.dump(yaml_d['phones'][ret], sys.stdout)
            except:
                error_printing(f"Error: phone '{ret}' not found.", False)
        case _:
            error_printing("User input do not match selection.", False)