#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Set
import re
import requests
import json
import argparse
import sys

STRIP_COMMENTS_PATTERN = re.compile(r"^([^#]+)")
ALLOWED_DOMAIN_PATTERN = re.compile("(?!-)[A-Z\d-]***REMOVED***1,63***REMOVED***(?<!-)$", re.IGNORECASE)


def sort_domains(domains: List[str]) -> List[str]:
    sorted_list = []
    for domain in domains:
        d = domain.strip().split('.')
        d.reverse()
        sorted_list.append(d)
    sorted_list.sort()
    for index, domain_parts in enumerate(sorted_list):
        domain_parts.reverse()
        sorted_list[index] = '.'.join(domain_parts)
    return sorted_list


def extract_domain(domain_entry: str) -> str:
    # First strip any comments
    match = STRIP_COMMENTS_PATTERN.match(domain_entry)
    if match and match.group(0):
        # At least one character was found that was not after a comment.
        # Split it on whitespace, if the parts found is exactly 2
        # then we can assume its a valid host entry
        entry_parts = match.group(0).split()
        if len(entry_parts) == 2 and is_valid_domain(entry_parts[1]):
            return entry_parts[1].lower()
    return ''


def load_domains_from_list(file_name: str) -> Set[str]:
    domains = set()
    with open(file_name) as file:
        lines = file.readlines()
    for index, line in enumerate(lines):
        domain = extract_domain(line)
        if domain:
            domains.add(domain)
    return domains


def write_domain_list(file_name: str, domains: Set[str]):
    sorted_domains = sort_domains(list(domains))
    with open(file_name, 'w') as file:
        file.write('# Collection of Analytics, Ads, and tracking hosts to block\n')
        file.write('# https://github.com/lightswitch05/hosts/blob/master/%s\n\n' % file_name)
        for domain in sorted_domains:
            file.write('0.0.0.0 %s\n' % domain)


def is_valid_domain(domain: str) -> bool:
    if not domain or len(domain) > 255:
        return False
    if domain[-1] == ".":
        domain = domain[:-1]  # strip exactly one dot from the right, if present
    return all(ALLOWED_DOMAIN_PATTERN.match(x) for x in domain.split("."))


def find_subdomains(domain: str) -> Set[str]:
    found_domains = ***REMOVED***domain***REMOVED***  # include query as a found domain
    url = 'https://crt.sh/?q=%.***REMOVED***d***REMOVED***&output=json'.format(d=domain)
    try:
        req = requests.get(url, headers=***REMOVED***
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) Gecko/20100101 Firefox/60.0'
        ***REMOVED***)
        if req.status_code != 200:
            print('Error received from crt.sh: ' + req.text)
        else:
            try:
                content = req.content.decode('utf-8')
                data = json.loads("[***REMOVED******REMOVED***]".format(content.replace('***REMOVED******REMOVED***', '***REMOVED***,***REMOVED***')))
                for key, value in enumerate(data):
                    found_domain = value['name_value'].lower()
                    if found_domain.startswith('*.'):
                        found_domain = found_domain[2:]
                    if is_valid_domain(found_domain):
                        found_domains.add(found_domain)
            except ValueError:
                print('Unknown response from crt.sh: ' + req.text)
    except Exception:
        print('Unable to connect to crt.sh to search: %s: ' % domain)
    return found_domains


def parse_args() -> sys.argv:
    parser = argparse.ArgumentParser()
    parser.add_argument('--domains', '-d', default=[], nargs='+', help='Domains to add to the list')
    parser.add_argument('--update', '-u', default=False, action='store_true',
                        help='Run a full scan of the entire list - slow!')
    args = parser.parse_args()
    if not args.domains and not args.update:
        parser.print_help()
        exit(1)
    return args


def main():
    args = parse_args()
    main_domains = load_domains_from_list('ads-and-tracking.txt')
    expanded_domains = load_domains_from_list('ads-and-tracking-extended.txt')
    main_domains_len_start = len(main_domains)
    expanded_domains_len_start = len(expanded_domains)

    if args.update:
        expanded_domains = set()  # Clear it out since we're doing a full update
        for domain in main_domains:
            print('Searching: %s' % domain)
            found_domains = find_subdomains(domain)
            expanded_domains.update(found_domains)
            print('    Found: %s' % (len(found_domains) - 1))

    for domain in args.domains:
        if is_valid_domain(domain):
            main_domains.add(domain)
            print('Searching: %s' % domain)
            found_domains = find_subdomains(domain)
            expanded_domains.update(found_domains)
            print('    Found: %s' % (len(found_domains) - 1))

    main_domains_len_end = len(main_domains)
    main_domains_len_diff = main_domains_len_end - main_domains_len_start
    expanded_domains_len_end = len(expanded_domains)
    expanded_domains_len_diff = expanded_domains_len_end - expanded_domains_len_start

    print('Base list: %s, expanded by: %s' % (main_domains_len_end, main_domains_len_diff))
    print('Extended List: %s, expanded by %s' % (expanded_domains_len_end, expanded_domains_len_diff))
    print('List Difference: %s' % (expanded_domains_len_end - main_domains_len_end))

    write_domain_list('ads-and-tracking.txt', main_domains)
    write_domain_list('ads-and-tracking-extended.txt', expanded_domains)


if __name__ == "__main__":
    main()
