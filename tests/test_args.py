# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import io

import lawnboy


def test_version():
    ret = lawnboy.main('-v')
    assert ret == 0


def test_required_args():
    ret = lawnboy.main('-H 5 -m 1,2,O')
    assert ret == 2


def test_input_parser(mocker):
    input_str = """5 5
    1 2 N
    5 5 O
    """
    mocker.patch('sys.stdin', io.StringIO(input_str))
    ret = lawnboy.main('-i -o')
    assert ret == 0


def test_simple_mow():
    ret = lawnboy.main('-H 5 -W 5 -m 1,2,O')
    assert ret == 0


def test_debug():
    ret = lawnboy.main('-H 5 -W 5 -m 1,2,O -d')
    assert ret == 0


def test_double_mow():
    ret = lawnboy.main('-H 5 -W 5 -m 1,2,O 3,4,N')
    assert ret == 0


def test_double_vertical():
    ret = lawnboy.main('-H 25 -W 5 -m 1,2,O 3,4,N')
    assert ret == 0
