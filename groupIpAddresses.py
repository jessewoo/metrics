import ipaddress
import os

def group_ips(ip_list):
    """Groups a list of IP addresses by network."""
    groups = {}
    for ip_str in ip_list:
        try:
            ip_address = ipaddress.ip_address(ip_str)
            network = ipaddress.ip_network(f"{ip_str}/24", strict=False)
            if network not in groups:
                groups[network] = []
            groups[network].append(ip_address)
        except ValueError:
            print(f"Invalid IP address: {ip_str}")
    return groups

script_dir = os.path.dirname(__file__)
blackListIp = script_dir + '/blacklistSorted.txt'

ip_addresses = []
with open(blackListIp, 'r') as file:
  # Read all lines into a list
  lines = file.readlines()
  ip_addresses = [line.strip() for line in lines]

file = open("ipaddressNetwork.txt", "w")

grouped_ips = group_ips(ip_addresses)

for network, ips in grouped_ips.items():
    print(f"Network: {network}")
    file.write(str(network).replace("0/24", "") + '\n')

    for ip in ips:
        print(f"  - {ip}")

file.close()