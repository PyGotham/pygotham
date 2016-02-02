#!/bin/bash
export PATH=/usr/local/python/3.5/bin:$PATH
uwsgi --ini ./uwsgi.ini
