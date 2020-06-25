#!/usr/bin/env python

#Import subprocess, this will execute system commands
import subprocess
#import optparse (it is used to collect options from user such as in command line when user adds -t)
import optparse
#Import re, this is used to regular expressions or patterns
import re

#This function will call the commands and store the values in variables called interface and new_mac
#Using list with the command, for security purposes
def change_mac(interface, new_mac):
    print("[+] Changing MAC Address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

#This function will be used to get user options from cmd and storing them in a variable called parser
#dest is the variable where the options will be stored in
#help is the help (--help) created for more info, if function for errors
def cmd_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface", dest="interface_cmd", help="Interface to change its MAC address")
    parser.add_option("-m","--mac", dest="new_mac_cmd", help="New MAC")
    (option, arguments) = parser.parse_args()
    if not option.interface_cmd:
        parser.error("[-] PLease Specify an Interface")
    elif not option.new_mac_cmd:
        parser.error("[-] PLease Choose a new MAC")
    return option

#This function will use subprocess to check the output and store them in a variable called ifconfig_result
#re.search will use a pattern to print only this specified pattern from the cmd (pattern created using Pythex)
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result  = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
            return mac_address_search_result.group(0)
    else:
            print("[-] Could Not Read MAC. ")



option = cmd_arguments()
current_mac = get_current_mac(option.interface_cmd)
print("Current MAC = " + str(current_mac))
change_mac(option.interface_cmd, option.new_mac_cmd)
current_mac = get_current_mac(option.interface_cmd)
if current_mac == option.new_mac_cmd:
    print ("[+] MAC Address was changed successfully to " + current_mac)
else:
    print("[-] MAC address did not get changed.")