#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import os.path
from typing import List
from typing import Set
from collections import namedtuple
from HostsTools import hosts_tools


class HostList(namedtuple('HostList', 'filename set')):
    pass


def parse_args() -> sys.argv:
    parser = argparse.ArgumentParser()
    parser.add_argument('filename_a', type=str, help='First list to compare')
    parser.add_argument('filename_b', type=str, help='Second list to compare')
    args = parser.parse_args()
    if not (args.filename_a and args.filename_b):
        parser.print_help()
        exit(1)
    validate_filename_args(args)
    return args


def validate_filename_args(args) -> bool:
    if not os.path.isfile(args.filename_a):
        raise Exception('Invalid host file: ', args.filename_a)
    if not os.path.isfile(args.filename_b):
        raise Exception('Invalid host file: ', args.filename_b)


def main() -> None:
    args = parse_args()
    filename_a = args.filename_a
    filename_b = args.filename_b
    set_a = hosts_tools.load_domains_from_list(filename_a)
    set_b = hosts_tools.load_domains_from_list(filename_b)

    list_a = HostList(filename_a, set_a)
    list_b = HostList(filename_b, set_b)

    print()
    print_list_size(list_a, list_b)
    print()
    print_list_difference(list_a, list_b)


def print_list_size(list_a: HostList, list_b: HostList) -> None:
    size_a = len(list_a.set)
    size_b = len(list_b.set)
    difference = size_a - size_b
    print('Number of unique host entries: %s' % difference)
    print_list_fact(list_a.filename, size_a)
    print_list_fact(list_b.filename, size_b)


def print_list_difference(list_a: HostList, list_b: HostList) -> None:
    unique_list_a = list_a.set - list_b.set
    size_unique_a = len(unique_list_a)
    percentage_unique_a = round((size_unique_a / len(list_a.set)) * 100, 2)

    unique_list_b = list_b.set - list_a.set
    size_unique_b = len(unique_list_b)
    percentage_unique_b = round((size_unique_b / len(list_b.set)) * 100, 2)

    print('Number of unique hosts not in the other list:')
    print_list_fact(list_a.filename, f'{size_unique_a} ({percentage_unique_a}%)')
    print_list_fact(list_b.filename, f'{size_unique_b} ({percentage_unique_b}%)')


def print_list_fact(list_name, fact) -> None:
    print('{:<30}{:<30}'.format(list_name, fact))


if __name__ == "__main__":
    main()
