#This is test case

from writing_unit_test import rearrange_name
import unittest

#provide a TestCase Class
#writing our own test class

class TestRearrange(unittest.TestCase):
    def test_basic(self):
        testcase = "Lovelace,Ada"
        expected = "Ada Lovelace"
        self.assertEqual(rearrange_name(testcase),expected)

    def test_input(self):
        testcase = ''
        expected = ''
        self.assertEqual(rearrange_name(testcase),expected)

unittest.main()
