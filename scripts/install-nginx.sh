#!/bin/bash

set -eux

sudo apt-get -y update
sudo apt-get -y install nginx

sudo service nginx start

mkdir -p /home/vagrant/files