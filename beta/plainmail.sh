#!/bin/bash

source /students/cs304reclib/draft/venv/bin/activate
cd /students/cs304reclib/beta/cron
python cron.py
echo "email sent"