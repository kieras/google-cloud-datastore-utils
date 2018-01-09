# -*- coding: utf-8 -*-
"""The export module."""
import io
import os
import json
import googleapiclient.discovery


def run(from_project, from_namespace, to_project, to_namespace, export_data_dir, kind):
    datastore = googleapiclient.discovery.build('datastore', 'v1')

    export_request_body = {
        'partitionId': {
            'projectId': from_project,
            'namespaceId': from_namespace
        },
        'query': {
            'kind': [
                {
                    'name': kind
                }
            ]
        }
    }

    export_response = datastore.projects() \
        .runQuery(projectId=from_project, body=export_request_body) \
        .execute()

    entities = extract_entities(export_response)

    updated_entities = update_entities_to_new_project_and_namespace(entities, from_namespace, from_project,
                                                                    to_namespace, to_project)

    save(updated_entities, kind, export_data_dir)


def extract_entities(export_response):
    entities = []
    for entityResult in export_response.get('batch').get('entityResults'):
        entity = entityResult.get('entity')
        entities.append(entity)
    return entities


def update_entities_to_new_project_and_namespace(entities, from_namespace, from_project, to_namespace, to_project):
    entities_str = json.dumps(entities)
    entities_str = entities_str.replace('"projectId": "{}"'.format(from_project),
                                        '"projectId": "{}"'.format(to_project))
    entities_str = entities_str.replace('"namespaceId": "{}"'.format(from_namespace),
                                        '"namespaceId": "{}"'.format(to_namespace))
    updated_entities = json.loads(entities_str)
    return updated_entities


def save(updated_entities, kind, export_data_dir):
    if not os.path.exists(export_data_dir):
        os.makedirs(export_data_dir)

    with io.open('{}/{}.json'.format(export_data_dir, kind), 'w', encoding='utf-8') as export_file:
        export_file.write(
            json.dumps(updated_entities, ensure_ascii=False, sort_keys=True, indent=2, separators=(',', ': ')))
