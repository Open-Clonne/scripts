#!/bin/bash

echo "Updating and Upgrading Packages"
sudo apt update -y && sudo apt upgrade -y

echo "Install system apps"
sudo apt install apt-transport-https ca-certificates curl software-properties-common

echo "Get and install docker keys"
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

echo "Setting environment variable for os flavor"
FLAVOR=`uname -s`

echo "Update apt-repository"
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $FLAVOR stable"

echo "Update apt packages"
sudo apt update

echo "Install docker"
sudo apt install docker-ce

echo "All done!"

