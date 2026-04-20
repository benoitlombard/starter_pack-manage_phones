# importing libraries
import ruamel.yaml
import typer
#global file_name
#global yaml
#global yaml_d

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

def error_method_menu_version(args: list['message': str, 'is_success':bool])->bool:
	"""
	Print error/success message formated GREEN/RED using Typer module.\n
	parameters of function: tuple= (message: str, is_success: bool)
	"""
	message = args[0]
	is_success = args[1]
	if is_success:
		typer.secho(message, fg=typer.colors.GREEN)
		return True
	else:
		typer.secho(message, fg=typer.colors.RED)
		return False

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
				error_method_menu_version(add_phone.add_phone(releasetype = '', write = False, yaml_d = yaml_d, call_from_CLI= False))
			case '2':
				error_method_menu_version(change_phone.change_phone(yaml_d = yaml_d, call_from_CLI= False))
			case '3':
				deploy_phone.deploy_phone(yaml_d = yaml_d, call_from_CLI= False)
			case '4':
				error_method_menu_version(remove_undeploy_phone.undeploy_phone(yaml_d = yaml_d, call_from_CLI= False))
			case '5':
				error_method_menu_version(remove_undeploy_phone.remove_phone(yaml_d = yaml_d, call_from_CLI= False))
			case '6':
				display_infos.display(yaml_d)
