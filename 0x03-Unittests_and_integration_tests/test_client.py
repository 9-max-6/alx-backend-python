#!/usr/bin/env python3
"""testsuite"""
import unittest
import client
from unittest.mock import patch, MagicMock, PropertyMock
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
        self.assertEqual(client.org(), resp)
        expected_arg = f"https://api.github.com/orgs/{org}"
        mock_get_json.assert_called_once_with(expected_arg)

    def test_public_repos_url(self):
        """a method to test GithubOrgClient._public_repos_url property."""
        module = "client.GithubOrgClient.org"
        with patch(module, new_callable=PropertyMock) as mock:
            TEST_PAYLOAD = {
                "repos_url": "https://api.github.com/orgs/google/repos"
                }
            mock.return_value = TEST_PAYLOAD
            self.assertEqual(
                GithubOrgClient("google")._public_repos_url,
                TEST_PAYLOAD.get("repos_url")
                )
