#!/bin/bash
export PATH=/usr/local/python/3.4/bin:$PATH
uwsgi --ini ./uwsgi.ini
