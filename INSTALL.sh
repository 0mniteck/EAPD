#!/bin/bash
# WIP adding niceness option for nano installs to prevent crashes with extroot
echo "Starting Installer for EAPD"
echo "Starting Installer for EAPD at $(date -u)" >> /root/EvilAPDefender.log
opkg update
opkg install aircrack-ng
opkg install python
opkg install mysql-server
opkg install python-mysqldb
pip install netaddr
pip install scappy
/etc/init.d/cron stop
/etc/init.d/mysqld disable
mv EvilAPDefender.py ~/
mv CRONTABS /etc/crontabs/root
mv EAPD /etc/init.d/eapd
chmod 744 /etc/init.d/eapd
chmod +x /etc/init.d/eapd
/etc/init.d/eapd disable
echo "Installer complete"
echo "Installer complete at $(date -u)" >> /root/EvilAPDefender.log
