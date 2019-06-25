#!/bin/bash
echo "Starting Uninstaller for EAPD..."
echo "Starting Uninstaller for EAPD at $(date -u)" >> /root/eapd.log
/etc/init.d/cron stop && /etc/init.d/cron disable && /etc/init.d/eapd stop
pip uninstall -y netaddr scappy
opkg --autoremove remove mysql-server python python-mysqldb python-pip
rm -f /root/eapd.py
rm -f /etc/crontabs/root
rm -f /etc/init.d/mysqld
rm -f /etc/init.d/eapdd
rm -f -r /pineapple/modules/eapd
rm -f -r /mnt/data
echo "Uninstaller Complete."
echo "If this is not a Wifi-Pineapple remove Aircrack-ng manually by running 'opkg remove aircrack-ng'."
echo "Log file saved to /root/eapd.log."
echo "Uninstaller Complete at $(date -u)" >> /root/eapd.log
echo "|-------------------------------------------END-------------------------------------------|" >> /root/eapd.log
exit
