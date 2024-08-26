#!/usr/bin/env python3
"""testsuite"""
import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from parameterized import parameterized
from typing import Dict, List
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


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

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """A function to test the publick repos function of the GithubOrgClient
        steps
        1. Mock get json. make it return a payload
        2. Mock _public_repos_url to return something
        3. Assert that both return the same thing.
        4. public_repos ->
        """
        mock_get_json.return_value = TEST_PAYLOAD[0][1]
        expected = TEST_PAYLOAD[0][2]
        prop_string = 'client.GithubOrgClient._public_repos_url'

        with patch(prop_string, new_callable=PropertyMock) as mock:
            mock.return_value = TEST_PAYLOAD[0][0]["repos_url"]
            client = GithubOrgClient("google")
            resp = client.public_repos()

            self.assertEqual(resp, expected)
            mock.assert_called_once()

        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
        ])
    def test_has_license(self, lic: Dict, lic_key: str, exp: bool) -> None:
        """A function to test has_license"""
        resp = GithubOrgClient.has_license(lic, lic_key)
    
        self.assertEqual(resp, exp)
