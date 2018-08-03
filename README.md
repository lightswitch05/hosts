# Hosts

[![Build Status](https://travis-ci.org/lightswitch05/hosts.svg?branch=master)](https://travis-ci.org/lightswitch05/hosts)

A collection of `hosts` files for domain blocking

Host file recipe | Description | Raw hosts
---------------- | ----------- |:---------:
Ads & Tracking | List of domains I've found to not be on other lists. | [link](https://raw.githubusercontent.com/lightswitch05/hosts/master/ads-and-tracking.txt)
Ads & Tracking Extended | A programmatically expanded version of my base Ads & Tracking list. This list is more likely to contain false positives, but is still very reliable and I recommend using it. If you use [Steven Black's hosts list](https://github.com/StevenBlack/hosts), then you are already using this list. | [link](https://raw.githubusercontent.com/lightswitch05/hosts/master/ads-and-tracking-extended.txt)
Tracking Aggressive | A very aggressive block list for tracking, geo-targeting, & ads. This list will break functionality, do no use it unless you are willing to maintain your own whitelist. Requests to remove domains from this list will be closed. | [link](https://raw.githubusercontent.com/lightswitch05/hosts/master/tracking-aggressive.txt)
Tracking Aggressive Extended | A programmatically expanded version of the Tracking Aggressive list. If you are willing to use the aggressive list, I recommend using this extended version instead. Again, do not use this if you are unwilling to deal with broken sites and self-managed whitelists. | [link](https://raw.githubusercontent.com/lightswitch05/hosts/master/tracking-aggressive-extended.txt)

# Adding a domain

## Pre-requisites

* Python 3.5 or later
* pip3

## Setup

```bash
$ make setup
```

## Test

```bash
$ make test
```

## Usage
```bash
$ python3 update_hosts_file.py --help
```

## Examples

```bash
$ python3 update_hosts_file.py -d amazon-adsystem.com doubleclick.net
```

```bash
$ python3 update_hosts_file.py -update
```
