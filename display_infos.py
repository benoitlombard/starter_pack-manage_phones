import sys
from manage_phones import yaml_d, yaml

def _list_from_yaml(yaml_list_key: str, yaml_d: dict = yaml_d)->None:
	"""
	Function dedicated to print informations in the yaml file that are available with a single key entry: 'biab'/'bts'
	"""
	yaml.dump(yaml_d[yaml_list_key], sys.stdout)
	return

def _show_stage(stage: str, yaml_d: dict = yaml_d)->None:
	"""
	Display the content of 'stages'['dev'] or 'stages'['prod'] from yaml file
	"""
	for hub in yaml_d['stages'][stage]:
		yaml.dump(hub, sys.stdout)

def _ask_user_for_sorting_parameters(phone_attribute: str, selected_vendor: str = '', selected_family: str = '', yaml_d: dict = yaml_d)-> str | None:
	"""
	Ask user for sorting and filtering parameters and print informations of phones that match the filtering and sorting
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
	except:
		print('Unknown selection')
		return
	if ret == atttribute_index + 1:
		for phone in yaml_d['phones']:
			if phone_attribute == 'family' and selected_vendor == yaml_d['phones'][phone]['vendor']:
				yaml.dump(yaml_d['phones'][phone], sys.stdout)
					
			elif phone_attribute == 'version' and selected_vendor == yaml_d['phones'][phone]['vendor'] and selected_family == yaml_d['phones'][phone]['family']:
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


def _list_phones(yaml_d: dict = yaml_d)->None:
	"""
	Display phone informations ordered and filtered by asking user choices of sorting and filtering
	"""
	print('1: all')
	print('2: by model')
	print('3: by platform')
	ret = input('? ')
	if ret == '1':
		yaml.dump(yaml_d['phones'], sys.stdout)
	elif ret == '2':
		sel_vendor = _ask_user_for_sorting_parameters('vendor', '', '', yaml_d)
		if sel_vendor != None:
			sel_family = _ask_user_for_sorting_parameters('family', sel_vendor, '', yaml_d)
			if sel_family != None:
				sel_platform = _ask_user_for_sorting_parameters('version', sel_vendor, sel_family, yaml_d)
	elif ret == '3':
		_ask_user_for_sorting_parameters('platform', '', '', yaml_d)

def display(yaml_d: dict = yaml_d)->None:
	"""
	Display a sub menu dedicated to allow user to list and print informations stored in the yaml file 
	"""
	print('1: List phones')
	print('2: List all bts')
	print('3: List all biab')
	print('4: List production stage')
	print('5: List development stage')
	print('6: Show undeployed phones')
	print('7: Show configuration of phone')
	ret = input('? ')
	if ret == '1':
		_list_phones(yaml_d)
	elif ret == '2':				#new function
		_list_from_yaml('bts', yaml_d)
	elif ret == '3':				#new function (same as previous)
		_list_from_yaml('biab', yaml_d)
	elif ret == '4':
		_show_stage('prod', yaml_d)
	elif ret == '5':
		_show_stage('dev', yaml_d)
	elif ret == '6':				#deleted call to check_deployed (optimizing)
		print('Not deployed phones:')
		for phone in yaml_d['phones']:
			if not yaml_d['phones'][phone]['deployed']:
				print(yaml_d['phones'][phone])
	elif ret == '7':				#new function
		print('Phone to show: ')
		ret = input('? ')
		for phone in yaml_d['phones']:
			if yaml_d['phones'][phone]['name'].lower() == ret.lower():
				yaml.dump(yaml_d['phones'][phone], sys.stdout)
				return
		print("Phone not found.")