import sys
from manage_phones import yaml_d, yaml, file_name

# change phone
def change_phone(phone: str, releasetype: str = '', user: str = '', fota: str = '', activitytracking: str = '', functional: str = '', performance: str = '', yaml_d: dict = yaml_d, call_from_CLI: bool = False)->None:
	"""
	Allows user to change some informations from 'phones' data by asking which phone and what value of attribute he want to change
	"""
	while phone == '':
		dict_of_phones = {}
		print('Phone to change: ')
		for phone_index, phone in  enumerate(yaml_d['phones']):
			dict_of_phones[phone_index] = phone
			print(str(phone_index) + ': ' + yaml_d['phones'][phone]['name'])
			print('\t' + yaml_d['phones'][phone]['vendor'] + ' ' + yaml_d['phones'][phone]['family'] + ' ' + str(yaml_d['phones'][phone]['version']))
		indx = input('? ')
		try:
			phone = dict_of_phones[int(indx)]
		except KeyError:
			print('Unknown selection')
			return 1 # KeyError unknown selection
	if not call_from_CLI:
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
			return 1 # KeyError unknown selection
	if call_from_CLI:
		if releasetype != '':
			yaml_d['phones'][phone]['release_type'] = releasetype
		if user != '':
			yaml_d['phones'][phone]['user'] = user
		if fota != '' or activitytracking != '' or functional != '' or performance != '':
			if not 'testrun_ids' in yaml_d['phones'][phone]:
				yaml_d['phones'][phone]['testrun_ids'] = {}
				yaml_d['phones'][phone]['testrun_ids']['fota'] = fota if fota != '' else None
				yaml_d['phones'][phone]['testrun_ids']['activitytracking'] = activitytracking if activitytracking != '' else None
				yaml_d['phones'][phone]['testrun_ids']['functional'] = functional if functional != '' else None
				yaml_d['phones'][phone]['testrun_ids']['performance'] = performance if performance != '' else None
			else:
				if fota != '':
					yaml_d['phones'][phone]['testrun_ids']['fota'] = fota
				if activitytracking != '':
					yaml_d['phones'][phone]['testrun_ids']['activitytracking'] = activitytracking
				if functional != '':
					yaml_d['phones'][phone]['testrun_ids']['functional'] = functional
				if performance != '':
					yaml_d['phones'][phone]['testrun_ids']['performance'] = performance	

	with open(file_name, 'w') as w:
		yaml.dump(yaml_d, w)
		return 0 # success
	return 2 # unknown failure during writing
