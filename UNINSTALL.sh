#!/bin/ash
# UNINSTALL.sh

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

rm -f /root/eapd.log && rm -f -r /root/logs
echo "Starting Uninstaller for EAPD..." && echo " " && echo "Starting Uninstaller for EAPD at $(date -u)" >> /root/eapd-uninstall.log
/etc/init.d/cron stop && /etc/init.d/cron disable && /etc/init.d/eapdd stop && sleep 5
pip uninstall -y netaddr scapy wheel
opkg --autoremove --force-removal-of-dependent-packages remove procps-ng-pkill mysql-server mariadb-server mariadb-client mariadb-server-extra python python-mysql python-pip
rm -f /root/eapd.py && rm -f /etc/crontabs/root && rm -f /etc/init.d/mysqld && rm -f /etc/init.d/eapdd
rm -f -r /pineapple/modules/EAPD/ && rm -f -r /mnt/data/ && rm -f -r /var/log/mysql/ && rm -f -r /var/log/mysqld/ && rm -f -r /var/run/mysqld/
opkg --autoremove --force-removal-of-dependent-packages remove procps-ng-pkill mysql-server mariadb-server mariadb-client mariadb-server-extra python python-mysql python-pip
echo "Uninstaller Complete." && echo " " && echo "Uninstaller Complete at $(date -u)" >> /root/eapd-uninstall.log
echo " " && echo "Log file saved to /root/eapd-uninstall.log." && echo " "
echo "|-------------------------------------------END-------------------------------------------|" >> /root/eapd-uninstall.log
exit
