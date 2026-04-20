from manage_phones import yaml_d, yaml, file_name

# undeploy phone
def undeploy_phone(phone: str = '', yaml_d: dict = yaml_d, call_from_CLI: bool = False)->tuple[str,bool]:
	"""
	Undeploy phone from 'stage', given his name\n
	It particular, values from his 'deployment_path' are set to none, 'deployed' attribute is set to false\n
	And the port his emptied from a reference of a yaml anchor of the phone's data
	"""
	while phone == '':
		dict_of_phones = {}
		print('Phone to undeploy: ')
		for phone_index, inspected_phone in  enumerate(yaml_d['phones']):
			if yaml_d['phones'][inspected_phone]['deployed']:
				dict_of_phones[phone_index] = yaml_d['phones'][inspected_phone]['name']
				print(str(phone_index) + ': ' + yaml_d['phones'][inspected_phone]['name'])
		indx = input('? ')
		try:
			phone = dict_of_phones[int(indx)]
		except:
			return "Unknown selection.", False
		
	try:
		if yaml_d['phones'][phone]['deployed']:
			phone_deployment_status = yaml_d['phones'][phone]['deployment_path']['status']
			phone_deployment_hub = yaml_d['phones'][phone]['deployment_path']['hub']
			phone_deployment_port = yaml_d['phones'][phone]['deployment_path']['port']
			source_name = yaml_d['stages'][phone_deployment_status][phone_deployment_hub]['source_name']
			hub_name = yaml_d['stages'][phone_deployment_status][phone_deployment_hub]['hub_name']
			yaml_d[str(source_name)][str(hub_name)][phone_deployment_port] = None

			yaml_d['phones'][phone]['deployment_path']['status'] = None
			yaml_d['phones'][phone]['deployment_path']['hub'] = None
			yaml_d['phones'][phone]['deployment_path']['port'] = None
			yaml_d['phones'][phone]['deployed'] = False
		else:
			return f"{phone} is not deployed.\nUndeployment is not possible.", False
	except:
		return "Key Error when writing to the yaml file.\nUndeployment failed.", False

	with open(file_name, 'w') as w:
		yaml.dump(yaml_d, w)
		print('Please unplug ' + str(phone) + ' from ' + str(phone_deployment_port) + ' at hub ' + str(phone_deployment_hub) + ' at stage ' + str(phone_deployment_status))
		return f"{phone} successfully undeployed.", True
	return "Unknown error happened.", False
	

# remove phone
def remove_phone(phone: str = '', yaml_d: dict = yaml_d, call_from_CLI: bool = False)->tuple[str,bool]:
	"""
	Remove an existing phone by asking user for input\n
	remove_phone will check if the phone is deployed and undeploy it if necessary befor removing it 
	"""
	while phone == '':
		print('Enter phone name')
		phone = input('? ')
	if phone in yaml_d['phones']:
		if not call_from_CLI:
			print('Sure to remove ' + phone + ' from test inventory?')
			print('You can just undeploy from test stages.')
		if call_from_CLI or input('enter yes if are sure: ').lower() == 'yes':
			if yaml_d['phones'][phone]['deployed']:
				undeploy_phone(phone, yaml_d, call_from_CLI) # passing call_from_CLI argument
			del yaml_d['phones'][phone]
			with open(file_name, 'w') as w:
				yaml.dump(yaml_d, w)
				return f'{phone} successfully removed.', True
		else:
			return 'User aborted phone removal.', False
	return f'{phone} not found.', False



