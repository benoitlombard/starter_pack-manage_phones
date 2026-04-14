from manage_phones import *

def _find_free_port(stage: str, yaml_d: dict)->dict[int, str]:
	"""
	return the first port of value 'None' found by looping through 'stages'[stage] for a given 'stage'\n
	the values of 'stage' can only be 'dev' or 'prod'
	"""
	for hub_id in range(len(yaml_d['stages'][stage])):
		try:
			for port in yaml_d['stages'][stage][hub_id]:
				if yaml_d['stages'][stage][hub_id][port] == None:
					#print("free port found, on return:", dict(hub = hub['name'], port = port))
					return dict(hub_id = hub_id, port = port)
		except TypeError:
			pass
		except KeyError:
			pass

# deploy phone
def deploy_phone(yaml_d: dict)-> bool:
	"""
	Deploy an existing phone by asking user for input\n
	1) Ask user for what stage he wants between 'dev' or 'prod' as deployment stage\n
	2) Search for a free port in 'stages'[stage][hubs]\n
	3) Ask user to chose a phone from undeployed elements of 'phones'\n
	4) Update 'deployed' and 'deploy_path' attributes from 'phones'[phone]\n
	5) Copy information of 'phones'[phone] in a new ruamel.yaml commented map\n
	6) Set a ruamel.yaml Anchor and store a reference to it in the free port found in 'stages'[stage][hubs]\n
	7) Update the yaml file according to previous changes.
	"""
	
	exist = False
	list_phones = set()
	print('Stage to deploy:')
	print('1: Production')
	print('2: Development')
	ret = input('? ')
	if ret == '1':
		stage = 'prod'
	elif ret == '2':
		stage = 'dev'
	else:
		print('Unknown selection')
		return False

	free_port = _find_free_port(stage, yaml_d)
	if free_port != None:
		print('Phone to deploy: ')
		for phone in yaml_d['phones']:
			if not yaml_d['phones'][phone]['deployed']:
				list_phones.add(phone)

		list_phones = list(list_phones)
		for phone_index, phone in enumerate(list_phones):
			print(str(phone_index) + ': ' + yaml_d['phones'][phone]['name'])
			print('\t' + yaml_d['phones'][phone]['vendor'] + ' ' + yaml_d['phones'][phone]['family'] + ' ' + str(yaml_d['phones'][phone]['version']))
		indx = input('? ')
		if indx == '' or int(indx) > len(list_phones) or int(indx) < 0:     # trash, faire un try/except plutot
			return False
		# ajouter try/ except !!!! erreur si on n'entre pas le bon nombre
		selected_phone = list_phones[int(indx)]

		yaml_d['phones'][selected_phone]['deployment_path']['status'] = stage
		yaml_d['phones'][selected_phone]['deployment_path']['hub'] = free_port['hub_id']
		yaml_d['phones'][selected_phone]['deployment_path']['port'] = free_port['port']

		# defining the yaml anchor (one version if testrun_ids defined, and one version if testrun_ids not defined)
		if 'testrun_ids' in yaml_d['phones'][selected_phone]: # version with testrun_ids defined
				yaml_d['phones'][selected_phone] = ruamel.yaml.CommentedMap(
									name = yaml_d['phones'][selected_phone]['name'],
									manufacturer = yaml_d['phones'][selected_phone]['manufacturer'],
									model =  yaml_d['phones'][selected_phone]['model'],
									vendor = yaml_d['phones'][selected_phone]['vendor'],
									family = yaml_d['phones'][selected_phone]['family'],
									version = yaml_d['phones'][selected_phone]['version'],
									platform = yaml_d['phones'][selected_phone]['platform'],
									release_type = yaml_d['phones'][selected_phone]['release_type'],
									ip = yaml_d['phones'][selected_phone]['ip'],
									udid = yaml_d['phones'][selected_phone]['udid'],
									user = yaml_d['phones'][selected_phone]['user'],
									deployed = yaml_d['phones'][selected_phone]['deployed'],
									deployment_path = yaml_d['phones'][selected_phone]['deployment_path'],
									testrun_ids = yaml_d['phones'][selected_phone]['testrun_ids']
									)
		
		else:	# version with testrun_ids undefined
			yaml_d['phones'][selected_phone] = ruamel.yaml.CommentedMap(
									name = yaml_d['phones'][selected_phone]['name'],
									manufacturer = yaml_d['phones'][selected_phone]['manufacturer'],
									model =  yaml_d['phones'][selected_phone]['model'],
									vendor = yaml_d['phones'][selected_phone]['vendor'],
									family = yaml_d['phones'][selected_phone]['family'],
									version = yaml_d['phones'][selected_phone]['version'],
									platform = yaml_d['phones'][selected_phone]['platform'],
									release_type = yaml_d['phones'][selected_phone]['release_type'],
									ip = yaml_d['phones'][selected_phone]['ip'],
									udid = yaml_d['phones'][selected_phone]['udid'],
									user = yaml_d['phones'][selected_phone]['user'],
									deployed = yaml_d['phones'][selected_phone]['deployed'],
									deployment_path = yaml_d['phones'][selected_phone]['deployment_path']
									)

		yaml_d['phones'][selected_phone].yaml_set_anchor(selected_phone, always_dump=True)
		yaml_d['stages'][stage][free_port['hub_id']][free_port['port']] = yaml_d['phones'][selected_phone]
		yaml_d['phones'][selected_phone]['deployed'] = True

		print('Phone deployed to ' + str(free_port['port']) + ' at hub ' + str(yaml_d['stages'][stage][free_port['hub_id']]['name']))
		print('Please connect phone as soon as possible')

		with open(file_name, 'w') as yaml_file:
			yaml.default_flow_style = False
			yaml.dump(yaml_d, yaml_file)
	else:
		print('No free port at stage ' + stage)
	return True

