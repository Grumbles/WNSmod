#!/bin/bash
# Simply runs the WNS automoderator once every ten minutes

while true
do
    python WNSmod.py
    sleep 600
done
