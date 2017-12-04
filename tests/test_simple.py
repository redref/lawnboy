import sys
import lawnboy


def test_parsearg():
    sys.argv = 'lawnboy -H 5 -W 5 -m 12O'.split(' ')
    lawnboy.main()
