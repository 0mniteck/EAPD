#!/bin/ash
# INSTALL.sh

######################################################################
#
# Copyright (C) 2019 Shant Patrick Tchatalbachian
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>
#
######################################################################

mkdir /root/logs
echo "Starting Installer for EAPD..." && echo " " && echo "Starting Installer for EAPD at $(date -u)" >> /root/logs/install.log
mkdir /mnt/data/ && mkdir /mnt/data/mysql/ && mkdir /mnt/data/tmp/
chmod 777 /mnt/data/ && chmod 777 /mnt/data/mysql/ && chmod 777 /mnt/data/tmp/
mkdir /var/log/mysql/ && chmod 777 /var/log/mysql/
mkdir /var/log/mysqld/ && chmod 777 /var/log/mysqld/
mkdir /var/run/mysqld/ && chmod 777 /var/run/mysqld/
opkg update && opkg --autoremove --force-removal-of-dependent-packages remove git-http
opkg install procps-ng-pkill mysql-server mariadb-client mariadb-server-extra python python-pip
pip install --upgrade pip
pip install wheel
pip install netaddr scapy
/etc/init.d/cron stop && /etc/init.d/cron disable && /etc/init.d/mysqld stop
mkdir /pineapple/
mkdir /pineapple/modules/
mkdir /pineapple/modules/eapd/ && mkdir /pineapple/modules/eapd/api/ && mkdir /pineapple/modules/eapd/js/
cp -f EAPD.py /root/eapd.py && cp -f CRONTABS /etc/crontabs/root
cp -f MODULE/MODULE.info /pineapple/modules/eapd/module.info
cp -f MODULE/MODULE.html /pineapple/modules/eapd/module.html
cp -f MODULE/MODULE.php /pineapple/modules/eapd/api/module.php
cp -f MODULE/MODULE.js /pineapple/modules/eapd/js/module.js
cp -f DAEMON/MYSQLD /etc/init.d/mysqld && cp -f DAEMON/EAPDD /etc/init.d/eapdd
chmod 744 /etc/init.d/mysqld && chmod 744 /etc/init.d/eapdd
chmod +x /etc/init.d/mysqld && chmod +x /etc/init.d/eapdd
echo 'innodb_use_native_aio = 0' >> /etc/mysql/conf.d/50-server.cnf
/etc/init.d/mysqld disable && /etc/init.d/eapdd disable && mysql_install_db --force && opkg install python-mysql
/usr/bin/mysqld &
mysql_secure_installation &
pkill -f "/usr/bin/mysqld"
echo "Installer Complete." && echo " " && echo "Installer Complete at $(date -u)" >> /root/logs/install.log
echo "Log file saved to /root/logs/install.log." && echo " "
echo "|-----------------------------------------README!-----------------------------------------|" && echo " "
echo "Set Mysql password on line 653 of /root/eapd.py, then just run '/etc/init.d/eapdd L' to start learning mode." && echo " "
echo "|-------------------------------------------END-------------------------------------------|" >> /root/logs/install.log
exit
