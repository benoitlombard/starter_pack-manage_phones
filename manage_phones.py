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
	for s in 'prod', 'dev':
		for i in yaml_d['stages'][s]:
			if 'hubs' in i:
				try:
					for k in i['hubs']:
						#for j in i['hubs'][k]['ports']:
						for j in k['ports']:
							#print("inspecting", j, "in i['hubs'][k]['ports']")
							try:
								#print("test if, comparaison entre :", udid, "et :", j['udid'])
								if str(udid) == str(j['udid']):
									j['port'] = None
									#print("test reussi")
									return True, s, i['name'], k['id'], j['id'] # found, mac name, hub name, port
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
			g = god.rstrip()
			if not g in used:
				new_name = g
				break
	return new_name

def get_ip():
	for i in range(yaml_d['rtc_params']['min_ip'], yaml_d['rtc_params']['max_ip']+1):
		found = False
		for j in yaml_d['phones']:
			if i == int(yaml_d['phones'][j]['ip'].split('.')[3]):
				found = True
				break
		if found == False:
			return i

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
	for i in yaml_d['phones']:
		if yaml_d['phones'][i]['udid'] == udid:
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
	
	new_record.yaml_set_anchor(new_record)

	new_record.yaml_set_anchor(yaml_name)
	new_record['self_reference'] = new_record # incroyable
	data = CM(yaml_name=new_record)
	#data[yaml_name] = data.pop('yaml_name') # incroyable
	
	if input('add entry to yaml? y|n ') == 'y':
		yaml_d['phones'][yaml_name] = data['yaml_name'] # operate name change here

		with open(file_name, 'w') as yaml_file:
			yaml.default_flow_style = False
			yaml.dump(yaml_d, yaml_file)
	return True


# change phone
def change_phone():
	l = {}
	print('Phone to change: ')
	for i, val in  enumerate(yaml_d['phones']):
		l[i] = val #l[i] = yaml_d['phones'][val]
		print(str(i) + ': ' + val['name'])
		print('\t' + val['model']['vendor'] + ' ' + val['model']['family'] + ' ' + str(val['model']['version']))
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
		phone['release_type'] = releasetype
	elif ret == '2':
		print('New user: (complete string)')
		user = input('? ')
		phone['user'] = user
	elif ret == '3':
		fota = input('fota: ')
		activitytracking = input('activitytracking: ')
		functional = input('functional: ')
		performance = input('performance: ')
		testrun_ids = dict(fota = fota, activitytracking = activitytracking, functional = functional, performance = performance)
		phone['testrun_ids'] = testrun_ids
	else:
		print('Unknown selection')

	with open(file_name, 'w') as w:
		#w.write(yaml.round_trip_dump(yaml_d))
		yaml.dump(yaml_d, w)



# remove phone
def remove_phone():
	print('Enter phone name')
	phone = input('? ')
	for i in range(len(yaml_d['phones'])):
		if yaml_d['phones'][i]['name'] == phone:
			print('Sure to remove ' + phone + ' from test inventory?')
			print('You can just undeploy from test stages.')
			if input('enter yes if are sure: ') == 'yes':
				undeploy_phone(phone)
				del yaml_d['phones'][i]
				with open(file_name, 'w') as w:
					#w.write(yaml.round_trip_dump(yaml_d))
					yaml.dump(yaml_d, w)
			return
	print(phone + ' not found')


# deploy phone
def find_free_port(stage):
	for i in yaml_d['stages'][stage]:
		try:
			for k in i['hubs']:
				for j in k['ports']:
					if j['port'] == None:
						print("free port found, on return:", dict(macmini = i['name'], hub = k['id'], port = j['id']))
						return dict(macmini = i['name'], hub = k['id'], port = j['id'])
		except TypeError:
			pass
		except KeyError:
			pass

def deploy_phone():
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
		for val in range(len(yaml_d['phones'])):
			f, s, m, h, p = check_deployed(yaml_d['phones'][val]['udid'])
			if not f:
				l.add(val)
			
		l = list(l)
		for i, val in enumerate(l):
			print(str(i) + ': ' + yaml_d['phones'][val]['name'])
			print('\t' + yaml_d['phones'][val]['model']['vendor'] + ' ' + yaml_d['phones'][val]['model']['family'] + ' ' + str(yaml_d['phones'][val]['model']['version']))
		idx = input('? ')
		if idx == '':
			return False
		
		for i in range(len(yaml_d['macmini'])):
			if yaml_d['macmini'][i]['name'] == free_port['macmini'] or yaml_d['macmini'][i]['name'] == None:
				# I added new possibility: ['name'] = None, for allowing deployment right after undeployment (undeployment will now trigger ['name']=None)
				
				print("yaml_d['macmini'][i]['hubs'][free_port['hub']]['ports']", yaml_d['macmini'][i]['hubs'][free_port['hub']]['ports'])
				print("[free_port['port']]", [free_port['port']])
				for id_index in range(len(yaml_d['macmini'][i]['hubs'][free_port['hub']]['ports'])):
					if yaml_d['macmini'][i]['hubs'][free_port['hub']]['ports'][id_index]['id'] == free_port['port']:
						print("index found:", id_index)
						break

				yaml_d['macmini'][i]['name'] = yaml_d['phones'][l[int(idx)]]['name']
				yaml_d['macmini'][i]['hubs'][free_port['hub']]['ports'][id_index]['udid'] = yaml_d['phones'][l[int(idx)]]['udid']
				yaml_d['macmini'][i]['hubs'][free_port['hub']]['ports'][id_index]['port'] = yaml_d['phones'][l[int(idx)]]
				print('Phone deployed to ' + str(free_port['port']) + ' at hub ' + str(free_port['hub']) + ' at mac mini ' + yaml_d['macmini'][i]['name'])
				print('Please connect phone as soon as possible')
		
		with open(file_name, 'w') as w:
			#w.write(yaml.round_trip_dump(yaml_d))
			yaml.dump(yaml_d, w)
	else:
		print('No free port at stage ' + stage)
	return True


# undeploy phone
def undeploy_phone(phone):
	print(phone)
	if phone == '':
		l = {}
		print('Phone to undeploy: ')
		for i, val in  enumerate(yaml_d['phones']):
			l[i] = val['name']
			print(str(i) + ': ' + val['name'])
		idx = input('? ')
		phone = l[int(idx)]

	print("avant la boucle de recherche, phone=", phone)
	for i in yaml_d['phones']:
		print("comparaison entre",phone,"et ", i['name'])
		if i['name'] == phone:
			print("la comparaison passe")
			f, s, m, h, p = check_deployed(i['udid'])
			print("check_deployed en fct du udid, retour=",f,s,m,h,p)
			if f:
				print("on a passe le check True pour check_deployed")
				for j in range(len(yaml_d['stages'][s])):
					print("comparaison (name) entre ", m, " et", yaml_d['stages'][s][j]['name'])
					if yaml_d['stages'][s][j]['name'] == m:
						for k in range(len(yaml_d['stages'][s][j]['hubs'])):
							print("comparaison (hub_id) entre ", h, " et", yaml_d['stages'][s][j]['hubs'][k]['id'])
							if yaml_d['stages'][s][j]['hubs'][k]['id'] == h:
								for l in range(len(yaml_d['stages'][s][j]['hubs'][h]['ports'])):
									print("comparaison (port_id) entre ", h, " et", yaml_d['stages'][s][j]['hubs'][k]['id'])
									if yaml_d['stages'][s][j]['hubs'][k]['ports'][l]['id'] == p:
										print("on est dans le code d'affectation")
										yaml_d['stages'][s][j]['hubs'][h]['ports'][p]['port'] = None #original affectation
										for macmini_index in range(len(yaml_d['macmini'])):
											if yaml_d['macmini'][macmini_index]['name'] == phone:
												print("le nom a ete trouve")
												break
										yaml_d['macmini'][macmini_index]['name'] = None	# proposition of new additional affectation for easier deployment
										for macmini_hub_index in range(len(yaml_d['macmini'][macmini_index]['hubs'])):
											for macmini_port_index in range(len(yaml_d['macmini'][macmini_index]['hubs'][macmini_hub_index]['ports'])):
												try :
													if len(yaml_d['macmini'][macmini_index]['hubs'][macmini_hub_index]['ports'][macmini_port_index]['port']) > 3:
														print("le pointeur de donnees a ete trouve")
														yaml_d['stages'][s][macmini_index]['hubs'][macmini_hub_index]['ports'][macmini_port_index]['port'] = None  # proposition of new additional affectation
														yaml_d['stages'][s][macmini_index]['hubs'][macmini_hub_index]['ports'][macmini_port_index]['udid'] = None  # proposition of new additional affectation
												except:
													print("error when looping to delete")


										with open(file_name, 'w') as w:
											yaml.dump(yaml_d, w)
										print('Please unplug ' + str(phone) + ' from ' + str(p) + ' at hub ' + str(yaml_d['stages'][s][j]['hubs'][h]['id']) + ' at mac mini ' + str(m))

def show_stage(stage):
	for i in yaml_d['stages'][stage]:
		if 'hub_id' in i:
			yaml.dump(i, sys.stdout)

def list_phones():
	print('1: all')
	print('2: by model')
	print('3: by platform')
	ret = input('? ')
	if ret == '1':
		yaml.dump(yaml_d['phones'], sys.stdout)
	elif ret == '2':
		vendor = set()
		for i in range(len(yaml_d['phones'])):
			vendor.add(yaml_d['phones'][i]['model']['vendor'])
		vendor = list(vendor)
		for i, val in enumerate(vendor):
			print(str(i) + ': ' + val)
		sel_vendor = vendor[int(input('Select vendor: '))]

		family = set()
		for i in range(len(yaml_d['phones'])):
			if sel_vendor == yaml_d['phones'][i]['model']['vendor']:
				family.add(yaml_d['phones'][i]['model']['family'])
		family = list(family)
		for i, val in enumerate(family):
			print(str(i) + ': ' + val)
		print(str(i+1) + ': All')
		ret = int(input('Select family: '))
		if ret == i+1:
			for i in range(len(yaml_d['phones'])):
				if sel_vendor == yaml_d['phones'][i]['model']['vendor']:
					yaml.dump(yaml_d['phones'][i], sys.stdout)
					#print(yaml.round_trip_dump(yaml_d['phones'][i]))
			return
		elif ret <= i:
			sel_family = family[ret]

		version = set()
		for i in range(len(yaml_d['phones'])):
			if sel_vendor == yaml_d['phones'][i]['model']['vendor'] and sel_family == yaml_d['phones'][i]['model']['family']:
				version.add(yaml_d['phones'][i]['model']['version'])
		version = list(version)
		for i, val in enumerate(version):
			print(str(i) + ': ' + str(val))
		print(str(i+1) + ': All')
		ret = int(input('Select version: '))
		if ret == i+1:
			for i in range(len(yaml_d['phones'])):
				if sel_vendor == yaml_d['phones'][i]['model']['vendor'] and sel_family == yaml_d['phones'][i]['model']['family']:
					#print(yaml.round_trip_dump(yaml_d['phones'][i]))
					yaml.dump(yaml_d['phones'][i], sys.stdout)
		elif ret <= i:
			for i in yaml_d['phones']:
				if sel_vendor == yaml_d['phones'][i]['model']['vendor'] and sel_family == yaml_d['phones'][i]['model']['family'] and version[ret] == yaml_d['phones'][i]['model']['version']:
					#print(yaml.round_trip_dump(yaml_d['phones'][i]))
					yaml.dump(yaml_d['phones'][i], sys.stdout)

	elif ret == '3':
		l = set()
		for i in yaml_d['phones']:
			l.add(i['platform'])
		l = list(l)
		for i, v in enumerate(l):
			print(str(i) + ': ' + v)
		ret = input('? ')
		platform = l[int(ret)]
		for i in yaml_d['phones']:
			if yaml_d['phones'][i]['platform'] == platform:
				yaml.dump(yaml_d['phones'][i], sys.stdout)

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
		for i in yaml_d['phones']:
			if not i['deployed']:
				print(i['name'])
	elif ret == '7':				#new function
		print('Phone to show: ')
		ret = input('? ')
		for i in range(len(yaml_d['phones'])):
			if yaml_d['phones'][i]['name'] == ret:
				yaml.dump(yaml_d['phones'][i], sys.stdout)
				return

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