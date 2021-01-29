#Python: Parse_device_list.py

"""
This program takes device index, location name as inputs and parses the pre populated list for any devices with these matches.Matched records will be printed.

Created on January 29, 2021
Author: xxxx
"""

import sys
import re

devices = {'ssw001.altn','ssw002.altn','ssw003.altn','efw001.altn','efw002.altn','ssw001.llan','ssw002.llan','ssw003.llan','efw002.llan'}

device_index =""
device_loc = ""
matched_device_list =[]

#This function gathers device name and location name from the cmd line args
def gather_dev_loc():
    global device_index
    global device_loc
    num_of_args = len(sys.argv)
    if num_of_args == 3:
        device_index = sys.argv[1]    
        device_loc = sys.argv[2]
    else:
        print("Invalid number of arguments, please rerun program with the correct option\n Usage: python3 Parse_device_list.py <device_index> <device_location>\n ")
        sys.exit()
    

#This function parses the list to check any records with device name and location requested
def parse_dev_list():
    global device_index
    global device_loc
    global devices
    pattern = '^' + device_index + '....' + device_loc + '$'
    for index in devices:
        if re.match(pattern, index, re.IGNORECASE):
            matched_device_list.append(index)
    return(matched_device_list)


#This function prints the number and list of matching devices with the pattern
def print_report(matched_device_list):
    print("There are %s matching devices in the list" % len(matched_device_list))
    print('\n'.join(matched_device_list))



#The program execution starts here
gather_dev_loc()    
matched_device_list = parse_dev_list()
print_report(matched_device_list)
