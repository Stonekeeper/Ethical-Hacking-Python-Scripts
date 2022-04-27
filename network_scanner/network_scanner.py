from http import client
from tabnanny import verbose
from click import option
import scapy.all as scapy
import argparse

def get_arguements():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--target",dest="target",help="Target IP/ IP range")
    options = parser.parse_args()
    return options
    
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list, unanswered_list = scapy.srp(arp_request_broadcast,verbose = False, timeout = 1)
    
    clients_list = []
    for i in answered_list:
        client_dict = {"ip" : i[1].psrc, "mac" : i[1].hwsrc}
        clients_list.append(client_dict)

    return clients_list

def print_result(results_list):
    print("IP\t\t\tMAC Address\n-----------------------------------------")
    for i in results_list:
        print(i["ip"]+"\t\t"+i["mac"])

options = get_arguements()
scan_result = scan(options.target)
print_result(scan_result)