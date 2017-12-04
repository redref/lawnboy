# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import argparse
import logging

import lawnboy.lawn

logging.basicConfig(
    format='%(asctime)s %(message)s',
    level=logging.INFO)
logger = logging.getLogger()

strategies = [
    'naive',
]


def input_parser(stream, args):
    """
    Parse input file format
    Exceptions raised as is
    """
    width, height = stream.readline().strip().split()
    args.height = int(width)
    args.width = int(height)
    args.mower = []
    line = stream.readline().strip()
    while line:
        if len(line) != 0:
            x, y, o = line.split(' ')
            args.mower.append('%s,%s,%s' % (x, y, o))
        line = stream.readline().strip()


def main(argv=None):
    """
    Input and outputs management
    """
    parser = argparse.ArgumentParser(
        description='Mower movement planning program')
    parser.add_argument(
        '-H', '--height', type=int, help='Lawn height')
    parser.add_argument(
        '-W', '--width', type=int, help='Lawn width')
    parser.add_argument(
        '-m', '--mower', nargs='+',
        help='Mower position (XYO)')
    parser.add_argument(
        '-s', '--strategy', choices=['naive'], default='naive',
        help='Move strategy class')
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Move strategy class')
    parser.add_argument(
        '-v', '--version', action='store_true',
        help='Print version')
    parser.add_argument(
        '-i', '--stdin', action='store_true',
        help="Read values from stdin ('width height' on first line,"
        " mowers 'X Y O' on subsequent lines)")
    parser.add_argument(
        '-o', '--out', action='store_true',
        help="Mower format output")
    if argv is not None:
        argv = argv.split(' ')
    args = parser.parse_args(argv)

    if args.version:
        from lawnboy._version import version
        print(version)
        return 0

    if args.debug:
        logger.setLevel(logging.DEBUG)

    if args.stdin:
        if sys.stdin.isatty():
            print('Cannot read from tty input.')
        else:
            input_parser(sys.stdin, args)

    if args.height is None or args.width is None or len(args.mower) == 0:
        print(
            'Lawn height/width and at least one Mower must be specified'
            'by arguments or by formatted input stream.')
        print('')
        parser.print_help()
        return 2

    # Init Lawn
    lawn_cls = getattr(lawnboy.lawn, '%sLawn' % args.strategy.capitalize())
    lawn = lawn_cls(args.width, args.height)

    # Init Mowers
    for mower in args.mower:
        try:
            x, y, o = mower.split(',')
            int(x)
            int(y)
        except:
            raise Exception(
                'Unable to parse "%s" as mower position ("X,Y,O")' % mower)
        lawn.add_mower(int(x), int(y), o)

    # Mow
    moves = lawn.mow()

    if args.out:
        for i, mower in enumerate(lawn.mowers):
            print(mower.instructions)
            print("%s %s %s" % (mower.x, mower.y, mower.o))
    else:
        print("Total moves : %s" % moves)
        for i, mower in enumerate(lawn.mowers):
            print(
                'Mower%s instructions (%s): %s' %
                (i + 1, len(mower.instructions), mower.instructions))
            print(
                'Mower%s final position: %s %s %s' %
                (i, mower.x, mower.y, mower.o))

    return 0
