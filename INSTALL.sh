#!/bin/bash
echo "Starting Installer for EAPD..."
echo "Starting Installer for EAPD at $(date -u)" >> /root/eapd.log
mkdir /mnt/data/ && mkdir /mnt/data/mysql/ && mkdir /mnt/data/tmp/
mkdir /var/log/mysql/ && chmod 777 /var/log/mysql/
mkdir /var/run/mysqld/ && chmod 777 /var/run/mysqld/
chmod 777 /mnt/data/ && chmod 777 /mnt/data/mysql/ && chmod 777 /mnt/data/tmp/
opkg update && opkg --autoremove --force-removal-of-dependent-packages remove git git-http
opkg install procps-ng-pkill aircrack-ng mysql-server mariadb-client mariadb-server-plugin-auth-socket python python-pip
pip install netaddr scapy
/etc/init.d/cron stop && /etc/init.d/cron disable && /etc/init.d/mysqld stop
mkdir /pineapple/ && mkdir /pineapple/modules/ && mkdir /pineapple/modules/eapd/
mkdir /pineapple/modules/eapd/api/ && mkdir /pineapple/modules/eapd/js/
cp -f EAPD.py /root/eapd.py && cp -f CRONTABS /etc/crontabs/root
cp -f MODULE/MODULE.info /pineapple/modules/eapd/module.info
cp -f MODULE/MODULE.html /pineapple/modules/eapd/module.html
cp -f MODULE/MODULE.php /pineapple/modules/eapd/api/module.php
cp -f MODULE/MODULE.js /pineapple/modules/eapd/js/module.js
cp -f DAEMON/MYSQLD /etc/init.d/mysqld && cp -f DAEMON/EAPDD /etc/init.d/eapdd
chmod 744 /etc/init.d/mysqld && chmod 744 /etc/init.d/eapdd
chmod +x /etc/init.d/mysqld && chmod +x /etc/init.d/eapdd
/etc/init.d/mysqld disable && /etc/init.d/eapdd disable && mysql_install_db --force && opkg install python-mysql
echo "Installer Complete." && echo "Installer Complete at $(date -u)" >> /root/eapd.log
echo "Log file saved to /root/eapd.log."
echo "Just run '/etc/init.d/eapdd L' to start learning mode."
echo "|-------------------------------------------END-------------------------------------------|" >> /root/eapd.log
exit
