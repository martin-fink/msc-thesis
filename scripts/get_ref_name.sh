#!/usr/bin/env bash

git describe --tags --dirty --always | tr -d '\n' | sed 's/^v\(.*\)/\1/'
