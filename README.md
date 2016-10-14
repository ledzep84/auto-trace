1. Change Variables input to suit your needs.<br>
2. To automate, set an entry in /etc/crontab file.<br>
  eg.,*/3  *      * * *   root    /root/Scripts/drafts/auto-trace.py<br>
3. If packet loss or latency is detected, script will generate an MTR result in /root/mtr_result.txt.<br>                                      #
4. Requirements python, linux, root privilege, MTR<br>
5. For bugs and question send a holler.<br>
6. Script will not check for incorrect variables like IP address, etc.<br>
https://github.com/ledzep84
