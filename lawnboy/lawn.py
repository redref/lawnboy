# -*- coding: utf-8 -*-
import logging
from bitarray import bitarray

from lawnboy.mower import Mower, NaiveMower, GRASS, CLEAN

logger = logging.getLogger('lawnboy')


class Lawn(object):
    mower_cls = Mower

    def __init__(self, width, height):
        self.width = width + 1  # indexed at 0
        self.height = height + 1
        # Local lawn state per coord
        self.state = [
            bitarray([GRASS for w in range(self.width)])
            for h in range(self.height)]
        self.mowers = []
        self.remaining = self.width * self.height

    def add_mower(self, x, y, o):
        """
        Init mower on this lawn
        """
        self.mowers.append(self.mower_cls(self, x, y, o))

    def do_cut(self, x, y):
        if self.state[y][x] == GRASS:
            self.remaining -= 1
            self.state[y][x] = CLEAN

    def mow(self):
        """
        Output mower instructions
        """
        raise NotImplementedError()

    def draw(self):
        """
        Output intermediate drawing on log output
        (not suitable on really big lawns)
        """
        if not logger.isEnabledFor(logging.DEBUG):
            return
        logger.debug(''.join(['-' for i in range(self.width)]))
        for y, line in enumerate(reversed(self.state)):
            print_line = ''
            for x, pos in enumerate(line):
                if pos == GRASS:
                    print_line += ' '
                else:
                    for mower in self.mowers:
                        if x == mower.x and y == mower.y:
                            print_line += '#'
                            break
                    else:
                        print_line += 'X'
            logger.debug(print_line)
        logger.debug(''.join(['-' for i in range(self.width)]))


class NaiveLawn(Lawn):
    """
    Lawn using NaiveMower and axis parallel pattern
    """
    mower_cls = NaiveMower

    def __init__(self, *args, **kwargs):
        super(NaiveLawn, self).__init__(*args, **kwargs)

        if self.width >= self.height:
            self.flow = 'horizontal'
        else:
            self.flow = 'vertical'
        logger.debug('Flow is : %s' % self.flow)

    def mow(self):
        max_iterate = self.height * self.width * 2
        count = 0
        self.draw()
        while self.remaining > 0:
            for mower in self.mowers:
                logger.debug(mower)
                mower.move()
            self.draw()
            # Anti infinite loop
            if count > max_iterate:
                raise Exception('Did not find a solution, mowing incomplete')
            count += 1

        logger.debug('Mow completed in %s moves' % count)
        return count
