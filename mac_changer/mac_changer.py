#!/usr/bin/env python

from hashlib import new
import subprocess
from tokenize import String
from sqlalchemy import true
from tempita import sub 
import optparse
from yaml import parse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface", dest="interface",help="Interface to change MAC address")
    parser.add_option("-m","--mac",dest="new_mac",help="New Mac Address")
    (options, arguememts) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify the interface, use --help for help")
    elif not options.new_mac:
        parser.error("[-] Please specify the Mac Address, use --help for help")
    else :
        return options


def change_mac(interface, new_mac):
    print("[+] Changing Mac address of interface " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(b'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result)
    if mac_address_search_result:
        mac_res = str(mac_address_search_result.group(0)) 
        mac_res = mac_res[3:-1]
        return mac_res
    else:
        print("[-] could not read Mac address")

options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current Mac = " + str(current_mac))
change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] Mac was successfully changed " + current_mac)
else:
    print("[-] Mac was not changed")

    
# interface = input("Enter the interface > ")
# new_mac = input("Enter the new MAC Address > ")

# subprocess.call("ifconfig " + interface + " down",shell=true)
# subprocess.call("ifconfig " + interface + " hw ether " + new_mac,shell=true)
# subprocess.call("ifconfig " + interface + " up",shell=true)



