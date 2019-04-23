# -*- coding: utf-8 -*-

import os
import pytest
import sys


@pytest.fixture(scope='module')
def plonectl_bin():
    bin_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    plonectl_bin = bin_path + '/plonectl'
    print('plonebin path: ' + plonectl_bin)
    yield plonectl_bin
