#!/bin/bash

/usr/bin/find ./document/images/drawio -name *.drawio -exec rm -f {}.pdf \; -exec /usr/local/bin/draw.io --crop -x -o {}.pdf {} \;

