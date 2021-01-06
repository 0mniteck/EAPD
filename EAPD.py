#!/usr/bin/python
# File: /root/eapd.py

######################################################################
#
# Copyright (C) 2015 Mohamed Idris
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

import MySQLdb
import time
import os
from subprocess import *
import csv
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from netaddr import *
import sys, getopt
import smtplib
import threading

########### Functions Def
# Usage
def Usage():
    print "\n########################USAGE##################################\n"
    print "\nEvil Access Point Defender (EAPD) - Protect your Wireless Network from Bad Access Points\n."
    print "Authors: Mohamed Idris, And Shant Patrick Tchatalbachian\n"
    print "GNU License v3\n\n"
    print "Normal Mode Usage: {} -N \n".format(sys.argv[0])
    print "Learning Mode Usage: {} -L \n".format(sys.argv[0])
    print "Help Screen: {} -h or --help\n".format(sys.argv[0])
    print "\n###############################################################\n"
    sys.exit(2)

# Help information
def Help():
    print "\n############################HELP###############################\n"
    print "\n     Check out the Wiki: https://github.com/0mniteck/EAPD/wiki/Wiki\n\n"
    print "\nUsage:\n"
    print "     - Normal Mode Usage: {} -N \n".format(sys.argv[0])
    print "     - Learning Mode Usage: {} -L \n".format(sys.argv[0])
    print "\n###############################################################\n"
    sys.exit(2)

# Learning choices
def Choices():
    print "\n###############################################################\n"
    print "What do you want to do (please choose a number):"
    print "1. AutoConfig (only choose SSID)"
    print "2. Add specific Access Point"
    print "3. Remove specific Access Point"
    print "4. Remove whitelisted Access Points"
    print "5. Update options"
    print "6. Go into Normal Mode"
    print "7. Nothing, just exit\n"

# Learning options
def Options():
    print "\n###############################################################\n"
    print "What option do you want to update (please choose a number):"
    print "1. Configure Preventive Mode"
    print "2. Admin notification"
    print "3. Return to previous menu\n"

# sending an alert to the admin email
def AlertAdmin(message):
    try:
        cmd = "select opt_val from options where opt_key = 'admin_email'"
        cursor.execute(cmd)
        if cursor.rowcount > 0:
            row = cursor.fetchone()
            admin_email = row[0]
            cmd = "select opt_val from options where opt_key = 'admin_smtp'"
            cursor.execute(cmd)
            if cursor.rowcount > 0:
                row = cursor.fetchone()
                admin_smtp = row[0]
                cmd = "select opt_val from options where opt_key = 'admin_smtp_username'"
                cursor.execute(cmd)
                if cursor.rowcount > 0:
                    row = cursor.fetchone()
                    admin_smtp_username = row[0]
                    cmd = "select opt_val from options where opt_key = 'admin_smtp_password'"
                    cursor.execute(cmd)
                    if cursor.rowcount > 0:
                        row = cursor.fetchone()
                        admin_smtp_password = row[0]
                        message = "From: EvilAP_Defender <{}>\nTo: Admin <{}>\nSubject: EvilAP_Defender Alert!\n\n"\
                            .format(admin_smtp_username, admin_email) + message
                        try:
                            print "\nConnecting to SMTP server\n"
                            mailsrv = smtplib.SMTP(admin_smtp,587)
                            print "\nSending ehlo message to SMTP server\n"
                            mailsrv.ehlo()
                            print "\nStarting TLS with SMTP server\n"
                            mailsrv.starttls()
                            print "\nSending ehlo message to SMTP server\n"
                            mailsrv.ehlo()
                            print "\nLogin to SMTP server\n"
                            mailsrv.login(admin_smtp_username,admin_smtp_password)
                            print "\nSending the message ...\n"
                            mailsrv.sendmail(admin_smtp_username, admin_email, message)
                            print "\nDisconnecting from mail server ...\n"
                            mailsrv.quit()
                            print "\nSuccessfully sent email to admin\n"
                        except:
                            print "\nError: unable to send an email to admin: {}\n".format(sys.exc_info()[0])
                    else:
                        print "Cannot send alert. SMTP password not found!\nConfigure admin notification from Learning Mode\n"
                else:
                    print "Cannot send alert. SMTP username not found!\nConfigure admin notification from Learning Mode\n"
            else:
                print "Cannot send alert. SMTP address not found!\nConfigure admin notification from Learning Mode\n"
        else:
            print "Cannot send alert. Admin email not found!\nConfigure admin notification from Learning Mode\n"
    except:
        print "Unexpected error in 'AlertAdmin': {}\n".format(sys.exc_info()[0])

    return

def Conf_viewSSIDs():
    try:
        cmd = "select * from ssids"
        cursor.execute(cmd)
        if cursor.rowcount > 0:
            ssids_data = cursor.fetchall()
            print "\n###############################################################\n"
            print "Wireless Networks Found:"
            print "ID. (BSSID - SSID - PWR - Channel - Cipher - Privacy - Auth)\n"
            for row in ssids_data:
                cmd = "select * from whitelist where mac=%s and ssid=%s and channel=%s and CIPHER=%s and Enc=%s and Auth=%s"
                cursor.execute(cmd, (row[1],row[2],row[4],row[5],row[6],row[7]))
                if cursor.rowcount > 0:
                    print "{}. ({} - {} - '{}' - {} - {} - {} - {})\n".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
                else:
                    print "{}. ({} - {} - '{}' - {} - {} - {} - {})\n".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
        else:
            print "\nNo Wireless Network Detected!\n"

        cmd = "select * from whitelist"
        cursor.execute(cmd)
        if cursor.rowcount > 0:
            whitelist_data = cursor.fetchall()
            print "\n###############################################################\n"
            print "Whitelisted Access Points:"
            print "ID. (BSSID - SSID - MinPWR - MaxPWR - Channel - Cipher - Privacy - Auth)\n"
            for row in whitelist_data:
                print "{}. ({} - {} - '{}' - '{}' - {} - {} - {} - {})".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
        else:
            print "\nCurrently, There are No Whitelisted Access Points\n"

        cmd = "select * from whitelist_OUIs"
        cursor.execute(cmd)
        if cursor.rowcount > 0:
            whitelist_OUIs_data = cursor.fetchall()
            print "\nWhitelisted OUIs (Tagged Parameters):"
            print "(BSSID - SSID - OUI)\n"
            for row in whitelist_OUIs_data:
                print "({} - {} - {})".format(row[0],row[1],row[2])
        else:
            print "\nCurrently, There are No Whitelisted OUIs\n"

    except:
        print ""

# Get MonInterface
def get_moniface():
    mons, ifaces = cmd_iwconfig()

    if len(mons) > 0:
        return mons[0]
    else:
        return 0

def cmd_iwconfig():
    mons = []
    ifaces = {}
    iwconf = Popen(['iwconfig'], stdout=PIPE)
    for line in iwconf.communicate()[0].split('\n'):
        if len(line) == 0: continue
        if line[0] != ' ':
            wired_search = re.search('eth[0-9]|em[0-9]|p[1-9]p[1-9]', line)
            if not wired_search:
                iface = line[:line.find(' ')]
                if 'Mode:Monitor' in line:
                    mons.append(iface)
                elif 'IEEE 802.11' in line:
                    if "ESSID:\"" in line:
                        ifaces[iface] = 1
                    else:
                        ifaces[iface] = 0
    return mons, ifaces

# Deauth Attack
def Deauth(Dbssid,Dssid,Dchannel,Dtime):
    try:
        print "Attacking Dbssid: {} - Dssid: {} - Dchannel: {} - Dtime: {}\n".format(Dbssid,Dssid,Dchannel,Dtime)
        print "\nChanging monitor interface into channel [{}]\n".format(Dchannel)
        Reset("INTF")
        airmon_out = Popen(["airmon-ng", "start", wireless_interface, Dchannel], stdout=PIPE).communicate()[0]
        mon_iface = get_moniface()
        print "\nAttack time set to: {} Seconds\n".format(Dtime)
        aireplay = Popen(["aireplay-ng", "--deauth", "0",  "-a", Dbssid, "-e", Dssid, mon_iface])
        time.sleep(Dtime)
        aireplay.terminate()
    except Exception,e:
        print "Unexpected error in 'Deauth': {}\n".format(sys.exc_info()[0]) + str(e)

#Initialize options
def Initialize_options():
    try:
        cmd = "select opt_val from options where opt_key = 'deauth_time'"
        cursor.execute(cmd)
        if cursor.rowcount <= 0:
            cmd = "insert into options values('deauth_time','0')"
            cursor.execute(cmd)
        cmd = "select opt_val from options where opt_key = 'deauth_repeat'"
        cursor.execute(cmd)
        if cursor.rowcount <= 0:
            cmd = "insert into options values('deauth_repeat','1')"
            cursor.execute(cmd)
    except:
        print "Unexpected error in 'Initialize_options': {}\n".format(sys.exc_info()[0])

# Tagged Parameters parsing
def insert_ap(pkt):
    try:
        bssid = pkt[Dot11].addr3
        if bssid in aps:
            return
        p = pkt[Dot11Elt]
        cap = pkt.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}"
                          "{Dot11ProbeResp:%Dot11ProbeResp.cap%}").split('+')

        ssid, OUI = None, None
        OUIs = []

        while isinstance(p, Dot11Elt):
            if p.ID == 0:
                ssid = p.info

            if p.ID == 221:
                s = p.info.encode("hex")
                OUI = s[:6]
                if OUI not in OUIs:
                    OUIs.append(OUI)

            p = p.payload

        for item in OUIs:
            cmd = "insert into ssids_OUIs (mac, ssid, oui) values(%s,%s,%s)"
            cursor.execute(cmd, (bssid, ssid, item))

        aps[bssid] = (ssid)
    except:
        print "Unexpected error in 'insert_ap': {}\n".format(sys.exc_info()[0])

# Check for Evil APs
def CheckEvilAP():
    EvilAPMAC = False
    EvilAPAttrib = False
    EvilAPOUI = False
    try:
        ########### Check for no SSIDs detected
        cmd = "select * from ssids where ssid in (select ssid from whitelist)"
        cursor.execute(cmd)
        if cursor.rowcount > 0:

        ########### Check rogue AP with same SSID and different MAC
            cmd = "select * from ssids as s where s.ssid in (select ssid from whitelist) and s.mac not in (select w.mac from whitelist as w where s.ssid = w.ssid)"
            cursor.execute(cmd)
            if cursor.rowcount > 0:
                Evil_data = cursor.fetchall()
                EvilAPMAC = True

        ########### Check rogue AP with same SSID and MAC and different other attribute (such as: channel, Auth, Enc, Cipher)
            cmd = "select distinct * from ssids as s inner join whitelist as w on s.ssid = w.ssid and s.mac = w.mac where s.channel != w.channel \
                          or s.CIPHER != w.CIPHER or s.Enc != w.Enc or s.Auth != w.Auth"
            cursor.execute(cmd)
            if cursor.rowcount > 0:
                attrib_data = cursor.fetchall()
                EvilAPAttrib = True

        ########### Check for rouge AP with different OUIs
            cmd = "select distinct * from whitelist_OUIs as wo where wo.oui not in (select so.oui from ssids_OUIs as so where so.mac = wo.mac) \
                and wo.mac in (select w.mac from whitelist as w inner join ssids as s on w.ssid = s.ssid)"
            cursor.execute(cmd)
            if cursor.rowcount > 0:
                OUIs_data = cursor.fetchall()
                EvilAPOUI = True
            else:
                cmd = "select distinct * from ssids_OUIs as so where so.oui not in (select wo.oui from whitelist_OUIs as wo where wo.mac = so.mac) \
                    and so.mac in (select w.mac from whitelist as w inner join ssids as s on w.ssid = s.ssid)"
                cursor.execute(cmd)
                if cursor.rowcount > 0:
                    OUIs_data = cursor.fetchall()
                    EvilAPOUI = True

        ########### Print the Result
            print "\n###########################CHECK-RESULT########################\n"
            if EvilAPMAC:
                file = open("/root/eapd.log","a")
                file.write("Fake AP with different MAC Detected!\n")
                file.close()
                file = open("/tmp/fail","a")
                file.write("Yes")
                file.close()
                print "Fake AP with different MAC Detected!\n"
                msg = "Fake AP with different MAC Detected!\n"
                msg = msg + "(BSSID - SSID - PWR - Channel - Cipher - Privacy - Auth)\n"
                print "(BSSID - SSID - PWR - Channel - Cipher - Privacy - Auth)"
                for row in Evil_data:
                    print "({} - {} - '{}' - {} - {} - {} - {})\n".format(row[1],row[2],row[3],row[4],row[5],row[6],row[7])
                    msg = msg + "({} - {} - '{}' - {} - {} - {} - {})\n".format(row[1],row[2],row[3],row[4],row[5],row[6],row[7])
                thread = threading.Thread(target=AlertAdmin, args=(msg,))
                thread.start()
                cmd = "select opt_val from options where opt_key = 'deauth_time'"
                cursor.execute(cmd)
                if cursor.rowcount > 0:
                    row = cursor.fetchone()
                    deauth_time = int(row[0])
                    print "Deauth time: {}".format(deauth_time)
                    if int(deauth_time) > 0:
                        file = open("/root/eapd.log","a")
                        file.write("Attacking Evil Access Point.\n")
                        file.close()
                        print "\n#########################ATTACK-MODE###########################\n"
                        print "Attacking Evil Access Point..."
                        cmd = "select opt_val from options where opt_key = 'deauth_repeat'"
                        cursor.execute(cmd)
                        if cursor.rowcount > 0:
                            raw_value = cursor.fetchone()
                            deauth_repeat = int(raw_value[0])
                            if deauth_repeat <= 0:
                                deauth_repeat = 1
                            for i in range(deauth_repeat):
                                if len(Evil_data) == 1:
                                    for row in Evil_data:
                                        Deauth(row[1],row[2],str(row[4]),deauth_time*deauth_repeat)
                                    break
                                else:
                                    for row in Evil_data:
                                        Deauth(row[1],row[2],str(row[4]),deauth_time)
                        print "\nStop attacking Evil Access Point...\n\n"
                    else:
                        print "Preventive Mode is not enabled\n"

            elif EvilAPAttrib:
                file = open("/root/eapd.log","a")
                file.write("Fake AP with different Attribute Detected!\n")
                file.close()
                file = open("/tmp/fail","a")
                file.write("Yes")
                file.close()
                print "Fake AP with different Attribute Detected!\n"
                msg = msg + "(BSSID - SSID - PWR - Channel - Cipher - Privacy - Auth)\n"
                print "(BSSID - SSID - PWR - Channel - Cipher - Privacy - Auth)"
                for row in attrib_data:
                    print "({} - {} - '{}' - {} - {} - {} - {})\n".format(row[1],row[2],row[3],row[4],row[5],row[6],row[7])
                    msg = msg + "({} - {} - '{}' - {} - {} - {} - {})\n".format(row[1],row[2],row[3],row[4],row[5],row[6],row[7])
                thread = threading.Thread(target=AlertAdmin, args=(msg,))
                thread.start()
                cmd = "select distinct * from ssids as s inner join whitelist as w on s.ssid = w.ssid and s.mac = w.mac where s.channel != w.channel"
                cursor.execute(cmd)
                if cursor.rowcount > 0:
                    cmd = "select opt_val from options where opt_key = 'deauth_time'"
                    cursor.execute(cmd)
                    if cursor.rowcount > 0:
                        row = cursor.fetchone()
                        deauth_time = int(row[0])
                        print "Deauth time: {}".format(deauth_time)
                        if int(deauth_time) > 0:
                            file = open("/root/eapd.log","a")
                            file.write("Attacking Evil Access Point.\n")
                            file.close()
                            print "\n#########################ATTACK-MODE###########################\n"
                            print "Attacking Evil Access Point..."
                            cmd = "select opt_val from options where opt_key = 'deauth_repeat'"
                            cursor.execute(cmd)
                            if cursor.rowcount > 0:
                                raw_value = cursor.fetchone()
                                deauth_repeat = int(raw_value[0])
                                if deauth_repeat <= 0:
                                    deauth_repeat = 1
                                for i in range(deauth_repeat):
                                    if len(attrib_data) == 1:
                                        for row in attrib_data:
                                            Deauth(row[1],row[2],str(row[4]),deauth_time*deauth_repeat)
                                        break
                                    else:
                                        for row in attrib_data:
                                            Deauth(row[1],row[2],str(row[4]),deauth_time)
                            print "\nStop attacking Evil Access Point...\n\n"
                        else:
                            print "Preventive Mode is not enabled\n"

            elif EvilAPOUI:
                file = open("/root/eapd.log","a")
                file.write("Fake AP with different OUI Detected!\n")
                file.close()
                file = open("/tmp/fail","a")
                file.write("Yes")
                file.close()
                print "Fake AP with different OUI Detected!\n"
                msg = "Fake AP with different OUI Detected!\n"
                msg = msg + "(BSSID - SSID - OUI)\n"
                print "(BSSID - SSID - OUI)"
                for row in OUIs_data:
                    print "({} - {} - {})\n".format(row[0],row[1],row[2])
                    msg = msg + "({} - {} - {})\n".format(row[0],row[1],row[2])
                thread = threading.Thread(target=AlertAdmin, args=(msg,))
                thread.start()
                #AlertAdmin(msg)
            else:
                file = open("/root/eapd.log","a")
                file.write("No Evil AP Detected!\n")
                file.close()
                print "No Evil AP Detected!\n"
            print "\n###############################################################\n"

        else:
            file = open("/root/eapd.log","a")
            file.write("No Whitelisted SSID Detected!\n")
            file.close()
            print "No Whitelisted SSID Detected!"
            print "Run Learning Mode first and add your SSID into the whitelist.\n"
    except:
        print "Unexpected error in 'CheckEvilAP': {}\n".format(sys.exc_info()[0])

# Parsing the output
def ParseAirodumpCSV():
    try:
        f = open('out.csv-01.csv', 'rb') # opens the csv file
        try:
            reader = csv.reader(x.replace('\0', '') for x in f)  # creates the reader object
            for row in reader:   # iterates the rows of the file in orders
                if 'BSSID' in row:
                    continue
                if 'Station MAC' in row:
                    continue
                if len(row) < 1:
                    continue
                cmd = "insert into ssids (mac,ssid,pwr,channel,CIPHER,Enc,Auth) values(%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(cmd, (row[0].strip(), row[13].strip(), row[8].strip(), row[3].strip(), row[6].strip(), row[5].strip(), row[7].strip()))
            db_connection.commit()

        finally:
            f.close()
    except:
        print ""

# Release resources
def Reset(Ropt):
    try:
        time.sleep(1)
        if Ropt == "INTF":
            os.system('airmon-ng stop ' + mon_iface)
            os.system('ifconfig ' + wireless_interface + ' down')
            os.system('ifconfig ' + wireless_interface + ' up')
        elif Ropt == "DB":
            cursor.close()
            db_connection.close()
        else:
            os.system('rm *.csv')
            os.system('airmon-ng stop ' + mon_iface)
            os.system('ifconfig ' + wireless_interface + ' down')
            os.system('ifconfig ' + wireless_interface + ' up')
            cursor.close()
            db_connection.close()
    except:
        print "Unexpected error in 'Reset': {}\n".format(sys.exc_info()[0])

def LearningMode():
    # here is Learning stuff
    try:
        while True:
            Conf_viewSSIDs()
            Choices()
            choice = raw_input('Enter the number for your choice: ')
            if choice == "1":
                print "\n######################AUTO-CONFIG-MODE#########################\n"
                SSID = raw_input('Enter the SSID name you want to whitelist: ')
                cmd = "select * from ssids where ssid=%s"
                cursor.execute(cmd, (SSID,))
                if cursor.rowcount > 0:
                    cmd = "delete from whitelist where ssid=%s"
                    cursor.execute(cmd, (SSID,))
                    cmd = "delete from whitelist_OUIs where ssid=%s"
                    cursor.execute(cmd, (SSID,))
                    cmd = "insert into whitelist(mac,ssid,min_pwr,max_pwr,channel,CIPHER,Enc,Auth) select mac,ssid,pwr-10,pwr+10,channel,CIPHER,Enc,Auth \
                    from ssids where ssid = %s"
                    cursor.execute(cmd, (SSID,))
                    cmd = "insert into whitelist_OUIs select * from ssids_OUIs where ssid=%s"
                    cursor.execute(cmd, (SSID,))
                    db_connection.commit()
                    print "The SSID and all its Access Points have been whitelisted!"
                    time.sleep(1)
                else:
                    print "The SSID you entered cannot be found among the discovered SSIDs"
            elif choice == "2":
                new_bssid = raw_input('Enter the BSSID you want to whitelist: ')
                cmd = "select * from ssids where mac=%s"
                cursor.execute(cmd, (new_bssid,))
                if cursor.rowcount > 0:
                    cmd = "delete from whitelist where mac=%s"
                    cursor.execute(cmd, (new_bssid,))
                    cmd = "delete from whitelist_OUIs where mac=%s"
                    cursor.execute(cmd, (new_bssid,))
                    cmd = "insert into whitelist(mac,ssid,min_pwr,max_pwr,channel,CIPHER,Enc,Auth) select mac,ssid,pwr-10,pwr+10,channel,CIPHER,Enc,Auth \
                    from ssids where mac = %s"
                    cursor.execute(cmd, (new_bssid,))
                    cmd = "insert into whitelist_OUIs select * from ssids_OUIs where mac=%s"
                    cursor.execute(cmd, (new_bssid,))
                    db_connection.commit()
                    print "The identified Access Point has been whitelisted!"
                    time.sleep(1)
                else:
                    print "The BSSID you entered cannot be found among the discovered BSSIDs"
            elif choice == "3":
                bssid_rm = raw_input('Enter the BSSID you want to remove from whitelist: ')
                cmd = "select * from whitelist where mac=%s"
                cursor.execute(cmd, (bssid_rm,))
                if cursor.rowcount > 0:
                    bssid_rm_confirm = raw_input('This will remove the identified BSSID from whitelist! Are you still want to continue?(y/n): ')
                    if bssid_rm_confirm == "y":
                        cmd = "delete from whitelist where mac=%s"
                        cursor.execute(cmd, (bssid_rm,))
                        cmd = "delete from whitelist_OUIs where mac=%s"
                        cursor.execute(cmd, (bssid_rm,))
                        db_connection.commit()
                        print "The identified Access Point has been removed from the whitelist!"
                    else:
                        print "No BSSID has been removed!"
                else:
                    print "The BSSID you entered cannot be found among the whitelisted BSSIDs"
            elif choice == "4":
                confirm = raw_input('This will remove all whitelisted SSIDs! Are you still want to continue?(y/n): ')
                if confirm == "y":
                    cmd = "delete from whitelist"
                    cursor.execute(cmd)
                    cmd = "delete from whitelist_OUIs"
                    cursor.execute(cmd)
                    db_connection.commit()
                    print "All whitelisted SSIDs have been removed!"
                else:
                    print "No SSID has been removed!"
                time.sleep(1)
            elif choice == "5":
                while True:
                    cmd = "select * from options"
                    cursor.execute(cmd)
                    print "\n###############################################################\n"
                    print "Current options:"
                    if cursor.rowcount > 0:
                        options_data = cursor.fetchall()
                        print "(Key, Value)\n"
                        for row in options_data:
                            if row[0] == "admin_smtp_password":
                                print "({}, ************)".format(row[0])
                            else:
                                print "({}, {})".format(row[0], row[1])
                        print "\n"

                    Options()
                    option = raw_input('Enter the number for your choice: ')
                    if option == "1":
                        deauth_time = int(raw_input('Enter Deauth attack time (attack duration in seconds. To disable enter 0): '))
                        cmd = "delete from options where opt_key = 'deauth_time'"
                        cursor.execute(cmd)
                        cmd = "insert into options values('deauth_time',%s)"
                        cursor.execute(cmd, (deauth_time,))
                        deauth_repeat = int(raw_input('How many times do you want to repeat Deauth attack (minimum 1): '))
                        cmd = "delete from options where opt_key = 'deauth_repeat'"
                        cursor.execute(cmd)
                        cmd = "insert into options values('deauth_repeat',%s)"
                        cursor.execute(cmd, (deauth_repeat,))
                        db_connection.commit()
                    elif option == "2":
                        admin_email = raw_input('Enter admin email: ')
                        cmd = "delete from options where opt_key = 'admin_email'"
                        cursor.execute(cmd)
                        cmd = "insert into options values('admin_email',%s)"
                        cursor.execute(cmd, (admin_email,))
                        admin_smtp = raw_input('Enter SMTP address or IP: ')
                        cmd = "delete from options where opt_key = 'admin_smtp'"
                        cursor.execute(cmd)
                        cmd = "insert into options values('admin_smtp',%s)"
                        cursor.execute(cmd, (admin_smtp,))
                        admin_smtp_username = raw_input('Enter SMTP username for authentication (complete email): ')
                        cmd = "delete from options where opt_key = 'admin_smtp_username'"
                        cursor.execute(cmd)
                        cmd = "insert into options values('admin_smtp_username',%s)"
                        cursor.execute(cmd, (admin_smtp_username,))
                        admin_smtp_password = raw_input('Enter SMTP password for authentication: ')
                        cmd = "delete from options where opt_key = 'admin_smtp_password'"
                        cursor.execute(cmd)
                        cmd = "insert into options values('admin_smtp_password',%s)"
                        cursor.execute(cmd, (admin_smtp_password,))
                        db_connection.commit()
                    else:
                        break

            elif choice == "6":
                print "Entering Normal Mode...\n"
                CheckEvilAP()
                break
            elif choice == "7":
                print "Exiting the application..." 
                print "Please wait...\n"
                break
            else:
                print "Wrong choice! Please use one of the avilable choices.\n"
    except:
        print "Unexpected error in 'LearningMode': {}".format(sys.exc_info()[0])

##################################################################### Main Start Here

Mode = ""
username = ""
password = ""
interface = ""
frequency = ""

try:
    opts, args = getopt.getopt(sys.argv[1:], "hLNu:p:i:f:", ["help"])
except getopt.GetoptError:
    Usage()
except:
        print "Unexpected error while parsing arguments: {}".format(sys.exc_info()[0])
for opt, arg in opts:
    if opt in ("-h", "--help"):
        Help()
    if opt == "-N":
        Mode = "Normal"
    if opt == "-L":
        Mode = "Learning"
    if opt == "-u":
        username = arg
    if opt == "-p":
        password = arg
    if opt == "-i":
        interface = arg
    if opt == "-f":
        frequency = arg

if Mode == "":
    Usage()

########### MySQL Database setup and preparation
print "Preparing MySQL Database\n"

try:
    try:
        db_connection = MySQLdb.connect(host='127.0.0.1', user='root', passwd=password)
        print "Connected to MySQL\n"
    except:
        print "Make sure MySQL server is running\n"
        sys.exit(2)

    cursor = db_connection.cursor()

    cmd = "show databases like 'EvilAPDef'"
    cursor.execute(cmd)
    if cursor.rowcount <= 0:
      cmd = 'CREATE DATABASE IF NOT EXISTS EvilAPDef'
      cursor.execute(cmd)

    cmd = 'USE EvilAPDef'
    cursor.execute(cmd)

    cmd = "show tables like 'ssids'"
    cursor.execute(cmd)
    if cursor.rowcount <= 0:
        cmd = '''CREATE TABLE IF NOT EXISTS ssids (
            id MEDIUMINT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id), mac TEXT, ssid TEXT, pwr INTEGER, channel NUMERIC, CIPHER TEXT, Enc TEXT, Auth TEXT)
                  '''
        cursor.execute(cmd)

    cmd = "show tables like 'whitelist'"
    cursor.execute(cmd)
    if cursor.rowcount <= 0:
        cmd = '''CREATE TABLE IF NOT EXISTS whitelist (
            id MEDIUMINT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id), mac TEXT, ssid TEXT, min_pwr INTEGER, max_pwr INTEGER, channel NUMERIC, CIPHER TEXT, Enc TEXT, Auth TEXT)
                  '''
        cursor.execute(cmd)

    cmd = "show tables like 'ssids_OUIs'"
    cursor.execute(cmd)
    if cursor.rowcount <= 0:
        cmd = '''CREATE TABLE IF NOT EXISTS ssids_OUIs (
            mac TEXT, ssid TEXT, oui TEXT)
                  '''
        cursor.execute(cmd)

    cmd = "show tables like 'whitelist_OUIs'"
    cursor.execute(cmd)
    if cursor.rowcount <= 0:
        cmd = '''CREATE TABLE IF NOT EXISTS whitelist_OUIs (
            mac TEXT, ssid TEXT, oui TEXT)
                  '''
        cursor.execute(cmd)

    cmd = "show tables like 'options'"
    cursor.execute(cmd)
    if cursor.rowcount <= 0:
        cmd = '''CREATE TABLE IF NOT EXISTS options (
            opt_key varchar(255), opt_val varchar(255))
                  '''
        cursor.execute(cmd)

    cmd = 'Truncate table ssids'
    cursor.execute(cmd)
    cmd = 'Truncate table ssids_OUIs'
    cursor.execute(cmd)
except:
        print "Unexpected error during intializing MySQL: {}\n".format(sys.exc_info()[0])
        sys.exit(2)

Initialize_options()

########### Preparing Monitor Interface
try:
    output = Popen("iwconfig", stdout=PIPE).communicate()[0]
    wireless_interface = ""
    mon_iface = ""
    if "wlan" in output:
        wireless_interface = interface
        file = open("/root/eapd.log","a")
        file.write("Using " + wireless_interface + ".\n")
        file.close()
    else:
        print "\n\nCould not find the wireless interface!"
        print "Exiting the application...\n"
        print "Please wait...\n"
        file = open("/root/eapd.log","a")
        file.write("Couldn't find the wireless interface, Error!.\n")
        file.close()
        Reset("DB")
        sys.exit(2)

    # Check if mon interface is not disabled
    airmon_data = Popen("airmon-ng", stdout=PIPE).communicate()[0]
    if 'mon' in airmon_data:
        print "Found existing monitor."
except:
        print ""

# Creating Monitor Interface
try:
        print "Restarting wireless interface: " + wireless_interface + "\n"
        os.system('ifconfig ' + wireless_interface + ' down')
        os.system('ifconfig ' + wireless_interface + ' up')
        print "Using wireless interface: " + wireless_interface + "\n"
        print "Creating a monitoring interface\n"
        airmon_out = Popen(["airmon-ng", "start", wireless_interface], stdout=PIPE).communicate()[0]
        mon_iface = get_moniface()
        if mon_iface != 0:
                print "Monitor interface {} created successfully.\n".format(mon_iface)
        else:
                print "Monitor interface cannot be created. Make sure your card support monitor mode and Aircrack-ng suite.\n"
except:
        print "Unexpected error during Creating Monitor Interface: {}\n".format(sys.exc_info()[0])
########### Remove the old output from airodump
try:
        os.system('rm *.csv')
except:
        print ""

# Scanning for available SSIDs
file = open("/root/eapd.log","a")
file.write("Scanning for wireless networks.\n")
file.close()
print "\n###############################################################\n"
print "SCANNING FOR WIRELESS NETWORKS\n"
try:
    if frequency == "2":
        airodump = Popen(["airodump-ng", "--output-format", "csv",  "-w", "out.csv", mon_iface])
    elif frequency == "5":
        airodump = Popen(["airodump-ng", "--output-format", "csv",  "-w", "out.csv", "--channel", "1,2,3,4,5,6,7,8,9,10,11,36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165", mon_iface])
    else:
        airodump = Popen(["airodump-ng", "--output-format", "csv",  "-w", "out.csv", mon_iface])
    
    aps = {}
    time.sleep(120)
    airodump.terminate()
    db_connection.commit()
except:
        print ""
ParseAirodumpCSV()

if Mode == "Normal":
    print "Entering Scanning Mode...\n"
    CheckEvilAP()
elif Mode == "Learning":
    print "Entering Learning Mode...\n"
    LearningMode()
else:
    print("Mode is not identified, Please use the suitable option to run the tool or use '%s' with no options for help menu." % sys.argv[0])

Reset("All")
