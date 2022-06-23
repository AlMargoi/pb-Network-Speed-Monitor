import speedtest
import datetime
import csv
import time
import subprocess
import re
import os.path
import logging


def get_date():
    return datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logging.info(f"{get_date()} Starting script")

s = speedtest.Speedtest()
csv_file = 'network_performance.csv'
file_exists = os.path.isfile(csv_file)


with open(csv_file, mode='a+', newline='',buffering=1) as speedcsv:
    csv_writer = csv.DictWriter(speedcsv, fieldnames=['time', 'Wifi', 'downspeed', 'upspeed'])
    if not file_exists:
        logging.info(f"{get_date()} CSV file does not exist, writing headers.") 
        csv_writer.writeheader()
    while True:
        time_now = get_date()
        wifi_conn_bytes = subprocess.check_output('netsh wlan show interfaces')
        wifi_conn = wifi_conn_bytes.decode('utf8')
        try:
            wifi_name = re.findall(" SSID.*: (.*)\r\n", wifi_conn)[0]
        except IndexError:
            wifi_name = "Hamburger_2"
        try:
            downspeed = round((round(s.download()) / 1048576), 2)
        except BaseException as err:
            logging.error(f"{get_date()} Could not get 'downspeed': {err}: {type(err)}")
            downspeed = 0.0
        try:
            upspeed = round((round(s.upload()) / 1048576), 2)
        except BaseException as err:
            logging.error(f"{get_date()} Could not get 'upspeed': {err}: {type(err)}")
            upspeed = 0.0
        data_dict = {
            'time': time_now,
            'Wifi': wifi_name,
            'downspeed': downspeed,
            "upspeed": upspeed
        }
        csv_writer.writerow(data_dict)
        logging.info(f"{get_date()} Appended line: {data_dict}")
        time.sleep(120)