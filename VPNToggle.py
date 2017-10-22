#!/usr/bin/env python3.5

'''Simple script to toggle the state of Nord VPN connection.
This script is designed to work with the default nord vpn connection names.
This script should work with any other VPN connections with minor modification
to line 71 and 72 - follow comments on said lines. This script relies on output
from nmcli commandline utility.

If a VPN is in use this script will turn it off.
Like wise if a VPN is not active it will turn one on.
This script is designed to be called by a keyboard shortcut
key.
Usage:
    Create new keyboard custom shortcut
    set command to run:
        /home/user/path/to/this/script
    Asign accelorator key to desired key'''

import random
import subprocess

def make_dict_of_connections(con_list):
    ''' takes a list of strings containing name of connection
    and type seperated by : eg  ["name:type",] and returns a dictionary
    where key is connnection type and value is a list of connection names
    matching that type. eg {"vpn": ["one.com", "two.com"]}'''

    connections_dict = {}
    for i in con_list:
        connection = i.split(':')
        try:
            if connection[0] not in connections_dict:
                connections_dict[connection[0]] = [connection[1]]
            else:
                connections_dict[connection[0]].append(connection[1])
        except IndexError:
            # Ignore blank lines produced by nmcli
            continue
    return connections_dict

def main():
    '''Toggle a VPN connection from active to inactive, or vise versa.
    Detect is a VPN is in use, if so disconnect from the VPN.
    If a VPN is not in use gather a list of VPN connections, filter for UK only,
    and connect to a random one.'''
    available_vpns = subprocess.run(['nmcli',
                                     '-t',
                                     '-f',
                                     'TYPE,NAME',
                                     'con'], stdout=subprocess.PIPE)

    vpn_list = available_vpns.stdout.decode('UTF-8').split('\n')
    vpn_dict = make_dict_of_connections(vpn_list)  # {"vpn": [vpn,names]}

    active_devices = subprocess.run(['nmcli',
                                     '-t',
                                     '-f',
                                     'TYPE,NAME',
                                     'con',
                                     'show',
                                     '--active'], stdout=subprocess.PIPE)

    if 'vpn' in active_devices.stdout.decode('UTF-8'):  # check if vpn is active
        con_list = active_devices.stdout.decode('UTF-8').split('\n')
        con_dict = make_dict_of_connections(con_list)
        active_vpn = con_dict['vpn'][0]
        subprocess.run(['nmcli', 'con', 'down', 'id', active_vpn])
    else:
        new_vpns = vpn_dict['vpn']
        #sublist uk vpns
        uk_vpns = [i for i in new_vpns if i.startswith('uk')]  # comment this out
        random_uk_vpn = random.choice(uk_vpns)  # replace uk_vpns with new_vpns
        subprocess.run(['nmcli', 'con', 'up', 'id', random_uk_vpn])

if __name__ == "__main__":
    main()
