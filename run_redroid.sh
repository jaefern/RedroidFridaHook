#!/bin/bash

sudo apt install linux-modules-extra-`uname -r`

modprobe binder_linux devices="binder,hwbinder,vndbinder"

docker compose up -d --build