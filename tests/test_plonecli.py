#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `plonectl` package."""

from __future__ import absolute_import
from click.testing import CliRunner
from plonectl import cli

import pytest


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    # assert 'Plone Command Line Interface' in result.output

    help_result = runner.invoke(cli.cli, ['--help'])
    assert help_result.exit_code == 0
    assert 'Usage: ctl' in help_result.output

    help_result = runner.invoke(cli.cli, ['-h'])
    assert help_result.exit_code == 0
    assert 'Usage: ctl' in help_result.output

    version_result = runner.invoke(cli.cli, ['-V'])
    assert version_result.exit_code == 0
    assert 'Available packages:' in version_result.output

    version_result = runner.invoke(cli.cli, ['--versions'])
    assert version_result.exit_code == 0
    assert 'Available packages:' in version_result.output
