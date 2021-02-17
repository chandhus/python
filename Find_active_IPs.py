# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 00:12:09 2020
@author: Chandhu
"""

import subprocess
import sys
import threading
import datetime
import ipaddress


start_time = datetime.datetime.now()
my_ip = "143.168.0.102"
network_addr = "143.168.0."
start_addr = "143.168.0.1"
end_addr = "143.168.0.255"
curr_addr = start_addr

num_of_threads = 1
active_ip_list = []
total_time = ""
thread_ip_list = []
thread_exec_time = []


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

   
def check_active_ip(offset,lock):
    global curr_addr
    global end_addr
    start_thread_time = datetime.datetime.now()
    
    
    while int(ipaddress.IPv4Address(curr_addr)) <= int(ipaddress.IPv4Address(end_addr)) :
        lock.acquire()
        chk_ip = curr_addr
        curr_addr = ipaddress.ip_address(curr_addr) + 1
        lock.release()
        
        thread_ip_list[offset].append(str(chk_ip))
        args=['ping', '-n', '1', str(chk_ip)] 
        ping_output = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)
        ping_output_out = str(ping_output.communicate()[0]) 
        if " TTL" in str(ping_output_out):
            active_ip_list.append(str(chk_ip))
        
    end_thread_time = datetime.datetime.now()
    exec_time = end_thread_time - start_thread_time
    thread_exec_time[offset].append(str(exec_time))
    


def trace_active_ips():    
    global total_time
    global curr_addr
    all_host_ips = capture_ips()
    check_valid_ip(my_ip, all_host_ips)
    
    thread_list = []   
    if num_of_threads == 1:
        check_active_ip(0)
    else:
        lock = threading.Lock()
        
        for offset in range(num_of_threads):
            thread_ip_list.append([])
            thread_exec_time.append([])
        
        for offset in range(num_of_threads):
            tid1 = threading.Thread(target=check_active_ip, args=[offset,lock])
            tid1.start()
            thread_list.append(tid1) 
            
        for offset in thread_list:
            offset.join()
    
    end_time = datetime.datetime.now()
    total_time = end_time - start_time
    active_ip_list.sort()
    return(active_ip_list)
    

def print_report(all_active_ips):
    
    print("\nIP Addresses validated by each thread:")
    i = 0
    for x in thread_ip_list:
        print("\nThread-%s  IP Addresses:"% i)
        print(*x)
        i += 1
    print("\nExecution time for each thread in HH:MM:SS:MS format:")
    for x in thread_exec_time:
        print(*x)
    print("\nThere are %s active ip addresses in this subnet" % len(all_active_ips))
    print('\n'.join(all_active_ips))
    print("\nTotal execution time with %s threads in HH:MM:SS:MS format is %s" % (num_of_threads, total_time))


concurrency_threads()
active_ip_list = trace_active_ips()
print_report(active_ip_list)
