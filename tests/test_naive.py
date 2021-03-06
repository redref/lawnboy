# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import lawnboy
from lawnboy.mower import NaiveMower


def test_collision(mocker):
    """
    This lawn naturally make mower collision
    Testing handling of this case correctly
    """
    args = '-H 5 -W 2 -m 0,0,O 0,5,N -s naive'
    # Check we can solve it
    ret = lawnboy.main(args)
    assert ret == 0
    # Check there was a collision
    m_col = mocker.patch.object(NaiveMower, 'collision')
    ret = lawnboy.main(args)
    assert m_col.call_count > 0


def test_lot_of_lawn():
    args = '-H 50 -W 50 -m 0,0,O 0,50,N 50,0,S 50,50,E -s naive'
    ret = lawnboy.main(args)
    assert ret == 0
