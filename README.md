# LawnBoy

## Objective

Control and optimise mower(s) move in order to mill your lawn. The program result is instructions to be executed sequentially by mowers.

This program only work on rectangular lawns.

### Theory

Digging on the web, this research paper treat this problem : http://www.ams.sunysb.edu/~estie/papers/lawn.pdf

TODO: Go further into this paper.

## Implementation

### Installation

```
pip install .
```

### CLI usage

```
lawnboy -W <lawn_width> -H <lawn_height> -m <XYO> [<XYO>]
```

You must specify

### File input usage

## TODO

 * Naive stategy is ok when initial positions are not close. This strategy need to be improved to manage all cases.
 * Testing.
 * Collisions between mowers
 * Upload to pypi



