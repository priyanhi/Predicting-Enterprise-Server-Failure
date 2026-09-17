import psutil
import pandas as pd
import time 
from datatime import datatime
from ping3 import ping
import os

# this line is writen to check that code is running succesfully or not because when i right PYTHON COLLECTOR.PY in samll latter then it was running but without printing anything 

print("collector start...")

# system file name 
file_name = "system_working_performance_dataset.csv"

# creating csv because it's not exist
if not os.path.exists(file_name):
    df = pd.DataFrame(columns = [
        "timestamp",
        "cpu_frequency_mhz",
        "cpu_usage",
        "memory_usage",
        "memory_availabale_gb",
        "disk_usage",
        "disk_read_mb",
        "disk_right_md",
        "network_set_mb",
        "network_recive_mb",
        "ping_ms",
        "battery_percent",
        "running_processes",
        "failure"
    ]) 
    df.tp_csv(file_name,
index = False)


# store previous disk and network counters
previous_disk = psutil.disk_io_counters()
previous_network = psutil.net_io_counters()

print("Data collection start...")
print("Press CTRL + C to stope\n")

# this line is writen to check that code is running succesfully or not because when i right PYTHON COLLECTOR.PY in samll latter then it was running but without printing anything 
print("Entering loop...")

while True:
    # current time
    timestamp = datatime.now().strftime("%Y-%m-%d %H:%M:%S")

    # CPU usage
    cpu_usage = psutil.cpu_percent(interval = 1)

    cpu_frequency = psutil.cpu_freq().current

    # Memory 
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    memory_avalible = round(memory.available / (1024*3), 2)

    # Disk Usage
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent

    # Disk Read / Wright
    current_disk = psutil.disk_io_counters()
    disk_read = round ((current_disk.read_bytes - previous_disk.read_bytes) / (1024**2), 2)
    disk_write = round((current_disk.write_bytes - previous_disk.write_bytes) / (1024**2), 2)
    previous_disk = current_disk

    # Network
    current_network = psutil.net_io_counters()
    sent = round((current_network.bytes_sent - previous_network.bytes_sent) / (1024**2), 2)
    received = round((current_network.bytes_recv - previous_network.bytes_recv) / (1024**2), 2)
    previous_network = current_network

    # Ping
    try:
        ping_ms = round(ping("8.8.8.8")* 1000, 2)
    except:
        ping_ms = None


    # Battery
    battery = psutil.sensors_battery()
    if battery:
        battery_percent = battery.percent
    else:
        battery_percent = None


    # Running Process
    process_count = len(psutil.pids())

    #bTemporary Failure Label
    failure = 0
    if cpu_usage > 90:
        failure = 1

    if memory_usage > 95:
        failure = 1

    if disk_usage > 95:
        failure = 1

    if ping_ms is not None and ping_ms > 300:
        failure = 1

    # store Row

    row = {
        "timestamp": timestamp,
        "cpu_usage": cpu_usage,
        "cpu_frequency_mhz": cpu_frequency,
        "memory_usage": memory_usage,
        "memory_available_gb": memory_avalible,
        "disk_usage": disk_usage,
        "disk_read_mb": disk_read,
        "disk_write_mb": disk_write,
        "network_sent_mb": sent,
        "network_received_mb": received,
        "ping_ms": ping_ms,
        "battery_percent":  battery_percent,
        "running_process" : process_count,
        "failure": failure
    }

    pd.DataFrame([row]).to_csv(
        file_name,
        mode = "a",
        header = False,
        index = False
    )

    print(row)
    time.sleep(5)