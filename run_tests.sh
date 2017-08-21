#!/usr/bin/env bash

. ./sourceme_bash.sh``
python -m unittest discover -s ./tests -p "*test.py"