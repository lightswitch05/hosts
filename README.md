# Hosts

[![Github Stars](https://img.shields.io/github/stars/lightswitch05/hosts)](https://github.com/lightswitch05/hosts)
[![Build Status](https://travis-ci.org/lightswitch05/hosts.svg?branch=master)](https://travis-ci.org/lightswitch05/hosts)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=lightswitch05_hosts&metric=alert_status)](https://sonarcloud.io/dashboard?id=lightswitch05_hosts)
[![license](https://img.shields.io/github/license/lightswitch05/hosts.svg)](https://github.com/lightswitch05/hosts/blob/master/LICENSE)
[![last commit](https://img.shields.io/github/last-commit/lightswitch05/hosts.svg)](https://github.com/lightswitch05/hosts/commits/master)
[![commit activity](https://img.shields.io/github/commit-activity/y/lightswitch05/hosts.svg)](https://github.com/lightswitch05/hosts/commits/master)
[![donate](https://img.shields.io/badge/Donate-EFF-orange.svg)](https://supporters.eff.org/donate)
[![gitter](https://img.shields.io/gitter/room/lightswitch05/hosts.svg)](https://gitter.im/lightswitch05/hosts)

A collection of `hosts` files for domain blocking. If you find something in a list that you believe is a mistake or breaks functionality, please open a ticket and I'll consider removing it. Also, if you find an unblocked subdomain of a blocked root domain, please let me know so I can add it to a list.

Host file recipe | Description | Raw hosts
---------------- | ----------- |:---------:
Ads & Tracking | A programmatically expanded list of hosts used for advertisements and tracking. This is my primary list and I recommend using it. | [link](https://www.github.developerdan.com/hosts/lists/ads-and-tracking-extended.txt)
Tracking Aggressive | A very aggressive block list for tracking, geo-targeting, & ads. This list will likely break functionality, so do not use it unless you are willing to maintain your own whitelist. If you find something in this list that you think is a mistake, please open a ticket and we can discuss it. Keep in mind that this is an aggressive list. | [link](https://www.github.developerdan.com/hosts/lists/tracking-aggressive-extended.txt)
AMP Hosts | [Google's Accelerated Mobile Pages (AMP)](https://www.theregister.co.uk/2017/05/19/open_source_insider_google_amp_bad_bad_bad/) are taking over the web. Block AMP pages with this list. Since I use [DuckDuckGo](https://duckduckgo.com/), this list is pretty sparse and suggestions are welcome! | [link](https://www.github.developerdan.com/hosts/lists/amp-hosts-extended.txt)
Facebook | A hosts file to block all facebook and facebook related services, including Messenger, Instagram, and WhatsApp. This is a pretty new list and I recommend using it with [anudeepND's](https://github.com/anudeepND/blacklist) [Facebook list](https://raw.githubusercontent.com/anudeepND/blacklist/master/facebook.txt) as well to ensure full coverage. | [link](https://www.github.developerdan.com/hosts/lists/facebook-extended.txt)

# Adding a domain

## Pre-requisites

* Python 3.6 or later
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
