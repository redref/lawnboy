# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger('lawnboy')


class Mower(object):
    """
    Mower object.
    Need to be extended in order to provide moving awareness
    """
    orientations = 'SONE'

    def __init__(self, lawn, x, y, o):
        if x < 0 or x > lawn.width - 1:
            raise Exception('Mower X "%s" is invalid' % x)
        self.x = x
        if y < 0 or y > lawn.height - 1:
            raise Exception('Mower Y "%s" is invalid' % y)
        self.y = y
        if o not in self.orientations:
            raise Exception('Mower O "%s" is invalid' % o)
        self.o = o

        #
        lawn.state[y][x] = 1
        self.lawn = lawn
        self.instructions = ''

    def orientate_to(self, to):
        if to == self.o:
            return None
        f = self.orientations.index(self.o)
        t = self.orientations.index(to)
        if f - t == -3:
            return 'L'
        return 'R'

    def do_forward(self):
        x = self.x
        y = self.y
        if self.o == 'S':
            y = y - 1
        elif self.o == 'N':
            y = y + 1
        elif self.o == 'O':
            x = x - 1
        elif self.o == 'E':
            x = x + 1
        return x, y

    def do_move(self, instruction):
        """
        Keep coords + lawn state up to date
        """
        logger.debug('Move %s' % instruction)
        self.instructions += instruction
        if instruction == 'R':
            i = self.orientations.index(self.o)
            if i < len(self.orientations) - 1:
                self.o = self.orientations[i+1]
            else:
                self.o = self.orientations[0]
        elif instruction == 'L':
            i = self.orientations.index(self.o)
            if i > 0:
                self.o = self.orientations[i-1]
            else:
                self.o = self.orientations[-1]
        elif instruction == 'F':
            self.lawn.state[self.y][self.x] = 2
            self.x, self.y = self.do_forward()
            self.lawn.do_cut(self.x, self.y)
            self.lawn.state[self.y][self.x] = 1
        else:
            raise Exception('Instruction "%s" is not valid' % instruction)


class NaiveMower(Mower):
    """
    Mower used by NaiveLawn cut strategy
    """
    def __init__(self, *args, **kwargs):
        super(NaiveMower, self).__init__(*args, **kwargs)

        # Choose a working direction
        if self.lawn.flow == 'horizontal':
            if self.lawn.height - 1 - self.y < self.y:
                self.direction = 'N'
            else:
                self.direction = 'S'
        else:
            if self.lawn.width - 1 - self.x < self.x:
                self.direction = 'E'
            else:
                self.direction = 'O'

    def __repr__(self):
        return "X:%s Y:%s O:%s D:%s" % (self.x, self.y, self.o, self.direction)

    def do_move(self, instruction):
        if instruction == 'F':
            x, y = self.do_forward()
            if self.lawn.state[y][x] == 1:
                # Collision
                return self.collision()
        super(NaiveMower, self).do_move(instruction)

    def collision(self):
        """
        Fine collision handling
        """
        return self.do_move('R')

    def move(self):
        """
        Wrapper for vertical/horizontal move functions
        """
        if self.lawn.flow == 'horizontal':
            return self.horizontal_move()
        else:
            return self.vertical_move()

    def horizontal_move(self):
        """
        Implement horizontal strategy
        """
        done, other = self.is_lane_done(y=self.y)
        if done:
            logger.debug('Lane done')
            # Change direction if needed
            if self.direction == 'N' and self.y == (self.lawn.height - 1):
                self.direction = 'S'
            if self.y == 0 and self.direction == 'S':
                self.direction = 'N'

            # 2 mowers on the lane
            if (
                other and self.o not in 'NS' and
                self.x != 0 and self.x != self.lawn.width - 1
            ):
                return self.do_move('F')

            # Follow direction
            move = self.orientate_to(self.direction)
            if move:
                return self.do_move(move)
            return self.do_move('F')

        else:
            # The other way
            if self.x == 0:
                move = self.orientate_to('E')
                if move:
                    return self.do_move(move)
            elif self.x == (self.lawn.width - 1):
                move = self.orientate_to('O')
                if move:
                    return self.do_move(move)
            if self.o in 'EO':
                return self.do_move('F')
            else:
                # Default to right here
                return self.do_move('R')

    def vertical_move(self):
        """
        Implement vertical strategy
        """
        done, other = self.is_lane_done(x=self.x)
        if done:
            logger.debug('Lane done')
            # Change direction if needed
            if self.direction == 'E' and self.x == (self.lawn.width - 1):
                self.direction = 'O'
            if self.x == 0 and self.direction == 'O':
                self.direction = 'E'

            # 2 mowers on the lane
            if (
                other and self.o not in 'EO' and
                self.y != 0 and self.y != self.lawn.height - 1
            ):
                return self.do_move('F')

            # Follow direction
            move = self.orientate_to(self.direction)
            if move:
                return self.do_move(move)
            return self.do_move('F')

        else:
            # The other way
            if self.y == 0:
                move = self.orientate_to('N')
                if move:
                    return self.do_move(move)
            elif self.y == (self.lawn.height - 1):
                move = self.orientate_to('S')
                if move:
                    return self.do_move(move)
            if self.o in 'NS':
                return self.do_move('F')
            else:
                # Default to right here
                return self.do_move('R')

    def is_lane_done(self, x=None, y=None):
        """
        Check a lane (vertical or horizontal) for status
        """
        # If another mower on the lane, skip it
        for mower in self.lawn.mowers:
            if x is not None and mower.x == x and self.y != mower.y:
                return True, True
            if y is not None and mower.y == y and self.x != mower.x:
                return True, True

        # Choose iterate
        if y is not None:
            it = self.is_lane_done_iterator_y
            arg = y
        else:
            it = self.is_lane_done_iterator_x
            arg = x

        # Iterate on grass
        for pos in it(arg):
            if pos == 0:
                return False, False
        return True, False

    def is_lane_done_iterator_y(self, y):
        for i in self.lawn.state[y]:
            yield i

    def is_lane_done_iterator_x(self, x):
        for i in self.lawn.state:
            yield i[x]
