# -*- coding: utf-8 -*-
import click

from __version__ import __version__ as version
from commands.export import export
from commands.import_cmd import import_cmd


@click.group()
@click.version_option(version=version)
def main():
    """Utilities for Google Cloud Datastore."""
    pass


main.add_command(export)
main.add_command(import_cmd)
