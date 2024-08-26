#!/usr/bin/env python3
"""module: test suite"""
import unittest
import utils
from parameterized import parameterized
from utils import access_nested_map


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
    @unittest.mock.patch('utils.get_json')
    def test_get_json(self, mock_get_json, test_url, test_payload):
        """A function to implement the test logic
        steps
        1. Make a mock object
        2. Create a method called json of the mock object
        3. Set the return value of the method to be the test_payload
        4. Set the return value of the mocked method to be the mock object.
        """
        mock = unittest.mock.Mock()
        mock.json.return_value = test_payload
        # print(f"\n\n\n{mock_get_json}\n\n\n")
        # print(f"\n\n\n{test_url}\n\n\n")
        # print(f"\n\n\n{test_payload}\n\n\n")
        mock_get_json.return_value = mock

        # Action
        response = mock_get_json(test_url)

        # Tests
        mock_get_json.assert_called_once_with(test_url)
        self.assertEqual(response, mock)
