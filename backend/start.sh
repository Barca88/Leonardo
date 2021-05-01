#!/bin/bash

killall flask
export FLASK_APP=leonardo.py
SUCCESS=$(nohup flask run > logs/accesslog.txt) 
echo $SUCCESS
exit 0
