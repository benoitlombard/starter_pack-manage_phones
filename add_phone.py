from manage_phones import *

# Add phone
def get_unused_name(yaml_d: dict)->str:
	"""
	Loop through gods in gods.txt file to return the first unused name in 'phones' from gods.txt
	"""
	list_of_used_names = []
	for phone_name in yaml_d['phones']:
		list_of_used_names.append(yaml_d['phones'][phone_name]['name'])
	with open('gods.txt', 'r') as gods_txt:
		for god in gods_txt:
			god_name = god.rstrip()
			if not god_name in list_of_used_names:
				unused_name = god_name
				break
	return unused_name

def get_ip(yaml_d: dict)->int:
	"""
	Loop through values from 'rtc_params'['min_ip'], 'rtc_params'['max_ip']\n
	And return the first 3 digits number unused as ip's last triple in 'phones'
	"""
	for last_digit_ip in range(yaml_d['rtc_params']['min_ip'], yaml_d['rtc_params']['max_ip']+1):
		found = False
		for phone in yaml_d['phones']:
			if last_digit_ip == int(yaml_d['phones'][phone]['ip'].split('.')[3]):
				found = True
				break
		if found == False:
			return last_digit_ip

def add_phone(yaml_d: dict)->bool:
	"""
	Allows the user to add a new phone by writing phone informations\n
	The informations will be stored in the yaml file
	"""
	yaml_phone_name = get_unused_name(yaml_d)
	print('RTC device name: ' + yaml_phone_name)
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
	ip = '192.168.5.' + str(get_ip(yaml_d))
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
	user = 'rtc-' + yaml_phone_name + '@cobi.bike'

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

		new_phone_record = dict(name = yaml_phone_name, manufacturer = None, model = None, vendor = vendor, family = family, version = version, platform = platform, release_type = releasetype, ip = ip, udid = udid, user = user, deployed = deployed, deployment_path = deployment_path, testrun_ids = testrun_ids)
	else:
		new_phone_record = dict(name = yaml_phone_name, manufacturer = None, model = None, vendor = vendor, family = family, version = version, platform = platform, release_type = releasetype, ip = ip, udid = udid, user = user, deployed = deployed, deployment_path = deployment_path)
	
	if input('add entry to yaml? y|n ') == 'y':
		yaml_d['phones'][yaml_phone_name] = new_phone_record # operate name change here

		with open(file_name, 'w') as yaml_file:
			yaml.default_flow_style = False
			yaml.dump(yaml_d, yaml_file)
	return True

