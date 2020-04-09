import psutil
import platform

from os import *
from datetime import datetime


def cpu_info():
    print("\n\t", platform.system(), "\n");
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Darwin":
        command = "/usr/sbin/sysctl -n machdep.cpu.brand_string"
        return popen(command).read().strip()
    if platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        print(popen(command).read().strip())
    return "\tPlatform not identified"


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def platform_info():
    print("\n-----System Information-----\n")
    uname = platform.uname()
    print(f"System    : {uname.system}")
    print(f"Node Name : {uname.node}")
    print(f"Release   : {uname.release}")
    print(f"Version   : {uname.version}")
    print(f"Machine   : {uname.machine}")
    print(f"Processor : {uname.processor}")


def boot_info():
    print("\n-----Boot Time-----\n")
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    print(f"Boot Time : {bt.year}/{bt.month}/{bt.day}  {bt.hour}:{bt.minute}:{bt.second}")
    

def cpu_usage_info():
    print("\n-----CPU Usage Information-----\n")
    print("Physical Cores : ", psutil.cpu_count(logical=False))
    print("Total Cores : ", psutil.cpu_count(logical=True))
    
    cpufreq = psutil.cpu_freq()
    print(f"Maximum frequency : {cpufreq.max:.2f}Mhz")
    print(f"Minimum frequency : {cpufreq.min:.2f}Mhz")
    print(f"Current frequency : {cpufreq.current:.2f}Mhz")
    
    print("CPU Usage per core:")
    for i,percentage in enumerate(psutil.cpu_percent(percpu=True)):
        print(f"Core{i} : {percentage}%")
    print(f"Total CPU Usage : {psutil.cpu_percent()}%")


def ram_info():
    print("\n-----Memory Information-----\n")
    
    svmem = psutil.virtual_memory()
    print(f"Total     : {get_size(svmem.total)}")
    print(f"Available : {get_size(svmem.available)}")
    print(f"Used      : {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")
    
    print("\nSWAP :-")
    swap = psutil.swap_memory()
    print(f"Total     : {get_size(swap.total)}")
    print(f"Free      : {get_size(swap.free)}")
    print(f"Used      : {get_size(swap.used)}")
    print(f"Percentage: {swap.percent}%")        
    
def disk_info():
    print("\n-----Disk Information-----\n")
    print("Partitions and Usage:")
    
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"\n\n----Device : {partition.device}---")
        print(f"\tMountpoint       : {partition.mountpoint}")
        print(f"\tFile system type : {partition.fstype} ")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        
        print(f"Total Size : {get_size(partition_usage.total)}")
        print(f"Used       : {get_size(partition_usage.used)}")
        print(f"Free       : {get_size(partition_usage.free)}")
        print(f"Percentage : {partition_usage.percent}%")
        disk_io = psutil.disk_io_counters()
        print(f"Total read  : {get_size(disk_io.read_bytes)}")
        print(f"Total write : {get_size(disk_io.write_bytes)}")
    
    
def main():
    line = '-' * 40
    print(f"\t{line}SYSTEM INFORMATION SCRIPT{line}\n")
    while True:  
        print(f"\n{line}\nSelect your option\n")
        opt = int(input("1.OS AND CPU INFORMATION\n2.PLATFORM INFORMATION\n3.BOOT TIME INFORMATION"
                        f"\n4.CPU USAGE INFORMATION\n5.RAM USAGE\n6.DISK SPACE INFORMATION\n7.EXIT\n{line}\n"))
        if opt == 1:
            cpu_info()
        elif opt == 2:
            platform_info()
        elif opt == 3:
            boot_info()
        elif opt == 4:
            cpu_usage_info()
        elif opt == 5:
            ram_info()
        elif opt == 6:
            disk_info()
        else:
            return
    
    
if __name__ == "__main__":
    main()
