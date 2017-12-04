# -*- coding: utf-8 -*-
import logging

from lawnboy.mower import *

logger = logging.getLogger('lawnboy')


class Lawn(object):
    mower_cls = Mower

    def __init__(self, width, height):
        self.width = width + 1  # indexed at 0
        self.height = height + 1
        # Local lawn state per coord
        self.state = [
            [0 for w in range(self.width)]
            for h in range(self.height)]
        self.mowers = []

    def add_mower(self, x, y, o):
        """
        Init mower on this lawn
        """
        self.mowers.append(self.mower_cls(self, x, y, o))

    def cut(self):
        """
        Output mower instructions
        """
        self.draw()
        raise NotImplementedError()

    def draw(self):
        """
        Output intermediate drawing on log output
        (not suitable on really big lawns)
        """
        logger.debug(''.join(['-' for i in range(self.width)]))
        for line in reversed(self.state):
            print_line = ''
            for pos in line:
                if pos == 0:
                    print_line += " "
                elif pos == 1:
                    print_line += "#"
                else:
                    print_line += "X"
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

    def cut(self):
        count = 0
        self.draw()
        while self.remaining_lawn() != 0:
            for mower in self.mowers:
                logger.debug(mower)
                mower.move()
            self.draw()
            # Anti infinite loop
            if count > (self.height * self.width * 2):
                raise Exception('No solution found')
            count += 1
        else:
            logger.debug('Completed in %s moves' % count)

        return count,

    def remaining_lawn(self):
        count = 0
        for line in self.state:
            for pos in line:
                if pos == 0:
                    count += 1
        return count
