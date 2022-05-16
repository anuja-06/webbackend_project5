#!/bin/sh

mkdir -p ./var
python3 -m pip install nltk
python3 -m pip install datetime
python3 -m pip install pyenchant
python3 -m pip install alt-profanity-check
python3 -m pip install sklearn --upgrade
python3 ./bin/init.py
mv *.db ./var/
