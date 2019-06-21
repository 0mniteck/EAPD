#!/bin/bash
# WIP
Git clone Https://github.com/0mniteck/EvilAPDefender
mv EvilAPDefender.py ~/
mv CRONTABS /etc/crontabs/root
mv EAPD /etc/init.d/eapd
chmod 744 /etc/init.d/eapd
chmod +x /etc/init.d/eapd
