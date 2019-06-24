#!/bin/bash
# WIP adding niceness option for nano installs to prevent crashes with extroot
echo "Starting Installer for EAPD..."
echo "Starting Installer for EAPD at $(date -u)" >> /root/EvilAPDefender.log
opkg update
opkg install aircrack-ng
opkg install mysql-server
opkg install python
opkg install python-mysqldb
opkg install python-pip
pip install netaddr
pip install scappy
/etc/init.d/cron stop && /etc/init.d/cron disable
/etc/init.d/mysqld stop
mv -f EvilAPDefender.py ~/
mv -f CRONTABS /etc/crontabs/root
mv -f MYSQLD /etc/init.d/mysqld
mv -f EAPDD /etc/init.d/eapdd
chmod 744 /etc/init.d/mysqld
chmod 744 /etc/init.d/eapdd
chmod +x /etc/init.d/mysqld
chmod +x /etc/init.d/eapdd
/etc/init.d/mysqld disable
/etc/init.d/eapd disable
echo "Installer Complete."
echo "Just run /etc/init.d/eapdd L to start learning mode."
echo "Then run /etc/init.d/cron enable && /etc/init.d/cron start to begin scheduled runs."
echo "Installer Complete at $(date -u)" >> /root/EvilAPDefender.log
exit
