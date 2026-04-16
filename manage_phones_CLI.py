#imports
import typer
import ruamel.yaml
import time

from manage_phones import yaml_d, yaml, file_name

from add_phone import _get_ip, _get_unused_name		# CLI function : add
from remove_undeploy_phone import undeploy_phone, remove_phone	 # CLI function : reploy, remove
from change_phone import change_phone	 # CLI function : change


# importing other files
import display_infos	# displaying infos
import deploy_phone		# deploying a phone

phone_management_app = typer.Typer()

# add
@phone_management_app.command()
def add(vendor: str, family: str, version: str, udid: str, user: str, releasetype: str = 'PU1', write: str = True, fota: str = None, activitytracking: str = None,  functional: str = None, performance: str = None, manufacturer: str = None, model: str = None)-> bool:
	"""
	Allows the user to add a new phone through CLI\n
	The informations will be stored in the yaml file by default, except if optional argument write is set to False.\n
	Exemples of use:     'python manage_phones_CLI.py add Apple ios3.0 4.5 Arwschio4cb8ac john
                         'python manage_phones_CLI.py add Samsung s10 12.0 udid-Arwschio4cb8ac john --releasetype PU100 --write True --manufacturer samsung
	"""
	yaml_phone_name =  _get_unused_name(yaml_d)
	if vendor.lower() == 'apple':
		platform = 'ios'
	else:
		platform = 'android'
	ip = _get_ip(yaml_d)
	
    # exit condition number 1
	if ip is None:
		typer.secho("Impossible to add a new phone\nThere is no ip available at the moment", fg=typer.colors.RED)
		return False
	ip = '192.168.5.' + str(ip)
	
    # exit condition number 2
	for phone in yaml_d['phones']:
		if yaml_d['phones'][phone]['udid'] == udid:
			typer.secho(f'Impossible to add a new phone\nPhone with {udid} already exists', fg=typer.colors.RED)
			return False

	user = 'rtc-' + yaml_phone_name + '@cobi.bike'	
    # Success
	typer.secho(f'RTC device name: {yaml_phone_name}', fg=typer.colors.GREEN)
	typer.secho(f'Platform set to: {platform}', fg=typer.colors.GREEN)
	typer.secho(f'IP used: {ip}', fg=typer.colors.GREEN)
	typer.secho(f'User: {user}', fg=typer.colors.GREEN)
	
	deployed = False #This condition is always verified because of 'print('Phone with ' + udid + ' already exists')' verification
	deployment_path = dict(status = None, hub = None, port = None)

	if fota is not None or activitytracking is not None or functional is not None or performance is not None:
		typer.secho('Testrun ids stored', fg=typer.colors.GREEN)
		testrun_ids = dict(fota = fota, activitytracking = activitytracking, functional = functional, performance = performance)
		new_phone_record = ruamel.yaml.CommentedMap(name = yaml_phone_name, manufacturer = manufacturer, model = model, vendor = vendor, family = family, version = version, platform = platform, release_type = releasetype, ip = ip, udid = udid, user = user, deployed = deployed, deployment_path = deployment_path, testrun_ids = testrun_ids)
	else:
		typer.secho('No testrun ids', fg=typer.colors.GREEN)
		new_phone_record = ruamel.yaml.CommentedMap(name = yaml_phone_name, manufacturer = manufacturer, model = model, vendor = vendor, family = family, version = version, platform = platform, release_type = releasetype, ip = ip, udid = udid, user = user, deployed = deployed, deployment_path = deployment_path)

	new_phone_record.yaml_set_anchor(yaml_phone_name, always_dump=True)
	if write:
		yaml_d['phones'][yaml_phone_name] = new_phone_record
		with open(file_name, 'w') as yaml_file:
			yaml.dump(yaml_d, yaml_file)
			typer.secho(f'{yaml_phone_name} successfully writen to yaml', fg=typer.colors.GREEN)
	return True


@phone_management_app.command()
def undeploy(phone: str, mesure_time: bool = True)->bool:
	"""
	Undeploy phone from 'stage', given his name\n
	Exemples of use:        'python manage_phones_CLI.py undeploy Aither
	"""
	if mesure_time:
		time_origin = time.time()
	ret = undeploy_phone(phone, yaml_d, True)
	match ret:
		case 0:
			typer.secho(f'{phone} successfully undeployed.', fg=typer.colors.GREEN)
		case 1:
			typer.secho('Key Error, unknown selection.', fg=typer.colors.RED)
		case 2:
			typer.secho('Key Error when writing to the yaml file.\nUndeployment failed', fg=typer.colors.RED)
		case 3:
			typer.secho(f'{phone} is not deployed.\nUndeployment is not possible', fg=typer.colors.RED)
		
	if mesure_time:
		typer.secho(f"time elapsed: {(time.time() - time_origin):.6f} seconds.", fg=typer.colors.BRIGHT_BLACK)
	if ret > 0:
		return False
	return True


@phone_management_app.command()
def remove(phone: str, mesure_time: bool = True)->bool:
	"""
	Remove phone from 'stage', given his name\n
	Exemples of use:        'python manage_phones_CLI.py remove Erebos
	"""
	if mesure_time:
		time_origin = time.time()
	ret = remove_phone(phone, yaml_d, True)

	match ret:
		case 0:
			typer.secho(f'{phone} successfully removed.', fg=typer.colors.GREEN)
		case 1:
			typer.secho('User aborted phone removal.', fg=typer.colors.RED)
		case 2:
			typer.secho(f'{phone} not found.', fg=typer.colors.RED)

	if mesure_time:
		typer.secho(f"time elapsed: {(time.time() - time_origin):.6f} seconds.", fg=typer.colors.BRIGHT_BLACK)
	if ret > 0:
		return False
	return True


@phone_management_app.command()
def change(phone: str, releasetype: str = '', user: str = '', fota: str = '', activitytracking: str = '', functional: str = '', performance: str = '', mesure_time: bool = True)->bool:
	"""
	Change one or more value of a phone's data given his name\n
	Exemples of use:        'python manage_phones_CLI.py change Chaos --releasetype PU100 --user jean
	      			        'python manage_phones_CLI.py change Chaos --fota fota_id
	"""
	if releasetype == '' and user == '' and fota == '' and activitytracking == '' and functional == '' and performance == '':
		typer.secho('No values to change !', fg=typer.colors.BRIGHT_RED)
		return False
	if mesure_time:
		time_origin = time.time()
	ret = change_phone(phone, releasetype, user, fota, functional, activitytracking, performance, yaml_d, True)

	match ret:
		case 0:
			typer.secho(f'{phone} successfully changed.', fg=typer.colors.GREEN)
		case 1:
			typer.secho('Key Error, unknown selection.', fg=typer.colors.RED)
		case 2:
			typer.secho('Error when writing to the yaml file.', fg=typer.colors.RED)

	if mesure_time:
		typer.secho(f"time elapsed: {(time.time() - time_origin):.6f} seconds.", fg=typer.colors.BRIGHT_BLACK)
	if ret > 0:
		return False
	return True



phone_management_app()
