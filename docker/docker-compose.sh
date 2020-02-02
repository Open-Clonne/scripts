#!/bin/bash

echo "Setting version to variable"
VERSION=1.25.4

echo "Installing docker-compose"
sudo curl -L "https://github.com/docker/compose/releases/download/$VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

echo "Set symlink"
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

echo "Set permissions"
sudo chmod +x /usr/local/bin/docker-compose

echo "Check version"
docker-compose --version

echo "All done!"

