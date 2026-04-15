import time
from manage_phones import yaml_d, yaml, file_name

# undeploy phone
def undeploy_phone(phone: str, yaml_d: dict = yaml_d) -> None:
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
			print("Error: unknown phone")
			return
	if yaml_d['phones'][phone]['deployed']:
		phone_deployment_status = yaml_d['phones'][phone]['deployment_path']['status']
		phone_deployment_hub = yaml_d['phones'][phone]['deployment_path']['hub']
		phone_deployment_port = yaml_d['phones'][phone]['deployment_path']['port']
		try:
			source_name = yaml_d['stages'][phone_deployment_status][phone_deployment_hub]['source_name']
			hub_name = yaml_d['stages'][phone_deployment_status][phone_deployment_hub]['hub_name']
			yaml_d[str(source_name)][str(hub_name)][phone_deployment_port] = None

			yaml_d['phones'][phone]['deployment_path']['status'] = None
			yaml_d['phones'][phone]['deployment_path']['hub'] = None
			yaml_d['phones'][phone]['deployment_path']['port'] = None
			yaml_d['phones'][phone]['deployed'] = False
		except:
			print("error when undeploying", phone)

		with open(file_name, 'w') as w:
			yaml.dump(yaml_d, w)
			print('Please unplug ' + str(phone) + ' from ' + str(phone_deployment_port) + ' at hub ' + str(phone_deployment_hub) + ' at stage ' + str(phone_deployment_status))
	else:
		print(phone, "is not deployed.")
	return

# remove phone
def remove_phone(yaml_d: dict = yaml_d)->None:
	"""
	Remove an existing phone by asking user for input\n
	remove_phone will check if the phone is deployed and undeploy it if necessary befor removing it 
	"""
	print('Enter phone name')
	phone = input('? ')
	if phone in yaml_d['phones']:
		print('Sure to remove ' + phone + ' from test inventory?')
		print('You can just undeploy from test stages.')
		if input('enter yes if are sure: ').lower() == 'yes':
			time_origin = time.time()
			if yaml_d['phones'][phone]['deployed']:
				undeploy_phone(phone, yaml_d)
			del yaml_d['phones'][phone]
			with open(file_name, 'w') as w:
					yaml.dump(yaml_d, w)
		print(f"time elapsed: {(time.time() - time_origin):.6f} seconds.")
		return
	print(phone + ' not found')

