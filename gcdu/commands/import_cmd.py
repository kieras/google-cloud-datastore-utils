# -*- coding: utf-8 -*-
"""The import command."""
import json

import click

from .utils import (get_datastore_api, partition_replace, load, execute_tasks)


@click.command('import')
@click.option('--project', '-p',
              help='GCP project.',
              required=True)
@click.option('--namespace', '-n',
              help='Datastore namespace.',
              required=True)
@click.option('--data-dir',
              help='Directory to be used to store exported files.',
              required=True,
              default='./data',
              show_default=True)
@click.option('--project-placeholder', '-pp',
              help='Placeholder value to replace the project value in'
                   ' previously exported files.',
              required=True,
              default='___PROJECT___',
              show_default=True)
@click.option('--namespace-placeholder', '-np',
              help='Placeholder value to replace the namespace value in'
                   ' previously exported files.',
              required=True,
              default='___NAMESPACE___',
              show_default=True)
@click.option('--kinds', '-k',
              help='Comma separated list of Datastore Kinds to import.',
              required=True)
def import_cmd(project, namespace, data_dir, project_placeholder,
               namespace_placeholder, kinds):
    """Import data to database using previously exported data as input."""
    execute_tasks({
        'type_task': 'import',
        'project': project,
        'namespace': namespace,
        'data_dir': data_dir,
        'project_placeholder': project_placeholder,
        'namespace_placeholder': namespace_placeholder,
        'kinds': kinds,
        'target': execute_import
    })


def execute_import(project, namespace, data_dir, project_placeholder,
                   namespace_placeholder, kind):
    datastore = get_datastore_api()

    entities = load(kind, data_dir)
    entities_json = json.dumps(entities)
    entities_replaced_json = partition_replace(entities_json,
                                               project_placeholder, project,
                                               namespace_placeholder,
                                               namespace)
    entities_replaced = json.loads(entities_replaced_json)

    inserts = [
        {'insert': entity} for entity in entities_replaced
    ]

    request_body = {
        "mutations": inserts,
        "mode": "NON_TRANSACTIONAL"
    }

    datastore.projects() \
        .commit(projectId=project, body=request_body) \
        .execute()
