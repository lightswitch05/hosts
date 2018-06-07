# Hosts

A collection of `hosts` files for domain blocking

Host file recipe | Description | Raw hosts
---------------- | ----------- |:---------:
Ads & Tracking | List of domains I've found to not be on other lists. | [link](https://raw.githubusercontent.com/lightswitch05/hosts/master/ads-and-tracking.txt)
Ads & Tracking Extended | A programmatically expanded version of my base Ads & Tracking list. This list is more likely to contain false positives, but is still very reliable and I recommend using it. | [link](https://raw.githubusercontent.com/lightswitch05/hosts/master/ads-and-tracking-extended.txt)

# Adding a domain

## Pre-requisites

* Python 3.5 or later
* pip3

## Setup

```bash
$ pip3 install -r requirements.txt
```

## Usage
```bash
$ python3 updateHostsFile.py --help
```

## Examples

```bash
$ python3 updateHostsFile.py -d amazon-adsystem.com doubleclick.net
```

```bash
$ python3 updateHostsFile.py -update
```
