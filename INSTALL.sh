#!/bin/bash
# WIP Adding pre-requisites to installer soon
/etc/init.d/cron stop
/etc/init.d/mysqld disable
mv EvilAPDefender.py ~/
mv CRONTABS /etc/crontabs/root
mv EAPD /etc/init.d/eapd
chmod 744 /etc/init.d/eapd
chmod +x /etc/init.d/eapd
/etc/init.d/eapd disable
