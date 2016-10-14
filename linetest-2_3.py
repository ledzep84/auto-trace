#!/usr/bin/env python
import subprocess
import re

#####################################################################################
#       Script to automate an MTR if packet loss or latency is detected             #
#       1. Change Variables input to suit your needs.                               #
#       2. To automate, set an entry in /etc/crontab file.                          #
#               eg.,*/3  *      * * *   root    /root/Scripts/drafts/linetest.py    #
#       3. If packet loss or latency is detected, script will generate an           #
#       MTR result in /root/mtr_result.txt.                                         #
#       4. Requirements python, linux, root privilege, MTR                          #
#       5. For bugs and question send a holler.                                     #
#	6. Script will not check for incorrect variables like IP address, etc.	    #
#  								  		    #	
#			https://github.com/ledzep84				    #
#####################################################################################


#####CHANGE INPUT VARIABLES#####

#BASELINE LATENCY
latency_base = 50

#PACKET LOSS BASELINE, 0% IS GOOD CHOICE
packetloss_base = 0

#TARGET IP ADDRESS
target_ip = “8.8.8.8”

#ENTER 1 FOR LATENCY TEST OR 2 FOR PACKET LOSS TEST
testoption = "2"

######END INPUT VARIABLES#######




######################DO NOT MODIFY BELOW THIS######################

#RECORD MTR RESULT
def mtr_test(ipadd_mtr):
	mtr_proc = subprocess.Popen(["mtr","-t","-c50","-r","-n",ipadd_mtr], stdout=subprocess.PIPE)
	mtr_result,err = mtr_proc.communicate()

	file = open("mtr_result.txt","a")
	file.write(mtr_result)
	file.close
	return

#LATENCY BASE TEST
def latency_test(ipadd_lat, latency_base_val_check):
	ping_proc = subprocess.Popen(["ping","-c20",ipadd_lat], stdout=subprocess.PIPE)
	ping_result,err = ping_proc.communicate()

	ping_result_print = re.findall(r"[0-9]{1,3}\D+[0-9]{1,3}[/]+", ping_result, re.DOTALL)
	lat_avg = list(ping_result_print)
	lat_avg_print = lat_avg[2].strip("/")

	if float(lat_avg_print) > float(latency_base_val_check):
		mtr_test(ipadd_lat)
	else:
		return

#PACKET LOSS BASE TEST
def packetloss_test(ipadd_pktloss, packetloss_base_val_check):
	ping_proc = subprocess.Popen(["ping","-c10",ipadd_pktloss], stdout=subprocess.PIPE)
        ping_result,err = ping_proc.communicate()

	ping_result_print = re.search(r"(\d+)[%]+ +([a-z]{6} +[a-z]{4})", ping_result, re.DOTALL)
	result = int(ping_result_print.group(1))

	if result != packetloss_base_val_check:
		mtr_test(ipadd_pktloss)
	else:
		return

#LATENCY OR PACKET LOSS OPTION
def latency_packet(testoption_choice, ipaddress, latency_base_val, packetloss_base_val):
	if testoption_choice == "1":
		latency_test(ipaddress, latency_base_val)
	else:
		packetloss_test(ipaddress, packetloss_base_val)


latency_packet(testoption,target_ip,latency_base,packetloss_base)
