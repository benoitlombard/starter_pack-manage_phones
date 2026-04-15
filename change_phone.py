import sys
from manage_phones import yaml_d, yaml, file_name

# change phone
def change_phone(yaml_d: dict = yaml_d)->None:
	"""
	Allows user to change some informations from 'phones' data by asking which phone and what value of attribute he want to change
	"""
	dict_of_phones = {}
	print('Phone to change: ')
	for phone_index, phone in  enumerate(yaml_d['phones']):
		dict_of_phones[phone_index] = phone
		print(str(phone_index) + ': ' + yaml_d['phones'][phone]['name'])
		print('\t' + yaml_d['phones'][phone]['vendor'] + ' ' + yaml_d['phones'][phone]['family'] + ' ' + str(yaml_d['phones'][phone]['version']))
	indx = input('? ')
	try:
		phone = dict_of_phones[int(indx)]
	except:
		print('Unknown selection')
		return
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
		yaml.dump(yaml_d, w)
