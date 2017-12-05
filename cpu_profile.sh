#!/bin/bash

pprofile --exclude-syspath ./cli.py -H 100 -W 100 -m 0,0,O 0,20,N 20,0,S 20,20,E -s naive
