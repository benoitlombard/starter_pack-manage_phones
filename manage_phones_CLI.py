#imports
import typer
import time
import sys

from manage_phones import yaml_d, yaml, file_name

# importing other functions
from add_phone import add_phone		 # CLI function : add
from remove_undeploy_phone import undeploy_phone, remove_phone	 # CLI function : reploy, remove
from change_phone import change_phone	 # CLI function : change
from deploy_phone import deploy_phone	 # CLI function : deploy
from display_infos import _list_from_yaml, _show_stage	# displaying infos

phone_management_app = typer.Typer()

# error_method
def error_method(args: list['message': str, 'is_success':bool])->bool:
	"""
	Print error/success message formated GREEN/RED using Typer module.\n
	parameters of function: tuple= (message: str, is_success: bool)
	"""
	message = args[0]
	is_success = args[1]
	if is_success:
		typer.secho(message, fg=typer.colors.GREEN)
		return True
	else:
		typer.secho(message, fg=typer.colors.RED)
		return False

# add
@phone_management_app.command()
def add(vendor: str = '', family: str = '', version: str = '', udid: str = '', user: str = '', release_type: str = 'PU1', write: str = True, fota: str = None, activitytracking: str = None,  functional: str = None, performance: str = None, manufacturer: str = None, model: str = None, mesure_time: bool = True)-> bool:
	"""
	Allows the user to add a new phone through CLI\n
	The informations will be stored in the yaml file by default, except if optional argument write is set to False.\n
	Exemples of use:     'python manage_phones_CLI.py add --vendor Apple --family ios3.0 --version 4.5 --udid Arwschio4cb8ac-cc4 --user john --release-type PU100
                         'python manage_phones_CLI.py add --vendor Microsoft --family msft --version 2 --udid udid-Arwschio4cb8ac-cc4 --user johnny --release-type PU1 --write True --manufacturer microsoft
						 'python manage_phones_CLI.py add --vendor Microsft --family msft --version 2 --udid udid-Arwschiddddd8888ac-cc4 --user johnny --manufacturer microsoft --fota fota_id_112 --activitytracking 44
	"""
	if mesure_time:
		time_origin = time.time()
	ret = error_method(add_phone(vendor, family, version, udid, user, release_type, write, fota, activitytracking,  functional, performance, manufacturer, model, yaml_d, True))
	if mesure_time:
		typer.secho(f"time elapsed: {(time.time() - time_origin):.6f} seconds.", fg=typer.colors.BRIGHT_BLACK)
	return ret

#undeploy
@phone_management_app.command()
def undeploy(phone: str = '', mesure_time: bool = True)->bool:
	"""
	Undeploy phone from 'stage', given his name\n
	Exemples of use:        'python manage_phones_CLI.py undeploy --phone Aither
	"""
	if mesure_time:
		time_origin = time.time()
	ret = error_method(undeploy_phone(phone, yaml_d, True))
	if mesure_time:
		typer.secho(f"time elapsed: {(time.time() - time_origin):.6f} seconds.", fg=typer.colors.BRIGHT_BLACK)
	return ret

#remove
@phone_management_app.command()
def remove(phone: str = '', mesure_time: bool = True)->bool:
	"""
	Remove phone from 'stage' entry, given his name\n
	Exemples of use:        'python manage_phones_CLI.py remove --phone Erebos
	"""
	if mesure_time:
		time_origin = time.time()
	ret = error_method(remove_phone(phone, yaml_d, True))
	if mesure_time:
		typer.secho(f"time elapsed: {(time.time() - time_origin):.6f} seconds.", fg=typer.colors.BRIGHT_BLACK)
	return ret

# change
@phone_management_app.command()
def change(phone: str = '', release_type: str = '', user: str = '', fota: str = '', activitytracking: str = '',
		   functional: str = '', performance: str = '', manufacturer: str = '', model: str = '',
		   vendor: str = '', family: str = '', version: str = '', platform: str = '', ip: str = '',
		   udid: str = '', deployed: str = '', status: str = '', hub: str = '', port: str = '',
		   mesure_time: bool = True)->bool:
	"""
	Change one or more value of a phone's data given his name\n
	Exemples of use:        'python manage_phones_CLI.py change --phone Chaos --release-type PU100 --user jean
	      			        'python manage_phones_CLI.py change --phone Chaos --fota fota_id
							'python manage_phones_CLI.py change --version 1.0 --manufacturer Samsung --phone Chaos --release-type PU100 --user jean-pierre --udid udid_test --status prod
							'python manage_phones_CLI.py change --version 1.0 --manufacturer Samsung --phone Nyx --release-type PU1 --user jean-claude --udid udid_223 --status dev --activitytracking test_activitytracking --performance 4 --platform android_18.1
							'python manage_phones_CLI.py change --version 8.1 --manufacturer Ssg --phone Nyx --release-type PU100 --user zidane --udid udid_0 --activitytracking test_2 --performance 11 --platform android_19.0
	"""
	if release_type == '' and user == '' and fota == '' and activitytracking == '' and functional == '' and performance == '' and manufacturer == '' and model == '' and vendor == '' and family == '' and version == '' and platform == '' and ip == '' and udid == '' and deployed == '' and status == '' and hub == '' and port == '':
		typer.secho('No values to change !', fg=typer.colors.BRIGHT_RED)
		return False
	if mesure_time:
		time_origin = time.time()
	ret = error_method(change_phone(phone = phone, release_type = release_type, user = user, fota = fota, functional = functional, activitytracking = activitytracking,
					performance = performance, manufacturer = manufacturer, model = model, vendor = vendor, family = family, version = version, platform = platform,
					ip = ip, udid = udid, deployed = deployed, status = status, hub = hub, port = port, yaml_d = yaml_d, call_from_CLI = True))
	if mesure_time:
		typer.secho(f"time elapsed: {(time.time() - time_origin):.6f} seconds.", fg=typer.colors.BRIGHT_BLACK)
	return ret

#deploy
@phone_management_app.command()
def deploy(phone: str = '', stage: str = '', mesure_time: bool = True)->bool:
	"""
	Deploy a phone given his name and the stage it should be deployed at\n
	Exemples of use:        'python manage_phones_CLI.py deploy --phone Chaos --stage dev
	      			        'python manage_phones_CLI.py deploy --phone Chaos --stage prod --no-mesure-time
	"""
	if mesure_time:
		time_origin = time.time()
	ret = error_method(deploy_phone(phone, stage, yaml_d, True))
	if mesure_time:
		typer.secho(f"time elapsed: {(time.time() - time_origin):.6f} seconds.", fg=typer.colors.BRIGHT_BLACK)
	return ret

#show_config
@phone_management_app.command()
def show_config(phone: str = '', mesure_time: bool = True)->bool:
	"""
	Show the detailed data of a phone data given his name\n
	Exemples of use:        'python manage_phones_CLI.py show-config --phone Chaos
	"""
	if mesure_time:
		time_origin = time.time()
	try:
		yaml.dump(yaml_d['phones'][phone], sys.stdout)
		if mesure_time:
			typer.secho(f"time elapsed: {(time.time() - time_origin):.6f} seconds.", fg=typer.colors.BRIGHT_BLACK)
		return True
	except:
		typer.secho(f'{phone} not found.', fg=typer.colors.RED)
		if mesure_time:
			typer.secho(f"time elapsed: {(time.time() - time_origin):.6f} seconds.", fg=typer.colors.BRIGHT_BLACK)
		return False

#lists
@phone_management_app.command()
def lists(item_to_show: str = 'phones', stage_to_show: str = 'prod', mesure_time: bool = True)->bool:
	"""
	Print available data in yaml file given item-to-show parameter and stage-to-show parameter if the item is a stage\n
	Exemples of use:		'python manage_phones_CLI.py lists --item-to-show phones
							'python manage_phones_CLI.py lists --item-to-show bts
							'python manage_phones_CLI.py lists --item-to-show stage
	      			        'python manage_phones_CLI.py lists --item-to-show stage --stage-to-show dev
          			        'python manage_phones_CLI.py lists --item-to-show undeployed_phones
	"""
	if mesure_time:
		time_origin = time.time()
	match item_to_show.lower():
		case 'phones':
			yaml.dump(yaml_d['phones'], sys.stdout)
			ret = True
		case 'bts' | 'biab':
			ret = _list_from_yaml(item_to_show.lower(), yaml_d)
		case 'stage':
			ret = _show_stage(stage_to_show.lower(), yaml_d)
		case 'undeployed_phones':
			for phone in yaml_d['phones']:
				if not yaml_d['phones'][phone]['deployed']:
					print(yaml_d['phones'][phone])
			ret = True
		case _:
			typer.secho(f'Error: Unknown entry: {item_to_show}', fg=typer.colors.RED)
			return False
	if ret:
		if mesure_time:
			typer.secho(f"time elapsed: {(time.time() - time_origin):.6f} seconds.", fg=typer.colors.BRIGHT_BLACK)
		return True
	else:
		typer.secho('Something went wrong.', fg=typer.colors.RED)
		if mesure_time:
			typer.secho(f"time elapsed: {(time.time() - time_origin):.6f} seconds.", fg=typer.colors.BRIGHT_BLACK)
		return False

phone_management_app()
