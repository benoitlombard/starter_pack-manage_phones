###!/usr/bin/env python3

#from types import new_class
import ruamel.yaml #as yaml
import sys
import click

file_name = 'test.yaml'
#file_name = '../components/commons/rtc_configuration.yaml'

with open(file_name, 'r') as yaml_file:
	yaml = ruamel.yaml.YAML(typ='rt')
	yaml_d = yaml.load(yaml_file)

def check_deployed(udid):
	for stage in 'prod', 'dev':
		for hub in yaml_d['stages'][stage]:
			try:
				for port in hub:
					print("inspection, port =", port)
					try:
						if str(udid) == str(yaml_d['stages'][stage][hub][port]['udid']):
							return True, stage, hub['name'], port # Description : true/false, hub_name, port_name
					except TypeError:
						pass
			except TypeError:
				pass
	return False, '', '', '', ''

# Add phone
def get_unused_name():
	used = []
	for name in yaml_d['phones']:
		used.append(yaml_d['phones'][name]['name'])
	with open('gods.txt', 'r') as gods:
		for god in gods:
			god_name = god.rstrip()
			if not god_name in used:
				new_name = god_name
				break
	return new_name

def get_ip():
	for last_digit_ip in range(yaml_d['rtc_params']['min_ip'], yaml_d['rtc_params']['max_ip']+1):
		found = False
		for phone in yaml_d['phones']:
			if last_digit_ip == int(yaml_d['phones'][phone]['ip'].split('.')[3]):
				found = True
				break
		if found == False:
			return last_digit_ip

def CM(**kw):
    return ruamel.yaml.comments.CommentedMap(**kw)

def add_phone():
	yaml_name = get_unused_name()
	print('RTC device name: ' + yaml_name)
	# TODO create selection
	print('Vendor:')
	vendor = input('? ')
	while vendor == '':
		print('Vendor must be set')
		vendor = input('? ')
	print('Family:')
	family = input('? ')
	while family == '':
		print('Family must be set')
		family = input('? ')
	print('Version:')
	version = input('? ')
	while version == '':
		print('Version must be set')
		version = input('? ')
	if vendor == 'Apple':
		platform = 'ios'
	else:
		platform = 'android'
	print('Platform set to: ' + platform)
	print('Release type:')
	print('1: PU1')
	print('2: PU100')
	ret = input('? ')
	while ret != '1' and ret != '2':
		print('Please select a for PU1 or b for PU100')
		ret = input('? ')
	if ret == '1':
		releasetype = 'PU1'
	elif ret == '2':
		releasetype = 'PU100'
	ip = '192.168.5.' + str(get_ip())
	print('IP used: ' + ip)
	print('UDID:')
	udid = input('? ')
	while udid == '':
		print('UDID must be set')
		udid = input('? ')
	for phone in yaml_d['phones']:
		if yaml_d['phones'][phone]['udid'] == udid:
			print('Phone with ' + udid + ' already exists')
			return False
	user = 'rtc-' + yaml_name + '@cobi.bike'

	"""
	New infos in yaml file's 'phone' section: 
		
							deployed: True/False
							deployment_path:
								status: 'dev' / 'prod' / None
								hub:	str / None
								port: str / None
	"""
	deployed = False #This condition is always verified because of 'print('Phone with ' + udid + ' already exists')' verification
	deployment_path = dict(status = None, hub = None, port = None)

	print('Add testrun ids?')
	if input('y|n ') == 'y':
		fota = input('fota: ')
		activitytracking = input('activitytracking: ')
		functional = input('functional: ')
		performance = input('performance: ')
		testrun_ids = dict(fota = fota, activitytracking = activitytracking, functional = functional, performance = performance)

		new_record = CM(name = yaml_name, manufacturer = None, model = None, vendor = vendor, family = family, version = version, platform = platform, release_type = releasetype, ip = ip, udid = udid, user = user, deployed = deployed, deployment_path = deployment_path, testrun_ids = testrun_ids)
	else:
		new_record = CM(name = yaml_name, manufacturer = None, model = None, vendor = vendor, family = family, version = version, platform = platform, release_type = releasetype, ip = ip, udid = udid, user = user, deployed = deployed, deployment_path = deployment_path)
	
	if input('add entry to yaml? y|n ') == 'y':
		yaml_d['phones'][yaml_name] = new_record # operate name change here

		with open(file_name, 'w') as yaml_file:
			yaml.default_flow_style = False
			yaml.dump(yaml_d, yaml_file)
	return True


# change phone
def change_phone():
	l = {}
	print('Phone to change: ')
	for phone_index, phone in  enumerate(yaml_d['phones']):
		l[phone_index] = phone
		print(str(phone_index) + ': ' + yaml_d['phones'][phone]['name'])
		print('\t' + yaml_d['phones'][phone]['vendor'] + ' ' + yaml_d['phones'][phone]['family'] + ' ' + str(yaml_d['phones'][phone]['version']))
	idx = input('? ')
	phone = l[int(idx)]
	#print(yaml.round_trip_dump(phone))
	yaml.dump(phone, sys.stdout)
	print('What to change')
	print('1: Release type')
	print('2: User')
	print('3: Testrun id\'s')
	ret = input('? ')
	if ret == '1':
		print('Release type:')
		print('1: PU1')
		print('2: PU100')
		ret = input('? ')
		while ret != '1' and ret != '2':
			print('Please select a for PU1 or b for PU100')
			ret = input('? ')
		if ret == '1':
			releasetype = 'PU1'
		elif ret == '2':
			releasetype = 'PU100'
		yaml_d['phones'][phone]['release_type'] = releasetype
	elif ret == '2':
		print('New user: (complete string)')
		user = input('? ')
		yaml_d['phones'][phone]['user'] = user
	elif ret == '3':
		fota = input('fota: ')
		activitytracking = input('activitytracking: ')
		functional = input('functional: ')
		performance = input('performance: ')
		testrun_ids = dict(fota = fota, activitytracking = activitytracking, functional = functional, performance = performance)
		yaml_d['phones'][phone]['testrun_ids'] = testrun_ids
	else:
		print('Unknown selection')

	with open(file_name, 'w') as w:
		#w.write(yaml.round_trip_dump(yaml_d))
		yaml.dump(yaml_d, w)



# remove phone
def remove_phone():
	"""
	Remove an existing phone by asking user for input\n
	remove_phone will check if the phone is deployed and undeploy it if necessary befor removing it 
	"""
	print('Enter phone name')
	phone = input('? ')
	if phone in yaml_d['phones']:
		print('Sure to remove ' + phone + ' from test inventory?')
		print('You can just undeploy from test stages.')
		if input('enter yes if are sure: ') == 'yes':
			if yaml_d['phones'][phone]['deployed']:
				undeploy_phone(phone)
			del yaml_d['phones'][phone]
			with open(file_name, 'w') as w:
					yaml.dump(yaml_d, w)
		return
	print(phone + ' not found')


# deploy phone
def find_free_port(stage: str)->dict:
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

def deploy_phone()-> bool:
	"""
	Deploy an existing phone by asking user for input\n
	1) Ask user for what stage he wants between 'dev' or 'prod' as stage\n
	2) Search for a free port in 'stages'[stage][hubs]\n
	3) Ask user to chose a phone from undeployed elements of 'phones'\n
	4) Update 'deployed' and 'deploy_path' attributes from 'phones'[phone]\n
	5) Copy information of 'phones'[phone] in a new ruamel.yaml commented map\n
	6) Set a ruamel.yaml Anchor and store a reference to it in the free port found in 'stages'[stage][hubs]\n
	7) Update the yaml file according to previous changes.
	"""

	exist = False
	l = set()
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

	free_port = find_free_port(stage)
	if free_port != None:
		print('Phone to deploy: ')
		for phone in yaml_d['phones']:
			if not yaml_d['phones'][phone]['deployed']:
				l.add(phone)

		l = list(l)
		for phone_index, phone in enumerate(l):
			print(str(phone_index) + ': ' + yaml_d['phones'][phone]['name'])
			print('\t' + yaml_d['phones'][phone]['vendor'] + ' ' + yaml_d['phones'][phone]['family'] + ' ' + str(yaml_d['phones'][phone]['version']))
		idx = input('? ')
		if idx == '':
			return False
		selected_phone = l[int(idx)]

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

		with open(file_name, 'w') as yaml_file:
			yaml.default_flow_style = False
			yaml.dump(yaml_d, yaml_file)

		yaml_d['phones'][selected_phone]['deployed'] = True
		print('Phone deployed to ' + str(free_port['port']) + ' at hub ' + str(yaml_d['stages'][stage][free_port['hub_id']]['name']))
		print('Please connect phone as soon as possible')

		with open(file_name, 'w') as w:
			yaml.dump(yaml_d, w)
	else:
		print('No free port at stage ' + stage)
	return True
		
# undeploy phone
def undeploy_phone(phone: str) -> None:
	"""
	Undeploy phone from 'stage', given his name
	"""

	print(phone)
	while phone == '':
		l = {}
		print('Phone to undeploy: ')
		for i, inspected_phone in  enumerate(yaml_d['phones']):
			if yaml_d['phones'][inspected_phone]['deployed']:
				l[i] = yaml_d['phones'][inspected_phone]['name']
				print(str(i) + ': ' + yaml_d['phones'][inspected_phone]['name'])
		idx = input('? ')
		phone = l[int(idx)]
	if yaml_d['phones'][phone]['deployed']:
		phone_deployment_status = yaml_d['phones'][phone]['deployment_path']['status']
		phone_deployment_hub = yaml_d['phones'][phone]['deployment_path']['hub']
		phone_deployment_port = yaml_d['phones'][phone]['deployment_path']['port']
		try:
			yaml_d['stages'][phone_deployment_status][phone_deployment_hub][phone_deployment_port] = None
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

def show_stage(stage):
	for hub in yaml_d['stages'][stage]:
		yaml.dump(hub, sys.stdout)

def list_phones():
	print('1: all')
	print('2: by model')
	print('3: by platform')
	ret = input('? ')
	if ret == '1':
		yaml.dump(yaml_d['phones'], sys.stdout)
	elif ret == '2':
		vendor = set()
		for phone in yaml_d['phones']:
			vendor.add(yaml_d['phones'][phone]['vendor'])
		vendor = list(vendor)
		for i, val in enumerate(vendor):
			print(str(i) + ': ' + val)
		sel_vendor = vendor[int(input('Select vendor: '))]

		family = set()
		for phone in yaml_d['phones']:
			if sel_vendor == yaml_d['phones'][phone]['vendor']:
				family.add(yaml_d['phones'][phone]['family'])
		family = list(family)
		for i, val in enumerate(family):
			print(str(i) + ': ' + val)
		print(str(i+1) + ': All')
		ret = int(input('Select family: '))
		if ret == i+1:
			for phone in yaml_d['phones']:
				if sel_vendor == yaml_d['phones'][phone]['vendor']:
					yaml.dump(yaml_d['phones'][phone], sys.stdout)
			return
		elif ret <= i:
			sel_family = family[ret]

		version = set()
		for phone in yaml_d['phones']:
			if sel_vendor == yaml_d['phones'][phone]['vendor'] and sel_family == yaml_d['phones'][phone]['family']:
				version.add(yaml_d['phones'][phone]['version'])
		version = list(version)
		for i, val in enumerate(version):
			print(str(i) + ': ' + str(val))
		print(str(i+1) + ': All')
		ret = int(input('Select version: '))
		if ret == i+1:
			for phone in yaml_d['phones']:
				if sel_vendor == yaml_d['phones'][phone]['vendor'] and sel_family == yaml_d['phones'][phone]['family']:
					#print(yaml.round_trip_dump(yaml_d['phones'][i]))
					yaml.dump(yaml_d['phones'][phone], sys.stdout)
		elif ret <= i:
			for phone in yaml_d['phones']:
				if sel_vendor == yaml_d['phones'][phone]['vendor'] and sel_family == yaml_d['phones'][phone]['family'] and version[ret] == yaml_d['phones'][phone]['version']:
					#print(yaml.round_trip_dump(yaml_d['phones'][i]))
					yaml.dump(yaml_d['phones'][phone], sys.stdout)

	elif ret == '3':
		l = set()
		for phone in yaml_d['phones']:
			l.add(yaml_d['phones'][phone]['platform'])
		l = list(l)
		for i, v in enumerate(l):
			print(str(i) + ': ' + v)
		ret = input('? ')
		platform = l[int(ret)]
		for phone in yaml_d['phones']:
			if yaml_d['phones'][phone]['platform'] == platform:
				yaml.dump(yaml_d['phones'][phone], sys.stdout)

def list_from_yaml(yaml_list_key):
	yaml.dump(yaml_d[yaml_list_key], sys.stdout)
	return

def display():
	print('1: List phones')
	print('2: List all bts')
	print('3: List all biab')
	print('4: List production stage')
	print('5: List development stage')
	print('6: Show undeployed phones')
	print('7: Show configuration of phone')
	ret = input('? ')
	if ret == '1':
		list_phones()
	elif ret == '2':				#new function
		list_from_yaml('bts')
	elif ret == '3':				#new function (same as previous)
		list_from_yaml('biab')
	elif ret == '4':
		show_stage('prod')
	elif ret == '5':
		show_stage('dev')
	elif ret == '6':				#deleted call to check_deployed (optimizing)
		print('Not deployed phones:')
		for phone in yaml_d['phones']:
			if not yaml_d['phones'][phone]['deployed']:
				print(yaml_d['phones'][phone])
	elif ret == '7':				#new function
		print('Phone to show: ')
		ret = input('? ')
		for phone in yaml_d['phones']:
			if yaml_d['phones'][phone]['name'] == ret:
				yaml.dump(yaml_d['phones'][phone], sys.stdout)
				return
		print("Phone not found.")

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
			add_phone()
		elif ret == '2':
			change_phone()
		elif ret == '3':
			deploy_phone()
		elif ret == '4':
			undeploy_phone('')
		elif ret == '5':
			remove_phone()
		elif ret == '6':
			display()