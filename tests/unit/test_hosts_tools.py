from HostsTools import hosts_tools


class TestHostTools(object):
    def test_none_is_not_a_valid_domain(self):
        is_valid = hosts_tools.is_valid_domain(None)
        assert not is_valid

    def test_empty_is_not_a_valid_domain(self):
        is_valid = hosts_tools.is_valid_domain("")
        assert not is_valid

    def test_wildcard_is_not_a_valid_domain(self):
        is_valid = hosts_tools.is_valid_domain("*.example.com")
        assert not is_valid

    def test_percent_is_not_a_valid_domain(self):
        is_valid = hosts_tools.is_valid_domain("%example.com")
        assert not is_valid

    def test_too_long_is_not_a_valid_domain(self):
        domain = ("a" * 255) + ".com"
        is_valid = hosts_tools.is_valid_domain(domain)
        assert not is_valid

    def test_long_is_a_valid_domain(self):
        domain = "a" * 251 + ".com"
        is_valid = hosts_tools.is_valid_domain(domain)
        assert is_valid

    def test_naked_is_a_valid_domain(self):
        is_valid = hosts_tools.is_valid_domain("example.com")
        assert is_valid

    def test_www_is_a_valid_domain(self):
        is_valid = hosts_tools.is_valid_domain("www.example.com")
        assert is_valid

    def test_trailing_dot_is_a_valid_domain(self):
        is_valid = hosts_tools.is_valid_domain("www.example.com.")
        assert is_valid

    def test_extract_basic(self):
        extracted = hosts_tools.extract_domain("0.0.0.0 example.com")
        assert extracted == "example.com"

    def test_extract_trailing_comment(self):
        extracted = hosts_tools.extract_domain("0.0.0.0 example.com # comment")
        assert extracted == "example.com"

    def test_extract_empty_line(self):
        extracted = hosts_tools.extract_domain("")
        assert extracted == ""

    def test_extract_only_comment(self):
        extracted = hosts_tools.extract_domain("# comment")
        assert extracted == ""

    def test_extract_commented_out_entry(self):
        extracted = hosts_tools.extract_domain("# 0.0.0.0 example.com")
        assert extracted == ""

    def test_sort_root_domains(self):
        domains = ["y.a", "z.a", "x.a", "c.z", "b.z", "a.z"]
        sorted = hosts_tools.sort_domains(domains)
        assert sorted == ["x.a", "y.a", "z.a", "a.z", "b.z", "c.z"]

    def test_sort_sub_domains(self):
        domains = ["b.y.a", "a.y.a", "y.a", "c.z", "b.a.z", "a.z"]
        sorted = hosts_tools.sort_domains(domains)
        assert sorted == ["y.a", "a.y.a", "b.y.a", "a.z", "b.a.z", "c.z"]
