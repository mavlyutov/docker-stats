#!/usr/bin/env python

import argparse
import json

import docker
try:
    docker_client = docker.Client
except AttributeError:
    docker_client = docker.APIClient


from operator import itemgetter


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


def main():
    parser = argparse.ArgumentParser(description='docker stats, json way')
    parser.add_argument('containers', metavar='container', type=str, nargs='*', help='IDs or NAMEs of desired containers')
    parser.add_argument('-a', '--all', dest='all', action='store_true', help='get stats of all available containers')
    parser.add_argument('-n', '--normalize', dest='normalize', action='store_true', help='try to normalize stats')
    args = parser.parse_args()

    if not args.containers and not args.all:
        parser.print_usage()
        parser.exit()

    client = docker_client(base_url='unix://var/run/docker.sock')
    ids = args.all and map(itemgetter('Id'), client.containers(quiet=True)) or args.containers

    stats = {c: client.stats(c, stream=0) for c in ids}
    stats = args.normalize and normalize(stats) or stats
    print json.dumps(stats)
