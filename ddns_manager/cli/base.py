from typing import Dict

import click
import yaml

from .ddns_updater import ddns_updater
from .public_ip_getter import public_ip_getter
from .error_handler import error_handler

from ddns_manager import DDNSManager


@click.group()
def cli():
    """
    DDNS Manager\n
    Simple, powerful and extensible Dynamic DNS manager
    """


@cli.command()
@click.option("--debug", type=click.types.BOOL, default=False)
@click.argument("file", type=click.types.File(), nargs=1, envvar="CONFIG_FILE")
def loop(file, debug):
    """Keeps DDNS updated according to the configuration provided"""
    click.echo("")

    # Load configuration
    try:
        config_dict = yaml.safe_load(file)
        file.close()
        check_config(config_dict)
    except Exception as ex:
        if debug:
            click.echo(ex)
            click.echo("")
        click.echo("Invalid configuration")
        click.echo("(for more details run command with --debug y)")
        return

    # Setup manager
    pig = public_ip_getter(config=config_dict["public_ip_getter"])
    du = ddns_updater(config=config_dict["ddns_updater"])

    dm = DDNSManager(ip_getter=pig, ddns_updater=du)

    eh = error_handler(config=config_dict["on_error_behaviour"])

    # Starting loop
    dm.update_loop(interval=config_dict["check_interval"], on_error=eh)

    click.echo(config_dict)


def check_config(config: Dict):
    # No need to get worried about different config versions for now
    # version = config.get('version', '0.1.0')

    required_keys = [
        "public_ip_getter",
        "ddns_updater",
        "check_interval",
        "on_error_behaviour",
    ]

    for key in required_keys:
        if key not in config:
            raise AttributeError(f"Invalid configuration file. (Missing '{key}' value)")

    if type(config["check_interval"]) != int:
        raise AttributeError("Parameter 'check_interval' should be a integer number")
