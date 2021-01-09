#!/bin/ash
# INSTALL.sh

######################################################################
#
# Copyright (C) 2021 Shant Patrick Tchatalbachian
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
printf "\033[92m\nStarting Installer for EAPD...\n\n\033[0m" && printf "Starting Installer for EAPD at $(date '+%r on %x')\n" >> /root/logs/install.log
read -s -n 1 -t 15 -p "On models before the MK7, or other openwrt, please look at the wiki under Requirements. Turn off PineAP then Press any key to continue . . . or ctrl+c to stop"
printf "\n\n" && opkg update && opkg install mariadb-server --force-overwrite && opkg install mariadb-client --force-overwrite
opkg install python --force-overwrite && opkg install python-pip --force-overwrite
#python -m pip install --upgrade pip
python -m pip install wheel netaddr scapy
rm -f -r /pineapple/modules/EAPD
cp -f MODULE/EAPD-master.tar.gz /pineapple/modules/EAPD-master.tar.gz
tar x -z -f /pineapple/modules/EAPD-master.tar.gz -C /pineapple/modules/
rm -f /pineapple/modules/EAPD-master.tar.gz
/etc/init.d/cron stop && /etc/init.d/cron disable
cp -f EAPD.py /root/eapd.py && cp -f CRONTABS /etc/crontabs/root && cp -f EAPDD /etc/init.d/eapdd
chmod 744 /etc/init.d/eapdd && chmod +x /etc/init.d/eapdd
chmod 3400 /root/eapd.py && chmod +x /root/eapd.py
printf 'innodb_use_native_aio = 0\n' >> /etc/mysql/conf.d/50-server.cnf
uci set mysqld.general.enabled='1' && uci commit
rm /etc/rc.local && printf '/etc/init.d/eapdd stop\n' > /etc/rc.local && sleep 10
/etc/init.d/eapdd disable && mysql_install_db --force && opkg install python-mysql
/etc/init.d/mysqld start && sleep 10 && printf "\nStarting and Securing MYSQL...\n\n"
rootpass=$(openssl rand -base64 16)
mysql -u root <<-EOF
UPDATE mysql.user SET Password=PASSWORD('$rootpass') WHERE User='root';
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
DELETE FROM mysql.user WHERE User='';
DELETE FROM mysql.db WHERE Db='test' OR Db='test_%';
FLUSH PRIVILEGES;
EOF
sleep 1 && /etc/init.d/mysqld stop && printf "Stopped and Secured MySQL.\n\n"
sed -i "23i###################################\n" /etc/init.d/eapdd
sed -i "23ipassword='$rootpass'\n" /etc/init.d/eapdd
read -n 1 -t 25 -p "Please select an interface Wlan[0-9]: " interface
printf "\n\n" && read -n 1 -t 25 -p "Please select the frequency your card supports [2(Ghz)/5(Ghz)]: " frequency
printf "\n\n" && read -n 3 -t 25 -p "Please select the scan length in seconds [1-120]: " time
printf "\n"
if [ -z $interface ]; then
  interface=1
fi
if [ -z $frequency ]; then
  frequency=2
fi
if [ -z $time ]; then
  time=60
fi
sed -i "23iinterface=wlan$interface" /etc/init.d/eapdd
sed -i "23ifrequency=$frequency" /etc/init.d/eapdd
sed -i "23itime=$time" /etc/init.d/eapdd
sed -i "23i###############VARS################\n" /etc/init.d/eapdd
chmod 3400 /etc/init.d/eapdd && chmod +x /etc/init.d/eapdd
printf "Installer Complete.\n\n" && printf "Installer Complete at $(date '+%r on %x')\n" >> /root/logs/install.log
printf "|-----------------------------------------README!-----------------------------------------|\n\n"
printf "Log file saved to /root/logs/install.log.\n\n"
printf "Just run '/etc/init.d/eapdd L' to start learning mode.\n\n"
printf "|-------------------------------------------END-------------------------------------------|\n" >> /root/logs/install.log
exit
