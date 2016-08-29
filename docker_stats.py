#!/usr/bin/env python

import argparse
import docker
import json

from operator import itemgetter


def main():
    parser = argparse.ArgumentParser(description='docker stats, json way')
    parser.add_argument('containers', metavar='container', type=str, nargs='*', help='IDs or NAMEs of desired containers')
    parser.add_argument('-a', '--all', dest='all', action='store_true', help='get stats of all available containers')
    args = parser.parse_args()

    if not args.containers and not args.all:
        parser.print_usage()
        parser.exit()

    client = docker.Client(base_url='unix://var/run/docker.sock')
    ids = args.all and map(itemgetter('Id'), client.containers(quiet=True)) or args.containers
    print json.dumps({c: client.stats(c, stream=0) for c in ids})
