#!/bin/bash
rm -f /root/eapd.log
echo "Starting Uninstaller for EAPD..." && echo " \n" && echo "Starting Uninstaller for EAPD at $(date -u)" >> /root/eapd.log
/etc/init.d/cron stop && /etc/init.d/cron disable && /etc/init.d/eapdd stop
sleep 5
pip uninstall -y netaddr scapy
opkg --autoremove --force-removal-of-dependent-packages remove procps-ng-pkill mysql-server mariadb-server mariadb-client mariadb-server-plugin-auth-socket python python-mysql python-pip
rm -f /root/eapd.py && rm -f /etc/crontabs/root && rm -f /etc/init.d/mysqld && rm -f /etc/init.d/eapdd
rm -f -r /pineapple/modules/eapd/ && rm -f -r /mnt/data/ && rm -f -r /var/log/mysql/ && rm -f -r /var/log/mysqld/ && rm -f -r /var/run/mysqld/
opkg --autoremove --force-removal-of-dependent-packages remove procps-ng-pkill mysql-server mariadb-server mariadb-client mariadb-server-plugin-auth-socket python python-mysql python-pip
echo "Uninstaller Complete." && echo " \n" && echo "Uninstaller Complete at $(date -u)" >> /root/eapd.log
echo "If this is not a Wifi-Pineapple remove Aircrack-ng manually by running 'opkg --autoremove remove aircrack-ng airmon-ng'."
echo " \n" && echo "Log file saved to /root/eapd.log."
echo "|-------------------------------------------END-------------------------------------------|" >> /root/eapd.log
exit
