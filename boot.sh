#!/bin/sh
source venv/bin/activate

python setup.py 1
exec python finance.py
