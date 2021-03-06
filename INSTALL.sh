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

interface=$1
frequency=$2
scantime=$3
mkdir -p /root/logs && mkdir -p /mnt/data/tmp/ && printf "\033[92m\nStarting Installer for EAPD...\n\n\033[0m" && printf "Starting Installer for EAPD at $(date '+%r on %x')\n" >> /root/logs/install.log
read -s -n 1 -t 15 -p "On models before the MK7, or other openwrt, please look at the wiki under Requirements. Turn off PineAP then Press any key to continue . . . or ctrl+c to stop"
printf "\n\n" && opkg update && opkg install mariadb-server --force-overwrite && opkg install mariadb-client --force-overwrite
opkg install python --force-overwrite && opkg install python-pip --force-overwrite
python -m pip install wheel && python -m pip install netaddr scapy
/etc/init.d/cron stop && /etc/init.d/cron disable && /etc/init.d/mysqld stop /etc/init.d/mysqld disable
rm -f -r /pineapple/modules/eapd/ && cp -f MODULE/eapd-master.tar.gz /pineapple/modules/eapd-master.tar.gz
tar x -z -f /pineapple/modules/eapd-master.tar.gz -C /pineapple/modules/ && rm -f /pineapple/modules/eapd-master.tar.gz
cp -f EAPD.py /root/eapd.py && cp -f CRONTABS /etc/crontabs/root && cp -f EAPDD /etc/init.d/eapdd
chmod 500 /etc/init.d/eapdd && chmod 500 /root/eapd.py
printf "innodb_use_native_aio = 0\n" >> /etc/mysql/conf.d/50-server.cnf
uci set mysqld.general.enabled='1' && uci commit
rm -f /etc/rc.local && printf "/etc/init.d/eapdd stop\nexit 0" > /etc/rc.local && sleep 10
/etc/init.d/eapdd disable && opkg install python-mysql --force-overwrite
mysql_installation_secure() {
/etc/init.d/mysqld start && sleep 10 && printf "\nStarting and Securing MYSQL...\n\n"
if [ -z $rootpass ]; then
  rootpass=$(openssl rand -base64 16)
fi
mysql -u root <<-EOF
UPDATE mysql.user SET Password=PASSWORD('$rootpass') WHERE User='root';
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
DELETE FROM mysql.user WHERE User='';
DELETE FROM mysql.db WHERE Db='test' OR Db='test_%';
FLUSH PRIVILEGES;
EOF
sleep 1 && /etc/init.d/mysqld stop && printf "Stopped and Secured MySQL.\n\n"
}
if [ -f /etc/config/eapdd ]; then
  source /etc/config/eapdd
  rootpass=$password
  mysql_installation_secure
else
  mysql_install_db --force
  mysql_installation_secure
  printf "###################################" > /etc/config/eapdd
  chmod 200 /etc/config/eapdd
  sed -i "1ipassword='$rootpass'\n" /etc/config/eapdd
fi
if [ -z $interface ]; then
  read -n 1 -t 25 -p "Please select an interface Wlan[0-9]: " interface
  if [ -z $interface ]; then
    interface=1
    sed -i "1iinterface=wlan$interface" /etc/config/eapdd
  else
    sed -i "1iinterface=wlan$interface" /etc/config/eapdd
  fi
  printf "\nSet interface to wlan$interface."
fi
if [ -z $frequency ]; then
  printf "\n\n" && read -n 1 -t 25 -p "Please select the frequency your card supports [2(Ghz)/5(Ghz)]: " frequency
  if [ -z $frequency ]; then
    frequency=2
    sed -i "1ifrequency=$frequency" /etc/config/eapdd
  else
    sed -i "1ifrequency=$frequency" /etc/config/eapdd
  fi
  printf "\nSet frequency to "$frequency"Ghz."
fi
if [ -z $scantime ]; then
  printf "\n\n" && read -n 2 -t 25 -p "Please select the scantime in seconds [30-90]: " scantime
  if [ -z $scantime ]; then
    scantime=60
    sed -i "1iscantime=$scantime" /etc/config/eapdd
    sed -i "1i###############VARS################\n" /etc/config/eapdd
  else
    sed -i "1iscantime=$scantime" /etc/config/eapdd
    sed -i "1i###############VARS################\n" /etc/config/eapdd
  fi
  printf "\nSet scantime to $scantime.\n"
fi && printf "\n"
chmod 400 /etc/config/eapdd
if [ -f /etc/config/eapd-cron ]; then
  printf ""
else
  printf "###################################" > /etc/config/eapd-cron
  chmod 200 /etc/config/eapd-cron
  sed -i "1ilast_runs='24,48'\n" /etc/config/eapd-cron
  sed -i "1ilast_expo='0 23'" /etc/config/eapd-cron
  sed -i "1iruns='first_runs'" /etc/config/eapd-cron
  sed -i "1iexpo='first_expo'" /etc/config/eapd-cron
  sed -i "1i###############VARS################\n" /etc/config/eapd-cron
  chmod 400 /etc/config/eapd-cron
fi
printf "Installer Complete.\n\n" && printf "Installer Complete at $(date '+%r on %x')\n" >> /root/logs/install.log
printf "|-----------------------------------------README!-----------------------------------------|\n\n"
printf "Log file saved to /root/logs/install.log.\n\n"
printf "Just run '/etc/init.d/eapdd L' to start learning mode.\n\n"
printf "|-------------------------------------------END-------------------------------------------|\n" >> /root/logs/install.log
exit 0
