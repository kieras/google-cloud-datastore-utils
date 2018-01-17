# -*- coding: utf-8 -*-
"""The export command."""
import copy
import json
import threading

import click

from .utils import (get_datastore_api, get_kinds_list, partition_replace, save)


@click.command()
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
              help='Placeholder value to replace the project value'
                   ' in exported files.',
              required=True,
              default='___PROJECT___',
              show_default=True)
@click.option('--namespace-placeholder', '-np',
              help='Placeholder value to replace the namespace value'
                   ' in exported files.',
              required=True,
              default='___NAMESPACE___',
              show_default=True)
@click.option('--kinds', '-k',
              help='Comma separated list of Datastore Kinds to export.',
              required=True)
def export(project, namespace, data_dir, project_placeholder,
           namespace_placeholder, kinds):
    """Export data from database."""
    kinds_list = get_kinds_list(kinds)
    click.echo(
        "Executing export. Project={}, Namespace={}, Kinds={}.".format(
            project,
            namespace,
            kinds_list))
    tasks = {}
    for kind in kinds_list:
        tasks[kind] = threading.Thread(
            target=execute_export,
            name=kind,
            args=(
                project, namespace, data_dir,
                project_placeholder,
                namespace_placeholder, kind
            )
        )

    kinds_list_progress = copy.deepcopy(kinds_list)

    click.echo('Starting tasks...\n')
    for task in tasks:
        tasks[task].start()
    while kinds_list_progress:
        for idx, kind in enumerate(kinds_list_progress):
            if not tasks.get(kind).is_alive():
                click.echo('Task finished. Kind: {}'.format(kind))
                kinds_list_progress.pop(idx)


def execute_export(project, namespace, data_dir, project_placeholder,
                   namespace_placeholder, kind):
    datastore = get_datastore_api()

    request_body = {
        'partitionId': {
            'projectId': project,
            'namespaceId': namespace
        },
        'query': {
            'kind': [
                {
                    'name': kind
                }
            ]
        }
    }

    response = datastore.projects() \
        .runQuery(projectId=project, body=request_body) \
        .execute()

    entities = extract_entities(response)
    entities_json = json.dumps(entities)
    entities_replaced_json = partition_replace(entities_json, project,
                                               project_placeholder, namespace,
                                               namespace_placeholder)
    entities_replaced = json.loads(entities_replaced_json)

    save(entities_replaced, kind, data_dir)


def extract_entities(response):
    return [
        entityResult.get('entity')
        for entityResult in response.get('batch', {}).get('entityResults', [])
    ]
