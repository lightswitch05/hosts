#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import signal
from typing import Set

import sys

from HostsTools import hosts_tools

global QUIT_GRACEFULLY
QUIT_GRACEFULLY = False


def parse_args() -> sys.argv:
    parser = argparse.ArgumentParser()
    parser.add_argument('--domains', '-d', default=[], nargs='+', help='Domains to add to the list')
    parser.add_argument('--list', '-l', default='ads-and-tracking',
                        help='Base list to use, defaults to "ads-and-tracking"')
    parser.add_argument('--update', '-u', default=False, action='store_true',
                        help='Run a full scan of the entire list - slow!')
    parser.add_argument('--virustotal', '-v', default=False, action='store_true',
                        help='Run a full scan of the entire list using VirusTotal API - slow!')
    parser.add_argument('--dryrun', '-t', default=False, action='store_true',
                        help='Dry run - do not write any list modifications')
    parser.add_argument('--verbose', '-vvv', default=False, action='store_true',
                        help='Verbose logging')
    args = parser.parse_args()
    if not args.domains and not args.update and not args.virustotal:
        parser.print_help()
        exit(1)
    validate_domain_args(args.domains)
    return args


def main():
    args = parse_args()
    main_domains = hosts_tools.load_domains_from_list(args.list + '.txt')
    expanded_domains = hosts_tools.load_domains_from_list(args.list + '-extended.txt')
    whitelist = hosts_tools.load_domains_from_whitelist(args.list + '-whitelist.txt')
    main_domains_len_start = len(main_domains)
    expanded_domains_len_start = len(expanded_domains)
    with open('secrets.json') as f:
        data = json.load(f)
        api_key = data['virustotal_api_key']

    if args.update:
        found = crt_update(main_domains, args.verbose)
        expanded_domains.update(found)

    if args.virustotal:
        found = virustotal_update(main_domains, api_key, args.verbose)
        expanded_domains.update(found)

    main_domains.update(args.domains)
    found = crt_update(args.domains, args.verbose)
    expanded_domains.update(found)

    found = virustotal_update(args.domains, api_key, args.verbose)
    expanded_domains.update(found)

    expanded_domains = hosts_tools.filter_whitelist(expanded_domains, whitelist)

    main_domains_len_end = len(main_domains)
    main_domains_len_diff = main_domains_len_end - main_domains_len_start
    expanded_domains_len_end = len(expanded_domains)
    expanded_domains_len_diff = expanded_domains_len_end - expanded_domains_len_start

    print('Base list: %s, expanded by: %s' % (main_domains_len_end, main_domains_len_diff))
    print('Extended List: %s, expanded by %s' % (expanded_domains_len_end, expanded_domains_len_diff))
    print('List Difference: %s' % (expanded_domains_len_end - main_domains_len_end))

    if not args.dryrun:
        hosts_tools.write_domain_list(args.list + '.txt', main_domains)
        hosts_tools.write_domain_list(args.list + '-extended.txt', expanded_domains)


def crt_update(main_domains: Set[str], verbose: bool):
    found = set()
    lookup_domains = hosts_tools.reduce_domains(main_domains)
    for index, domain in enumerate(lookup_domains):
        if QUIT_GRACEFULLY:
            break
        print('Searching: %s' % domain)
        found_domains = hosts_tools.find_subdomains(domain, verbose)
        found.update(found_domains)
        found.update(main_domains)
        print('    Found: %s' % (len(found_domains) - 1))
        print_progress(index, len(lookup_domains))
    return found


def virustotal_update(main_domains: Set[str], api_key: str, verbose: bool):
    found = set()
    lookup_domains = hosts_tools.reduce_domains(main_domains)
    for index, domain in enumerate(lookup_domains):
        if QUIT_GRACEFULLY:
            break
        print('Searching: %s' % domain)
        found_domains = hosts_tools.virustotal_find_subdomain(domain, api_key, verbose)
        found.update(found_domains)
        found.update(main_domains)
        print('    Found: %s' % (len(found_domains) - 1))
        print_progress(index, len(lookup_domains))
    return found


def print_progress(current: int, total: int):
    if total != 0:
        percent = int((current / total) * 100)
        if (percent % 5) == 0:
            print('Progress: %s%%' % percent)


def validate_domain_args(domains):
    for domain in domains:
        if not hosts_tools.is_valid_domain(domain):
            raise Exception('Invalid domain: ', domain)


def quit_gracefully(sig, frame):
    global QUIT_GRACEFULLY
    print('Quitting gracefully')
    QUIT_GRACEFULLY = True


if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully)
    main()
