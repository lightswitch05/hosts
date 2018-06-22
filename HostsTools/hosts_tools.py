#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Set
import re
import requests
import json
import datetime

STRIP_COMMENTS_PATTERN = re.compile(r"^([^#]+)")
ALLOWED_DOMAIN_PATTERN = re.compile("(?!-)[A-Z\d-]{1,255}(?<!-)$", re.IGNORECASE)
FILE_HEADER = """
# Collection of Analytics, Ads, and tracking hosts to block.
#
# Released: [timestamp]
# Count: [domain_count] domains
# Details: https://github.com/lightswitch05/hosts
# Issues: https://github.com/lightswitch05/hosts/issues
# Source: https://raw.githubusercontent.com/lightswitch05/hosts/master/[file_name]
#
# Copyright [yyyy] Daniel White
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.\n
""".lstrip()


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


def build_file_header(file_name: str, list_length: int):
    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc, microsecond=0)
    header = FILE_HEADER.replace('[domain_count]', str(list_length))
    header = header.replace('[file_name]', file_name)
    header = header.replace('[yyyy]', str(now.year))
    return header.replace('[timestamp]', now.isoformat())


def write_domain_list(file_name: str, domains: Set[str]):
    sorted_domains = sort_domains(list(domains))
    with open(file_name, 'w') as file:
        file.write(build_file_header(file_name, len(sorted_domains)))
        for domain in sorted_domains:
            file.write('0.0.0.0 %s\n' % domain)


def is_valid_domain(domain: str) -> bool:
    if not domain or len(domain) > 255:
        return False
    if domain[-1] == ".":
        domain = domain[:-1]  # strip exactly one dot from the right, if present
    return all(ALLOWED_DOMAIN_PATTERN.match(x) for x in domain.split("."))


def find_subdomains(domain: str) -> Set[str]:
    found_domains = {domain}  # include query as a found domain
    url = 'https://crt.sh/?q=%.{d}&output=json'.format(d=domain)
    try:
        req = requests.get(url, headers={
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) Gecko/20100101 Firefox/60.0'
        })
        if req.status_code != 200:
            print('Error received from crt.sh: ' + req.text)
        else:
            try:
                content = req.content.decode('utf-8')
                data = json.loads("[{}]".format(content.replace('}{', '},{')))
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
