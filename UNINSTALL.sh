#!/bin/ash
# UNINSTALL.sh

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

config=$1
printf "\033[92m\nStarting Uninstaller for EAPD...\n\n\033[0m" && printf "Starting Uninstaller for EAPD at $(date '+%r on %x')\n" >> /root/eapd-uninstall.log
if [ -z $config ]; then
  read -n 1 -t 25 -p "Keep config files? [Y/n]: " config
  if [ $config == "n" ]; then
    printf "\n\nRemoving configs...\n\n"
    rm -f /etc/config/eapdd && rm -f -r /mnt/data/ && rm -f -r /var/log/mysql/ && rm -f -r /var/log/mysqld/ && rm -f -r /var/run/mysqld/
  else
    printf "\n\nKeeping configs...\n\n"
  fi
else
  if [ $config == "-r" ]; then
    printf "\n\nRemoving configs...\n\n"
    rm -f /etc/config/eapdd && rm -f -r /mnt/data/ && rm -f -r /var/log/mysql/ && rm -f -r /var/log/mysqld/ && rm -f -r /var/run/mysqld/
  else
    printf "\n\nKeeping configs...\n\n"
  fi
fi
/etc/init.d/cron stop && /etc/init.d/cron disable && /etc/init.d/eapdd stop && sleep 5 && python -m pip uninstall -y netaddr scapy wheel
opkg --autoremove --force-remove --force-removal-of-dependent-packages remove mariadb-server mariadb-client python python-mysql python-pip
opkg --autoremove --force-remove --force-removal-of-dependent-packages remove mariadb-server mariadb-client python python-mysql python-pip
rm -f /root/eapd.py && rm -f /etc/crontabs/root && rm -f /etc/init.d/eapdd && rm -f /root/eapd.log && rm -f -r /root/logs/
rm -f /etc/config/mysqld && rm -f /etc/mysql/conf.d/50-server.cnf && rm -f /etc/rc.local && printf "exit 0" > /etc/rc.local
rm -f -r /pineapple/modules/eapd/
printf "\nUninstaller Complete.\n\n" && printf "Uninstaller Complete at $(date '+%r on %x')\n" >> /root/eapd-uninstall.log
printf "Log file saved to /root/eapd-uninstall.log.\n\n"
printf "|-------------------------------------------END-------------------------------------------|\n" >> /root/eapd-uninstall.log
exit 0
