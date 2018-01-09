# -*- coding: utf-8 -*-
import click

from __version__ import __version__ as version
from commands.export import export


@click.group()
@click.version_option(version=version)
def main():
    """Utilities for Google Cloud Datastore."""
    pass

main.add_command(export)
