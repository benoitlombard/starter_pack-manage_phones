# importing libraries
import ruamel.yaml

file_name = 'test.yaml'    # variables: file_name, yaml, yaml_d have to be declared before importing local modules
with open(file_name, 'r') as yaml_file:
    yaml = ruamel.yaml.YAML(typ='rt')
    yaml_d = yaml.load(yaml_file)

# importing other files
from display_infos import display   # displaying infos
from add_phone import add_phone       # adding a new phone
from change_phone import change_phone       # changing phone infos
from deploy_phone import deploy_phone        # deploying a phone
from remove_undeploy_phone import undeploy_phone, remove_phone    # removing or undeploying a phone

if __name__ == "__main__":
    ret = ''
    while ret != 'x':
        print('---------------------------------------------')
        print('Manage: ')
        print('1: Add phone')
        print('2: Change phone')
        print('3: Deploy phone')
        print('4: Undeploy phone')
        print('5: Remove phone')
        print('6: Show configuration')
        print('x: Exit')
        ret = input('? ')

        match ret:
            case '1':
                add_phone(yaml_d = yaml_d, yaml = yaml, file_name = file_name, write = False, call_from_CLI= False)
            case '2':
                change_phone(yaml_d = yaml_d, yaml = yaml, file_name = file_name, call_from_CLI= False)
            case '3':
                deploy_phone(yaml_d = yaml_d, yaml = yaml, file_name = file_name, call_from_CLI= False)
            case '4':
                undeploy_phone(yaml_d = yaml_d, yaml = yaml, file_name = file_name, call_from_CLI= False)
            case '5':
                remove_phone(yaml_d = yaml_d, yaml = yaml, file_name = file_name, call_from_CLI= False)
            case '6':
                display(yaml_d = yaml_d, yaml = yaml)
