#!/bin/bash

# clear
clear

# echo command
echo "Starting up IDE"

# cd into the directory
cd ~/c9sdk

# run command
./server.js -p 8080 -l localhost -a : -w /var/www 
