#!/bin/bash

# Main domains first
DOMAINS="-d pygotham.org -d www.pygotham.org"
# Add the yearly subdomains
DOMAINS="$DOMAINS -d 2014.pygotham.org -d 2015.pygotham.org -d 2016.pygotham.org -d 2017.pygotham.org"
# Store the challenge in a tmp dir (only needed when letsencrypt is running)
WEBROOT_PATH="/tmp/letsencrypt-auto"
mkdir -p $WEBROOT_PATH
letsencrypt --renew certonly --webroot --webroot-path $WEBROOT_PATH --agree-tos $DOMAINS
service nginx reload
