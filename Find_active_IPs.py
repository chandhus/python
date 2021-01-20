# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 00:12:09 2020
@author: Chandhu
"""

import subprocess
import sys
import threading
import datetime


start_time = datetime.datetime.now()
my_ip = "143.168.0.103"
network_addr = "143.168.0."
usable_range = 120
start_index = 100

num_of_threads = 1
active_ip_list = []
total_time = ""


def concurrency_threads():
    global num_of_threads
    num_of_args = len(sys.argv)
    if num_of_args == 2:
        num_of_threads = int(sys.argv[1])    
    elif num_of_args > 2:
        print("Invalid number of arguments, please rerun program with the correct option")
        sys.exit()


def capture_ips():
    cmd = "netsh interface ip show address | findstr IP"
    all_ips_output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    all_host_ips = str(all_ips_output.communicate()[0])
    return(all_host_ips)


def check_valid_ip(my_ip, all_host_ips):
    if my_ip not in all_host_ips:
        print("\n%s is not assigned to this host, Please rerun the program opting the correct IP!" % my_ip)
        sys.exit()
    print("\n%s is a matched IP Address!" % my_ip)

   
def check_active_ip(offset):
    host_index = start_index + offset
    
    while host_index <= usable_range:
        addr = network_addr + str(host_index)
        args=['ping', '-n', '1', addr]
        ping_output = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)
        ping_output_out = str(ping_output.communicate()[0]) 
        if "TTL" in str(ping_output_out):
            active_ip_list.append(addr)
        host_index += num_of_threads             
    


def trace_active_ips():    
    global total_time
    all_host_ips = capture_ips()
    check_valid_ip(my_ip, all_host_ips)
    
    thread_list = []   
    if num_of_threads == 1:
        check_active_ip(0)
    else:
        for offset in range(0, num_of_threads):
            tid1 = threading.Thread(target=check_active_ip, args=[offset])
            tid1.start()
            thread_list.append(tid1) 
            
            for offset in thread_list:
                offset.join()
    
    end_time = datetime.datetime.now()
    total_time = end_time - start_time
    return(active_ip_list)
    

def print_report(all_active_ips):
    print("There are %s active ip addresses in this subnet" % len(all_active_ips))
    print(','.join(all_active_ips))
    print("Total execution time with %s threads is %s" % (num_of_threads, total_time))


concurrency_threads()
all_active_ips = trace_active_ips()
print_report(all_active_ips)
