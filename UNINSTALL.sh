#!/bin/bash
echo "Starting Uninstaller for EAPD..."
echo "Starting Uninstaller for EAPD at $(date -u)" >> /root/eapd.log
/etc/init.d/cron stop && /etc/init.d/cron disable
/etc/init.d/eapd stop
opkg remove mysql-server
pip remove netaddr
pip remove scappy
opkg remove python python-mysqldb python-pip
rm -f /root/eapd.py
rm -f /etc/crontabs/root
rm -f -r /pineapple/modules/eapd
rm -f -r /mnt/data
rm -f /etc/init.d/mysqld
rm -f /etc/init.d/eapdd
echo "Uninstaller Complete."
echo "Log file saved to /root/eapd.log."
echo "Uninstaller Complete at $(date -u)" >> /root/eapd.log
echo "|-------------------------------------------END-------------------------------------------|" >> /root/eapd.log
exit
