#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from HostsTools import hosts_tools
import argparse
import sys


def parse_args() -> sys.argv:
    parser = argparse.ArgumentParser()
    parser.add_argument('--domains', '-d', default=[], nargs='+', help='Domains to add to the list')
    parser.add_argument('--list', '-l', default='ads-and-tracking', help='Base list to use, defaults to "ads-and-tracking"')
    parser.add_argument('--update', '-u', default=False, action='store_true',
                        help='Run a full scan of the entire list - slow!')
    args = parser.parse_args()
    if not args.domains and not args.update:
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

    if args.update:
        expanded_domains = set(main_domains)  # Clear it out since we're doing a full update
        lookup_domains = hosts_tools.reduce_domains(main_domains)
        for domain in lookup_domains:
            print('Searching: %s' % domain)
            found_domains = hosts_tools.find_subdomains(domain)
            expanded_domains.update(found_domains)
            print('    Found: %s' % (len(found_domains) - 1))

    for domain in args.domains:
        if hosts_tools.is_valid_domain(domain):
            main_domains.add(domain)
            print('Searching: %s' % domain)
            found_domains = hosts_tools.find_subdomains(domain)
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


if __name__ == "__main__":
    main()
