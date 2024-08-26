#!/usr/bin/env python3
"""testsuite"""
import unittest
import client
from unittest.mock import patch, MagicMock
from parameterized import parameterized
from typing import Dict
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """class: tests"""

    @parameterized.expand([
        ("google", {'login': "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch('client.get_json')
    def test_org(self, org: str, resp: Dict, mock_get_json: MagicMock) -> None:
        """a function to test the GithubOrgClient.org"""
        mock = MagicMock(return_value=resp)
        mock_get_json.return_value = mock

        client = GithubOrgClient(org)
        self.assertEqual(client.org, resp)
        expected_arg = f"https://api.github.com/orgs/{org}"
        mock_get_json.assert_called_once_with(expected_arg)
