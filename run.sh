#!/bin/bash

sed -i "9s/.*/TOKEN = 'NTU5ODA2OTYyNjAzMjYxOTky.D34bqw.q29_sMZoac9GWhD3lDACqmsPtjw'/" bot.py

python3 ./src/bot.py

sed -i "9s/*/TOKEN = ''/" bot.py