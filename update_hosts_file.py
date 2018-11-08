#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json

import sys

from HostsTools import hosts_tools


def parse_args() -> sys.argv:
    parser = argparse.ArgumentParser()
    parser.add_argument('--domains', '-d', default=[], nargs='+', help='Domains to add to the list')
    parser.add_argument('--list', '-l', default='ads-and-tracking',
                        help='Base list to use, defaults to "ads-and-tracking"')
    parser.add_argument('--update', '-u', default=False, action='store_true',
                        help='Run a full scan of the entire list - slow!')
    parser.add_argument('--virustotal', '-v', default=False, action='store_true',
                        help='Run a full scan of the entire list using VirusTotal API - slow!')
    args = parser.parse_args()
    if not args.domains and not args.update and not args.virustotal:
        parser.print_help()
        exit(1)
    return args


def main():
    args = parse_args()
    main_domains = hosts_tools.load_domains_from_list(args.list + '.txt')
    expanded_domains = hosts_tools.load_domains_from_list(args.list + '-extended.txt')
    whitelist = hosts_tools.load_domains_from_whitelist(args.list + '-whitelist.txt')
    main_domains_len_start = len(main_domains)
    expanded_domains_len_start = len(expanded_domains)
    api_key = None
    with open('secrets.json') as f:
        data = json.load(f)
        api_key = data['virustotal_api_key']

    if args.update:
        lookup_domains = hosts_tools.reduce_domains(main_domains)
        for index, domain in enumerate(lookup_domains):
            print('Searching: %s' % domain)
            found_domains = hosts_tools.find_subdomains(domain)
            expanded_domains.update(found_domains)
            print('    Found: %s' % (len(found_domains) - 1))
            print_progress(index, len(lookup_domains))

    if args.virustotal:
        lookup_domains = hosts_tools.reduce_domains(main_domains)
        for index, domain in enumerate(lookup_domains):
            print('Searching: %s' % domain)
            found_domains = hosts_tools.virustotal_find_subdomain(domain, api_key)
            expanded_domains.update(found_domains)
            print('    Found: %s' % (len(found_domains) - 1))
            print_progress(index, len(lookup_domains))

    for domain in args.domains:
        if hosts_tools.is_valid_domain(domain):
            main_domains.add(domain)
            print('Searching: %s' % domain)
            found_domains = hosts_tools.find_subdomains(domain)
            expanded_domains.update(found_domains)
            found_domains = hosts_tools.virustotal_find_subdomain(domain, api_key)
            expanded_domains.update(found_domains)
            print('    Found: %s' % (len(found_domains) - 1))

    expanded_domains = expanded_domains.difference(whitelist)

    main_domains_len_end = len(main_domains)
    main_domains_len_diff = main_domains_len_end - main_domains_len_start
    expanded_domains_len_end = len(expanded_domains)
    expanded_domains_len_diff = expanded_domains_len_end - expanded_domains_len_start

    print('Base list: %s, expanded by: %s' % (main_domains_len_end, main_domains_len_diff))
    print('Extended List: %s, expanded by %s' % (expanded_domains_len_end, expanded_domains_len_diff))
    print('List Difference: %s' % (expanded_domains_len_end - main_domains_len_end))

    hosts_tools.write_domain_list(args.list + '.txt', main_domains)
    hosts_tools.write_domain_list(args.list + '-extended.txt', expanded_domains)


def print_progress(current: int, total: int):
    if total != 0:
        percent = int((current / total) * 100)
        if (percent % 5) == 0:
            print('Progress: %s%%' % percent)


if __name__ == "__main__":
    main()
