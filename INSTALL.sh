#!/bin/bash
# WIP adding niceness option for nano installs to prevent crashes with extroot
echo "Starting Installer for EAPD..."
echo "Starting Installer for EAPD at $(date -u)" >> /root/eapd.log
opkg update
opkg install aircrack-ng
mkdir /mnt/data/
mkdir /mnt/data/mysql/
opkg install mysql-server
mysql_install_db --force
opkg install python python-mysqldb python-pip
pip install netaddr
pip install scappy
/etc/init.d/cron stop && /etc/init.d/cron disable
/etc/init.d/mysqld stop
mkdir /pineapple/modules/eapd/
mkdir /pineapple/modules/eapd/api/
mkdir /pineapple/modules/eapd/js/
mv -f EAPD.py /root/eapd.py
mv -f CRONTABS /etc/crontabs/root
mv -f MODULE/MODULE.info /pineapple/modules/eapd/module.info
mv -f MODULE/MODULE.html /pineapple/modules/eapd/module.html
mv -f MODULE/MODULE.php /pineapple/modules/eapd/api/module.php
mv -f MODULE/MODULE.js /pineapple/modules/eapd/js/module.js
mv -f DAEMON/MYSQLD /etc/init.d/mysqld
mv -f DAEMON/EAPDD /etc/init.d/eapdd
chmod 744 /etc/init.d/mysqld
chmod 744 /etc/init.d/eapdd
chmod +x /etc/init.d/mysqld
chmod +x /etc/init.d/eapdd
/etc/init.d/mysqld disable
/etc/init.d/eapdd disable
echo "Installer Complete."
echo "Just run /etc/init.d/eapdd L to start learning mode. Log file saved to /root/eapd.log."
echo "Installer Complete at $(date -u)" >> /root/eapd.log
echo "|-------------------------------------------END-------------------------------------------|" >> /root/eapd.log
exit
