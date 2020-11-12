#!/bin/bash

wget https://golang.org/dl/go1.15.5.linux-amd64.tar.gz

tar -C /usr/local -xzf go1.15.5.linux-amd64.tar.gz

echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.zshrc

source ~/.zshrc

go --version

rm go1.15.5.linux-amd64.tar.gz

