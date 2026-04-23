import typer
import time
import sys

from manage_phones import yaml_d, yaml, file_name

# importing other functions
from add_phone import add_phone                                     # CLI function : add
from remove_undeploy_phone import undeploy_phone, remove_phone      # CLI functions : deploy, remove
from change_phone import change_phone                               # CLI function : change
from deploy_phone import deploy_phone                               # CLI function : deploy
from display_infos import _list_from_yaml, _show_stage              # CLI function : lists

phone_management_app = typer.Typer()

# add
@phone_management_app.command("add")
def add(vendor: str = '', family: str = '', version: str = '', udid: str = '', user: str = '',
        release_type: str = 'PU1', write: bool = True, fota: str = None, activitytracking: str = None,
        functional: str = None, performance: str = None, manufacturer: str = None, model: str = None)->None:
    """
    Allows the user to add a new phone through CLI\n
    The information will be stored in the yaml file by default, except if optional argument write is set to False.\n
    Examples of use:     'python manage_phones_CLI.py add --vendor Apple --family ios3.0 --version 4.5 --udid Arwschio4cb8ac-cc4 --user john --release-type PU100
                         'python manage_phones_CLI.py add --vendor Microsoft --family msft --version 2 --udid udid-Arwschio4cb8ac-cc4 --user johnny --release-type PU1 --write --manufacturer microsoft
                         'python manage_phones_CLI.py add --vendor Microsft --family msft --version 2 --udid udid-Arwschiddddd8888ac-cc4 --user johnny --manufacturer microsoft --fota fota_id_112 --activitytracking 44
                         'python manage_phones_CLI.py add --vendor Microsoft --family msft --version 2 --udid udid-test-cc4 --user johnny --release-type PU1 --manufacturer microsoft --no-write
    """
    add_phone(yaml_d = yaml_d, yaml = yaml, file_name = file_name, vendor = vendor, family = family,
            version = version, udid = udid, user = user, releasetype = release_type, write = write,
            fota = fota, activitytracking = activitytracking, functional = functional,
            performance = performance, manufacturer = manufacturer, model = model, call_from_CLI = True)

# undeploy
@phone_management_app.command("undeploy")
def undeploy(phone: str = '')->None:
    """
    Undeploy phone from 'stage', given his name\n
    Examples of use:        'python manage_phones_CLI.py undeploy --phone Aither
    """
    undeploy_phone(yaml_d = yaml_d, yaml = yaml,
                   file_name = file_name, phone = phone,
                   call_from_CLI = True)

# remove
@phone_management_app.command("remove")
def remove(phone: str = '')->None:
    """
    Remove phone from 'stage' entry, given his name\n
    Examples of use:        'python manage_phones_CLI.py remove --phone Erebos
    """
    remove_phone(yaml_d = yaml_d, yaml = yaml,
                 file_name = file_name, phone = phone,
                 call_from_CLI = True)

# change
@phone_management_app.command("change")
def change(phone: str = '', release_type: str = '', user: str = '', fota: str = '', activitytracking: str = '',
           functional: str = '', performance: str = '', manufacturer: str = '', model: str = '',
           vendor: str = '', family: str = '', version: str = '', platform: str = '', ip: str = '',
           udid: str = '', deployed: str = '', status: str = '', hub: str = '', port: str = '')->None:
    """
    Change one or more value of a phone's data given his name\n
    Examples of use:        'python manage_phones_CLI.py change --phone Chaos --release-type PU100 --user jean
                            'python manage_phones_CLI.py change --phone Chaos --fota fota_id
                            'python manage_phones_CLI.py change --version 1.0 --manufacturer Samsung --phone Chaos --release-type PU100 --user jean-pierre --udid udid_test --status prod
                            'python manage_phones_CLI.py change --version 1.0 --manufacturer Samsung --phone Nyx --release-type PU1 --user jean-claude --udid udid_223 --status dev --activitytracking test_activitytracking --performance 4 --platform android_18.1
                            'python manage_phones_CLI.py change --version 8.1 --manufacturer Ssg --phone Nyx --release-type PU100 --user zidane --udid udid_0 --activitytracking test_2 --performance 11 --platform android_19.0
    """
    if all(attribute == '' for attribute in [release_type, user, fota, activitytracking, functional, performance, manufacturer, model, vendor, family, version, platform, ip, udid, deployed, status, hub, port]):
        typer.secho('No values to change !', fg=typer.colors.BRIGHT_RED)
        return
    change_phone(yaml_d = yaml_d, yaml = yaml, file_name = file_name, phone = phone, release_type = release_type, user = user,
                 fota = fota, functional = functional, activitytracking = activitytracking, performance = performance,
                 manufacturer = manufacturer, model = model, vendor = vendor, family = family, version = version, platform = platform,
                 ip = ip, udid = udid, deployed = deployed, status = status, hub = hub, port = port, call_from_CLI = True)

# deploy
@phone_management_app.command("deploy")
def deploy(phone: str = '', stage: str = '')->None:
    """
    Deploy a phone given his name and the stage it should be deployed at\n
    Examples of use:        'python manage_phones_CLI.py deploy --phone Chaos --stage dev
                            'python manage_phones_CLI.py deploy --phone Chaos --stage prod
    """
    deploy_phone(yaml_d = yaml_d, yaml = yaml,
                 file_name = file_name, phone = phone,
                 stage = stage, call_from_CLI = True)

# show_config
@phone_management_app.command("show_config")
def show_config(phone: str = '', mesure_time: bool = True)->None:
    """
    Show the detailed data of a phone data given his name\n
    Examples of use:        'python manage_phones_CLI.py show_config --phone Chaos
    """
    if mesure_time:
        time_origin = time.time()
    try:
        yaml.dump(yaml_d['phones'][phone], sys.stdout)
        if mesure_time:
            typer.secho(f"time elapsed: {(time.time() - time_origin):.6f} seconds.", fg=typer.colors.BRIGHT_BLACK)
    except:
        typer.secho(f'{phone} not found.', fg=typer.colors.RED)
        if mesure_time:
            typer.secho(f"time elapsed: {(time.time() - time_origin):.6f} seconds.", fg=typer.colors.BRIGHT_BLACK)

# lists
@phone_management_app.command("lists")
def lists(item_to_show: str = '', stage_to_show: str = '', mesure_time: bool = True)->None:
    """
    Print available data in yaml file given item-to-show parameter and stage-to-show parameter if the item is a stage\n
    Examples of use:        'python manage_phones_CLI.py lists --item-to-show phones
                            'python manage_phones_CLI.py lists --item-to-show bts
                            'python manage_phones_CLI.py lists --item-to-show biab
                            'python manage_phones_CLI.py lists --item-to-show stage --stage-to-show dev
                            'python manage_phones_CLI.py lists --item-to-show undeployed_phones
    """
    match item_to_show.lower():
        case 'phones':
            if mesure_time:
                time_origin = time.time()
            yaml.dump(yaml_d['phones'], sys.stdout)
            if mesure_time:
                typer.secho(f"time elapsed: {(time.time() - time_origin):.6f} seconds.", fg=typer.colors.BRIGHT_BLACK)
        case 'bts' | 'biab':
            _list_from_yaml(yaml_d = yaml_d,
                            yaml = yaml,
                            yaml_list_key = item_to_show.lower())
        case 'stage':
            try:
                _show_stage(yaml_d = yaml_d,
                            yaml = yaml,
                            stage = stage_to_show.lower())
            except KeyError as err:
                typer.secho(f"KeyError: makes sure 'stage' value is either 'dev' or 'prod'.", fg=typer.colors.RED)
                raise err
        case 'undeployed_phones':
            if mesure_time:
                time_origin = time.time()
            for phone in yaml_d['phones']:
                if not yaml_d['phones'][phone]['deployed']:
                    print(yaml_d['phones'][phone])
            if mesure_time:
                typer.secho(f"time elapsed: {(time.time() - time_origin):.6f} seconds.", fg=typer.colors.BRIGHT_BLACK)
        case _:
            typer.secho(f"Error: User input do not match selection: '{item_to_show}'.", fg=typer.colors.RED)

phone_management_app()
