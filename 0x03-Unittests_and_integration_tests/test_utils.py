#!/usr/bin/env python3
"""module: test suite"""
import unittest
import requests
from unittest.mock import patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """A class to implement the test cases for the
    utils.access_nested_map function
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """test that the method returns- supposed to return"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """A function to assert that a keyerror is raised for some inputs."""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """A class to test the utils.get_json() function"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """A function to implement the test logic
        steps
        1. Create a context manager using patch
        2. The object in the context manager should be
            a Mock object that has a method that returns
            test_payload
        3. Set the return value of the method to be the test_payload
        4. Set the return value of the mocked method to be the mock object.
        """
        mock = unittest.mock.Mock()
        mock.json.return_value = test_payload
        with patch('requests.get', return_value=mock) as m:
            self.assertEqual(get_json(test_url), test_payload)
            m.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """A class to implement the memoization function in utils.py"""

    def test_memoize(self):
        """a function to implement the actual test"""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as m:
            test = TestClass()
            first_resp = test.a_property()
            sec_resp = test.a_property()

            self.assertEqual(first_resp, 42)
            self.assertEqual(sec_resp, 42)
            m.assert_called_once()
