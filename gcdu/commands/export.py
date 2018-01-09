# -*- coding: utf-8 -*-
"""The export command."""
import io
import os
import json
import click
import googleapiclient.discovery

from .utils import show_progressbar_item, replace_with_placeholders


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
              help='Placeholder value to replace the project value in exported files.',
              required=True,
              default='___PROJECT___',
              show_default=True)
@click.option('--namespace-placeholder', '-np',
              help='Placeholder value to replace the namespace value in exported files.',
              required=True,
              default='___NAMESPACE___',
              show_default=True)
@click.option('--kinds', '-k',
              help='Comma separated list of Datastore Kinds to export.',
              required=True)
def export(project, namespace, data_dir, project_placeholder, namespace_placeholder, kinds):
    """Export data from database."""
    kinds_list = kinds.split(',')
    click.echo("Executing export. Project={}, Namespace={}, Kinds={}.".format(project, namespace, kinds_list))
    with click.progressbar(kinds_list, label='Exporting', show_eta=True,
                           item_show_func=show_progressbar_item) as bar:
        for kind in bar:
            execute_export(project, namespace, data_dir, project_placeholder, namespace_placeholder, kind)


def execute_export(project, namespace, data_dir, project_placeholder, namespace_placeholder, kind):
    datastore = googleapiclient.discovery.build('datastore', 'v1')

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
    entities_replaced_json = replace_with_placeholders(entities_json, project, project_placeholder, namespace,
                                                       namespace_placeholder)
    entities_replaced = json.loads(entities_replaced_json)

    save(entities_replaced, kind, data_dir)


def extract_entities(response):
    entities = []
    for entityResult in response.get('batch').get('entityResults'):
        entity = entityResult.get('entity')
        entities.append(entity)
    return entities


def save(entities, kind, data_dir):
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    with io.open('{}/{}.json'.format(data_dir, kind), 'w', encoding='utf-8') as export_file:
        export_file.write(
            json.dumps(entities, ensure_ascii=False, sort_keys=True, indent=2, separators=(',', ': ')))
