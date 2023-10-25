#!/bin/bash


###############################
### DO NOT MODIFY THIS FILE ###
###############################


# Build image
docker build . -t ube-scrape

# Run container, mount volume
docker run --platform linux/amd64 -v $PWD:/opt/mount ube-scrape