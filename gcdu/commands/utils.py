# -*- coding: utf-8 -*-
"""Utilities."""
import io
import json
import os

import click
import googleapiclient.discovery


def get_datastore_api():
    return googleapiclient.discovery.build('datastore', 'v1')


def get_kinds_list(kinds):
    return kinds.split(',')


def show_progressbar_item(item):
    if item is None:
        return 'Done!'
    return "Kind: {}".format(item)


def partition_replace(entities_json, from_project, to_project, from_namespace,
                      to_namespace):
    result = entities_json.replace('"projectId": "{}"'.format(from_project),
                                   '"projectId": "{}"'.format(to_project))
    result = result.replace('"namespaceId": "{}"'.format(from_namespace),
                            '"namespaceId": "{}"'.format(to_namespace))
    return result


def save(entities, kind, data_dir):
    if not entities:
        click.echo('No entities found for kind {}'.format(kind))
        return
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    with io.open('{}/{}.json'.format(data_dir, kind), 'w',
                 encoding='utf-8') as export_file:
        export_file.write(
            json.dumps(entities, ensure_ascii=False, sort_keys=True, indent=2,
                       separators=(u',', u': ')))


def load(kind, data_dir):
    with io.open('{}/{}.json'.format(data_dir, kind), 'r',
                 encoding='utf-8') as export_file:
        entities = json.load(export_file)
    return entities
