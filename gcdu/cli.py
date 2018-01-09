# -*- coding: utf-8 -*-
import click
import export_kind
from __version__ import __version__ as version


@click.group()
@click.version_option(version=version)
def main():
    """Utilities for Google Cloud Datastore."""
    pass


@main.command()
@click.option('--from-project', '-fp',
              help='Origin GCP Project.',
              required=True)
@click.option('--from-namespace', '-fn',
              help='Origin Datastore namespace.',
              required=True)
@click.option('--to-project', '-tp',
              help='Destination GCP Project.',
              required=True)
@click.option('--to-namespace', '-tn',
              help='Destination Datastore namespace.',
              required=True)
@click.option('--skip-export',
              help='Skip the export process from origin database.',
              required=True,
              is_flag=True,
              default=False,
              show_default=True)
@click.option('--skip-import',
              help='Skip the import process to destination database',
              required=True,
              is_flag=True,
              default=False,
              show_default=True)
@click.option('--export-data-dir', help='Directory used to store exported data files.',
              required=True,
              default='./data',
              show_default=True)
@click.option('--kinds',
              help='Comma separated list of Datastore Kinds to use.',
              required=True)
def migrate(from_project, from_namespace, to_project, to_namespace, skip_export, skip_import, export_data_dir, kinds):
    """Migrate data from one namespace to another."""
    kinds_list = kinds.split(',')

    click.echo("Executing migration from '{}.{}' to '{}.{}'. Kinds: '{}'"
               .format(from_project, from_namespace, to_project, to_namespace, kinds))
    click.echo("Storing export data in '{}' directory."
               .format(export_data_dir))

    click.echo("Starting...")

    if not skip_export:
        with click.progressbar(kinds_list, label='Exporting',
                               show_eta=False, item_show_func=show_progressbar_item) as bar:
            for kind in bar:
                export_kind.run(from_project, from_namespace, to_project, to_namespace, export_data_dir, kind)

    if not skip_import:
        with click.progressbar(kinds_list, label='Importing',
                               show_eta=False, item_show_func=show_progressbar_item) as bar:
            for kind in bar:
                # TODO: Implement import feature.
                pass

    click.echo("Finished!")


def show_progressbar_item(item):
    return 'Kind: {}'.format(item)
