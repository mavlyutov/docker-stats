#!/usr/bin/env python

import argparse
import docker
import json
import re


def normalize(dictionary):
    """
    see README.rst
    """

    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            normalize(value)

        item_dict = dict()
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and "op" in item:
                    item_dict.update({item.pop("op"): item})
        if item_dict:
            dictionary[key] = item_dict

    return dictionary


def container_name(id):
    """
    Find container`s name by its ID and return it with replacing non-word and non-digit symbols to underscores
    :param id: Container`s Id
    :return: Container`s name
    """

    client = docker.Client(base_url='unix://var/run/docker.sock', version='auto')
    return re.sub('[^\w]', '_', client.inspect_container['Name'])


def main():
    parser = argparse.ArgumentParser(description='docker stats, json way')
    parser.add_argument('containers', metavar='container', type=str, nargs='*', help='IDs or NAMEs of desired containers')
    parser.add_argument('-a', '--all', dest='all', action='store_true', help='get stats of all available containers')
    parser.add_argument('-n', '--normalize', dest='normalize', action='store_true', help='try to normalize stats')
    parser.add_argument('-N', '--names', dest='names', action='store_true', help='return containers names instead of Ids with replacing non-digit and non-word symbols to underscores')
    args = parser.parse_args()

    if not args.containers and not args.all:
        parser.print_usage()
        parser.exit()

    client = docker.Client(base_url='unix://var/run/docker.sock', version='auto')
    ids = args.all and [container['Id'] for container in client.containers(quiet=True)] or args.containers

    stats = {args.names and container_name(c) or c: client.stats(c, stream=0) for c in ids}
    stats = args.normalize and normalize(stats) or stats
    print json.dumps(stats)
