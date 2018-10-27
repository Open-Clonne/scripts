#!/bin/bash

# clear
clear

# echo what we are about to do
echo "Jeffery Clonne - https://jefferyclonne.com"

# install build-essential
echo "installing build-essentials"
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install build-essential

# check and install node
echo "Installing nodejs 8 now"
sudo apt-get update
curl -sL https://deb.nodesource.com/setup_8.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
sudo apt-get install nodejs

# check versions
node -v
npm -v
sudo npm install -g yarn webpack eslint tslint git curl wget

# change directory
cd ~

# clone cloud9 sdk
git clone https://github.com/c9/core.git c9sdk

# change directory into sdk folder
cd ~/c9sdk

# now run
sudo bash scripts/install-sdk.sh

# echo command
echo "Starting up IDE"

# make projects directory
mkdir ~/projects_code

# cd into the directory
cd ~/c9sdk

# run command
./server.js -p 8080 -l localhost -a : -w ~/projects_code 
