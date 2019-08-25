#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import update_hosts_file


class TestUpdateHostsFile(object):

    def test_validate_domain_args_empty(self):
        update_hosts_file.validate_domain_args([])

    def test_validate_domain_args_valid(self):
        update_hosts_file.validate_domain_args(['example.com'])

    def test_validate_domain_args_invalid(self):
        with pytest.raises(Exception):
            update_hosts_file.validate_domain_args(['not valid'])

    def test_print_progress_zero(self):
        update_hosts_file.print_progress(0, 0)

    def test_print_progress_half(self):
        update_hosts_file.print_progress(5, 10)

    def test_print_progress_done(self):
        update_hosts_file.print_progress(10, 10)
