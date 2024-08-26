#!/usr/bin/env python3
"""testsuite"""
import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from parameterized import parameterized, parameterized_class
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


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Use @parameterized_class to decorate the class and parameterize it
    with fixtures found in fixtures.py. The file contains
    the following fixtures:
    org_payload,
    repos_payload,
    expected_repos,
    apache2_repos
    The setupClass should mock requests.get to
    return example payloads found in the fixtures.
    Use patch to start a patcher named get_patcher,
    and use side_effect to make sure the mock of requests.get(url).json()
    returns the correct fixtures for the various values of url that
    you anticipate to receive.
    Implement the tearDownClass class method to stop the patcher.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Start the patcher"""
        def fetch_payload(url):
            """Side effect"""
            if url == 'https://api.github.com/orgs/google':
                return cls.org_payload
            elif url == 'https://api.github.com/google/repos':
                return cls.repos_payload
            else:
                return
        
        module = "requests.get"
        cls.get_patcher = patch(module, side_effect=fetch_payload)
        cls.get_patcher.start()
    
    @classmethod
    def tearDownClass(cls) -> None:
        """Stop the patcher"""
        cls.get_patcher.stop()
    

    def test_public_repos(self) -> None:
        """Tests the `public_repos` method."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """Tests the `public_repos` method with a license."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )
