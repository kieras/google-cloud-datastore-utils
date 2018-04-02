# -*- coding: utf-8 -*-
"""The export command."""
import json

import click

from .utils import (get_datastore_api, partition_replace, save, execute_tasks)


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
    execute_tasks({
        'type_task': 'export',
        'project': project,
        'namespace': namespace,
        'data_dir': data_dir,
        'project_placeholder': project_placeholder,
        'namespace_placeholder': namespace_placeholder,
        'kinds': kinds,
        'chunk': None,
        'target': execute_export
    })


def execute_export(project, namespace, data_dir, project_placeholder,
                   namespace_placeholder, kind, chunk):
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

    entities_replaced = []
    more = True
    
    while more:
        response = datastore.projects() \
            .runQuery(projectId=project, body=request_body) \
            .execute()

        more = not (response['batch']['moreResults'] in ['NO_MORE_RESULTS'])
        cursor = response['batch']['endCursor']

        if more and cursor:
            request_body['query']['startCursor'] = cursor

        entities = extract_entities(response)
        entities_json = json.dumps(entities)
        entities_replaced_json = partition_replace(entities_json, project,
                                                project_placeholder, namespace,
                                                namespace_placeholder)
    
        entities_replaced.extend(json.loads(entities_replaced_json))

    save(entities_replaced, kind, data_dir)


def extract_entities(response):
    return [
        entityResult.get('entity')
        for entityResult in response.get('batch', {}).get('entityResults', [])
    ]
