#!/bin/bash
sudo apt-get update
sudo apt-get -y install cron

sudo systemctl start cron
sudo systemctl status cron
