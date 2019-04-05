#!/usr/bin/env bash
sudo cp clock.service /etc/systemd/system/clock.service
sudo systemctl enable clock.service
sudo systemctl start clock.service