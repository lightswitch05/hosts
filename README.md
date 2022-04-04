# Hosts --- TEST

[![Github Stars](https://img.shields.io/github/stars/lightswitch05/hosts)](https://github.com/lightswitch05/hosts)
[![license](https://img.shields.io/github/license/lightswitch05/hosts.svg)](https://github.com/lightswitch05/hosts/blob/master/LICENSE)
[![last commit](https://img.shields.io/github/last-commit/lightswitch05/hosts.svg)](https://github.com/lightswitch05/hosts/commits/master)
[![commit activity](https://img.shields.io/github/commit-activity/y/lightswitch05/hosts.svg)](https://github.com/lightswitch05/hosts/commits/master)
[![donate](https://img.shields.io/badge/Donate-EFF-orange.svg)](https://supporters.eff.org/donate)

A collection of `hosts` files for domain blocking. If you find something in a list that you believe is a mistake or breaks functionality, please open a ticket and I'll consider removing it. Also, if you find an unblocked subdomain of a blocked root domain, please let me know so I can add it to a list.

[![Hosts Logo](https://raw.githubusercontent.com/lightswitch05/hosts/master/docs/logo.png)](https://www.github.developerdan.com/hosts/)

Host file recipe | Description | Raw hosts
---------------- | ----------- |:---------:
Ads & Tracking | A programmatically expanded list of hosts used for advertisements and tracking. This is my primary list and I recommend using it. | [link](https://www.github.developerdan.com/hosts/lists/ads-and-tracking-extended.txt)
Facebook | A hosts file to block all Facebook and Facebook related services, including Messenger, Instagram, and WhatsApp. | [link](https://www.github.developerdan.com/hosts/lists/facebook-extended.txt)
AMP Hosts | [Google's Accelerated Mobile Pages (AMP)](https://www.theregister.co.uk/2017/05/19/open_source_insider_google_amp_bad_bad_bad/) are taking over the web. Block AMP pages with this list. | [link](https://www.github.developerdan.com/hosts/lists/amp-hosts-extended.txt)
Dating Services | Block all dating services. This list covers everything from eharmony and match.com to AshleyMadison and SwingLifeStyle. If your not interested in hot local singles, this is the list for you. This is a new blocking category for me to take on, and I'm discovering that there are a lot more dating services then I initial thought. I'm going to give it my best effort to maintain this list, but if it ends up being too challenging and time consuming, I might have to drop it. Anyways, give it a try and let me know what you think - good or bad. I've been out of the dating game for a while now, so I expect there to be some large gaps in coverage - especially in terms of apps - so please give drop me a ticket if you find some missing services and help make this a list worth using. | [link](https://www.github.developerdan.com/hosts/lists/dating-services-extended.txt)
Hate & Junk | This is an opinionated list to block things that I consider to be hateful or just plain junk. This list isn't for censorship, but rather websites that I wouldn't want my children to read without having a discussion first. Topics include but are not limited to hate groups, anti-vax, flat earth, and climate change denial. You are welcome to use this list if you like. If you disagree with something in this list... [well, that's just, like, your opinion, man.](https://www.youtube.com/watch?v=pWdd6_ZxX8c) | [link](https://www.github.developerdan.com/hosts/lists/hate-and-junk-extended.txt)
Tracking Aggressive | I do not recommend this list for most users. It is a very aggressive block list for tracking, geo-targeting, & ads. This list will likely break functionality, so do not use it unless you are willing to maintain your own whitelist. If you find something in this list that you think is a mistake, please open a ticket and we can discuss it. Keep in mind that this is an aggressive list. | [link](https://www.github.developerdan.com/hosts/lists/tracking-aggressive-extended.txt)

# Read before use

## CNAME-based ad blockers

If you are using these lists with an ad blocker that uses CNAME blocking, **please read Common Issues / Google Fonts**.

Ad blockers/tools using CNAME blocking include:
* Blokada
* PiHole
* uBlock Origin

This list is not exhaustive, feel free to make suggestions.

# Common Issues

### Google Fonts

I DO NOT BLOCK `fonts.gstatic.com`. However, I do block `gstaticadssl.l.google.com`. If you are using the Ads & Tracking list and are having issues with `fonts.gstatic.com`, then you might be using a blocker that blocks based on CNAME. Depending on your blocking tool, you might want to whitelist `fonts.gstatic.com` to prevent it from getting blocked by `gstaticadssl.l.google.com` CNAME.

See: [#197](https://github.com/lightswitch05/hosts/issues/197), [#136](https://github.com/lightswitch05/hosts/issues/136), and [#213](https://github.com/lightswitch05/hosts/issues/213)

### Xbox Live Achievements

Turns out Xbox Live Achievements is using a common Microsoft tracking server. If you are using the Ads & Tracking list and want to continue getting Xbox Live Achievements, then you might need to whitelist a couple domains. Since I do not have an Xbox, I can't really help you with that, but please see [#161](https://github.com/lightswitch05/hosts/issues/161) for details.
