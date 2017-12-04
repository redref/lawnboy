# LawnBoy

[![Build Status](https://travis-ci.org/redref/lawnboy.svg?branch=master)](https://travis-ci.org/redref/lawnboy)
[![Coverage Status](https://coveralls.io/repos/github/redref/lawnboy/badge.svg?branch=master)](https://coveralls.io/github/redref/lawnboy?branch=master)


## Objective

Control and optimise mower(s) move in order to mill your lawn. The program result is instructions to be executed sequentially by mowers.

This program only work on rectangular lawns.

### Theory

Digging on the web, this research paper treat this problem : http://www.ams.sunysb.edu/~estie/papers/lawn.pdf

TODO: Go further into this paper.

## Implementation

### Installation

```
pip install git+https://github.com/redref/lawnboy.git@master
```

### CLI usage

```
lawnboy -W <lawn_width> -H <lawn_height> -m <X,Y,O> [<X,Y,O>]
```

You must specify mower as 'X,Y,O' with X and Y coordinates and O the start orientation (S/O/N/E).

### File input usage

```
echo -e "5 5\n1 2 O\n3 4 S\n" | lawnboy -i -o
```

## TODO

 * Naive stategy is ok when initial positions are not close. This strategy need to be improved to manage all cases.
 * Testing.
 * Collisions between mowers
 * Upload to pypi



