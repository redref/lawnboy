import argparse
import logging

import lawnboy.lawn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

strategies = [
    'naive',
]


def main():
    """
    Input and outputs management
    """
    parser = argparse.ArgumentParser(
        description='Mower movement plannng program')
    parser.add_argument(
        '-H', '--height', type=int, required=True,
        help='Lawn height')
    parser.add_argument(
        '-W', '--width', type=int, required=True,
        help='Lawn width')
    parser.add_argument(
        '-m', '--mower', nargs='+', required=True,
        help='Mower position (XYO)')
    parser.add_argument(
        '-s', '--strategy', choices=['naive'], default='naive',
        help='Move strategy class')
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Move strategy class')
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    lawn_cls = getattr(lawnboy.lawn, '%sLawn' % args.strategy.capitalize())

    lawn = lawn_cls(args.width, args.height)
    for mower in args.mower:
        try:
            x, y, o = mower
            int(x)
            int(y)
        except:
            raise Exception(
                'Unable to parse "%s" as mower position ("XYO")' % mower)
        lawn.add_mower(int(x), int(y), o)

    lawn.cut()
