# -*- coding: utf-8 -*-
"""Utilities."""


def show_progressbar_item(item):
    if item is None:
        return 'Done!'
    return "Kind: {}".format(item)


def replace_with_placeholders(entities_json, from_project, to_project, from_namespace, to_namespace):
    result = entities_json.replace('"projectId": "{}"'.format(from_project),
                                   '"projectId": "{}"'.format(to_project))
    result = result.replace('"namespaceId": "{}"'.format(from_namespace),
                            '"namespaceId": "{}"'.format(to_namespace))
    return result


