# importing libraries
import ruamel.yaml
import sys # useful for dumping yaml content to terminal
import click

file_name = 'test.yaml'
with open(file_name, 'r') as yaml_file:
	yaml = ruamel.yaml.YAML(typ='rt')
	yaml_d = yaml.load(yaml_file)

# importing other files
import display_infos
import add_phone
import change_phone
import deploy_phone
import remove_undeploy_phone


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
		if ret == '1':
			add_phone.add_phone(yaml_d)
		elif ret == '2':
			change_phone.change_phone(yaml_d)
		elif ret == '3':
			deploy_phone.deploy_phone(yaml_d)
		elif ret == '4':
			remove_undeploy_phone.undeploy_phone('', yaml_d)
		elif ret == '5':
			remove_undeploy_phone.remove_phone(yaml_d)
		elif ret == '6':
			display_infos.display(yaml_d)

