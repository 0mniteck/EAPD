#!/bin/ash
# INSTALL.sh

######################################################################
#
# Copyright (C) 2020 Shant Patrick Tchatalbachian
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
printf "\033[92m\n\nStarting Installer for EAPD...\n\n" && printf "Starting Installer for EAPD at $(date '+%r on %x')\n" >> /root/logs/install.log
read -s -n 1 -p "On models before the MK7, or other openwrt, please look at the wiki under Requirements. Turn off PineAP then Press any key to continue . . . or ctrl+c to stop" && printf "\n\n"
mkdir /mnt/data/ && mkdir /mnt/data/mysql/ && mkdir /mnt/data/tmp/
chmod 777 /mnt/data/ && chmod 777 /mnt/data/mysql/ && chmod 777 /mnt/data/tmp/
mkdir /var/log/mysql/ && chmod 777 /var/log/mysql/
mkdir /var/log/mysqld/ && chmod 777 /var/log/mysqld/
mkdir /var/run/mysqld/ && chmod 777 /var/run/mysqld/
opkg update && opkg --autoremove --force-removal-of-dependent-packages remove git-http
opkg install mariadb-server
opkg install mariadb-client
opkg install mariadb-server-extra
opkg install python --force-overwrite
opkg install python-pip --force-overwrite
#python -m pip install --upgrade pip
python -m pip install wheel
python -m pip install netaddr
python -m pip install scapy
/etc/init.d/cron stop && /etc/init.d/cron disable && /etc/init.d/mysqld stop
mkdir /pineapple/
mkdir /pineapple/modules/
mkdir /pineapple/modules/EAPD/
cp -fr MODULE/* /pineapple/modules/EAPD/
cp -f EAPD.py /root/eapd.py && cp -f CRONTABS /etc/crontabs/root
cp -f DAEMON/MYSQLD /etc/init.d/mysqld && cp -f DAEMON/EAPDD /etc/init.d/eapdd
chmod 744 /etc/init.d/mysqld && chmod 744 /etc/init.d/eapdd
chmod +x /etc/init.d/mysqld && chmod +x /etc/init.d/eapdd
printf 'innodb_use_native_aio = 0\n' >> /etc/mysql/conf.d/50-server.cnf
/etc/init.d/mysqld disable && /etc/init.d/eapdd disable && mysql_install_db --force && opkg install python-mysql
/etc/init.d/mysqld start && printf "\n\n"
read -s -n 1 -p "Make sure MySQL is fully started!!! then press any key to continue . . . or ctrl+c to stop" && printf "\n\n"
#mysql_secure_installation
rootpass=$(openssl rand -base64 16)
mysql -u root <<-EOF
UPDATE mysql.user SET Password=PASSWORD('$rootpass') WHERE User='root';
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
DELETE FROM mysql.user WHERE User='';
DELETE FROM mysql.db WHERE Db='test' OR Db='test_%';
FLUSH PRIVILEGES;
EOF
/etc/init.d/mysqld stop
sed -i '32i        password=$rootpass' /etc/init.d/eapdd
rm /etc/rc.local
printf '/etc/init.d/eapdd stop\n' > /etc/rc.local && printf "\n\n"
printf "Installer Complete.\n\n" && printf "Installer Complete at $(date '+%r on %x')\n" >> /root/logs/install.log
printf "|-----------------------------------------README!-----------------------------------------|\n\n"
printf "Log file saved to /root/logs/install.log.\n\n"
printf "Add the password '$rootpass' to line 666 of /root/eapd.py\n\n"
printf "Then just run '/etc/init.d/eapdd L' to start learning mode.\n\n"
printf "|-------------------------------------------END-------------------------------------------|\n" >> /root/logs/install.log
exit
