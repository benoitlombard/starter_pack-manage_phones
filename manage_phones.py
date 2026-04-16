# importing libraries
import ruamel.yaml

global file_name
global yaml
global yaml_d

file_name = 'test.yaml'	# variables: file_name, yaml, yaml_d have to be declared before importing local modules
with open(file_name, 'r') as yaml_file:
	yaml = ruamel.yaml.YAML(typ='rt')
	yaml_d = yaml.load(yaml_file)

# importing other files
import display_infos	# displaying infos
import add_phone		# adding a new phone
import change_phone		# changing phone infos
import deploy_phone		# deploying a phone
import remove_undeploy_phone	# removing or undeploying a phone

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
				add_phone.add_phone(yaml_d)
			case '2':
				change_phone.change_phone(yaml_d)
			case '3':
				deploy_phone.deploy_phone(yaml_d)
			case '4':
				remove_undeploy_phone.undeploy_phone('', yaml_d)
			case '5':
				remove_undeploy_phone.remove_phone(yaml_d)
			case '6':
				display_infos.display(yaml_d)
