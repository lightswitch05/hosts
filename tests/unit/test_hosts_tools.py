from HostsTools import hosts_tools
import os


class TestHostTools(object):

    TEST_FILE_NAME = 'test-write-domain-list.txt'
    TEST_WHITELIST_FILE_NAME = 'test-write-domain-list-whitelist.txt'
    TEST_DOMAINS = {'a.com', 'b.a.com', 'b.com', 'a.b.com'}
    TEST_WHITELIST = {'b.b.com', 'z.com'}

    def setup_class(self):
        with open(self.TEST_WHITELIST_FILE_NAME, 'w') as file:
            for domain in self.TEST_WHITELIST:
                file.write(domain + '\n')

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

    def test_double_quote_is_not_a_valid_domain(self):
        is_valid = hosts_tools.is_valid_domain("\"example.com")
        assert not is_valid

    def test_single_quote_is_not_a_valid_domain(self):
        is_valid = hosts_tools.is_valid_domain("'example.com")
        assert not is_valid

    def test_unicode_is_a_valid_domain(self):
        is_valid = hosts_tools.is_valid_domain(u"www.с\ud0b0.com")
        assert is_valid

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

    def test_build_file_header(self):
        file_name = 'TgM&2BXKw0SWVvync@%Az1cN6.txt'
        count = 23235
        header = hosts_tools.build_file_header(file_name, count)
        assert str(count) in header
        assert file_name in header
        assert '[' not in header
        assert ']' not in header

    def test_write_domain_list(self):
        hosts_tools.write_domain_list(self.TEST_FILE_NAME, self.TEST_DOMAINS)
        assert os.path.isfile(self.TEST_FILE_NAME)

    def test_read_domains_list(self):
        domains = hosts_tools.load_domains_from_list(self.TEST_FILE_NAME)
        assert domains
        assert not self.TEST_DOMAINS.difference(domains)

    def test_missing_whitelist(self):
        whitelist = hosts_tools.load_domains_from_whitelist('not-a-real-file.txt')
        assert len(whitelist) == 0

    def test_reduce_domains(self):
        reduced = hosts_tools.reduce_domains(self.TEST_DOMAINS)
        assert reduced
        assert not {'a.com', 'b.com'}.difference(reduced)

    def teardown_class(self):
        if os.path.isfile(self.TEST_FILE_NAME):
            os.remove(self.TEST_FILE_NAME)
        if os.path.isfile(self.TEST_WHITELIST_FILE_NAME):
            os.remove(self.TEST_WHITELIST_FILE_NAME)
