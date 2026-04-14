from manage_phones import *

from manage_phones import yaml_d

def list_from_yaml(yaml_list_key: str, yaml_d: dict)->None:
	"""
	Function dedicated to print informations in the yaml file that are available with a single key entry: 'biab'/'bts'
	"""
	yaml.dump(yaml_d[yaml_list_key], sys.stdout)
	return

def show_stage(stage: str, yaml_d: dict)->None:
	"""
	Display the content of 'stages'['dev'] or 'stages'['prod'] from yaml file
	"""
	for hub in yaml_d['stages'][stage]:
		yaml.dump(hub, sys.stdout)

def list_phones(yaml_d: dict)->None:
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
		list_of_vendor = set()
		for phone in yaml_d['phones']:
			list_of_vendor.add(yaml_d['phones'][phone]['vendor'])
		vendor = list(list_of_vendor)
		for vendor_index, vendor_val in enumerate(vendor):
			print(str(vendor_index) + ': ' + vendor_val)
		sel_vendor = vendor[int(input('Select vendor: '))]

		list_of_family = set()
		for phone in yaml_d['phones']:
			if sel_vendor == yaml_d['phones'][phone]['vendor']:
				list_of_family.add(yaml_d['phones'][phone]['family'])
		family = list(list_of_family)
		for family_index,family_val in enumerate(family):
			print(str(family_index) + ': ' + family_val)
		print(str(family_index+1) + ': All')
		ret = int(input('Select family: '))
		if ret == family_index+1:
			for phone in yaml_d['phones']:
				if sel_vendor == yaml_d['phones'][phone]['vendor']:
					yaml.dump(yaml_d['phones'][phone], sys.stdout)
			return
		elif ret <= family_index:
			sel_family = family[ret]

		version = set()
		for phone in yaml_d['phones']:
			if sel_vendor == yaml_d['phones'][phone]['vendor'] and sel_family == yaml_d['phones'][phone]['family']:
				version.add(yaml_d['phones'][phone]['version'])
		version = list(version)
		for version_index, val_version in enumerate(version):
			print(str(version_index) + ': ' + str(val_version))
		print(str(version_index) + ': All')
		ret = int(input('Select version: '))
		if ret == version_index + 1:
			for phone in yaml_d['phones']:
				if sel_vendor == yaml_d['phones'][phone]['vendor'] and sel_family == yaml_d['phones'][phone]['family']:
					yaml.dump(yaml_d['phones'][phone], sys.stdout)
		elif ret <= version_index:
			for phone in yaml_d['phones']:
				if sel_vendor == yaml_d['phones'][phone]['vendor'] and sel_family == yaml_d['phones'][phone]['family'] and version[ret] == yaml_d['phones'][phone]['version']:
					yaml.dump(yaml_d['phones'][phone], sys.stdout)

	elif ret == '3':
		list_of_platforms = set()
		for phone in yaml_d['phones']:
			list_of_platforms.add(yaml_d['phones'][phone]['platform'])
		list_of_platforms = list(list_of_platforms)
		for platform_index, platform_val in enumerate(list_of_platforms):
			print(str(platform_index) + ': ' + platform_val)
		ret = input('? ')
		platform = list_of_platforms[int(ret)]
		for phone in yaml_d['phones']:
			if yaml_d['phones'][phone]['platform'] == platform:
				yaml.dump(yaml_d['phones'][phone], sys.stdout)

def display(yaml_d: dict)->None:
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
		list_phones(yaml_d)
	elif ret == '2':				#new function
		list_from_yaml('bts', yaml_d)
	elif ret == '3':				#new function (same as previous)
		list_from_yaml('biab', yaml_d)
	elif ret == '4':
		show_stage('prod', yaml_d)
	elif ret == '5':
		show_stage('dev', yaml_d)
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