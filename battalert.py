#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description
Informs user of low battery and starts hibernate process before complete poweroff.

License info
With code from: https://www.geeksforgeeks.org/python-script-to-shows-laptop-battery-percentage/
With code from: https://gist.github.com/zkneupper/8c1faed1296ff0eb8923e6f2ee6fb74c (computer_sleep)

TODO:
- add log to /var/log
- add settings file
- add cmd line params
- add action on low bat
- define warning threshold
- define low bat threshold
- alternate config file
IMPROVEMENTS
- define multiple actions for different threshold

Requirements:
- psutil:  sudo pip3 install psutil
- notify2: sudo pip3 install notify2
"""

__author__ = 'Marcel Gerber'
__copyright__ = 'Copyright 2021, Linux Battery Alert'
__credits__ = ['{credit_list}']
__license__ = '{license}'
__version__ = '0.0.1'
__maintainer__ = 'Marcel Gerber'
__email__ = 'info@ariaservices.ch'
__status__ = 'dev'

# for path.abspath
import os

# add logging
import logging
log_file     = '/var/log/battalert.log'
log_encoding = 'utf-8'
log_format   = "[%(asctime)s] %(name)s - %(module)s (%(process)d) - %(levelname)s - %(message)s"
log_file_alt = "{}.log".format(os.path.splitext(os.path.basename(__file__))[0])

# import json for settings
import json
cfg_file = os.path.abspath('./battalert.yml')

# python script showing battery details
import psutil

# desktop notifications
import notify2

# load settings
def load_config(cfg_file):
    try:
        with open(cfg_file, 'r') as f:
            array = json.load(f)
        print("Successfully loaded config file '{}'.".format(cfg_file))
    except Exception as e:
        print("Error: could not load config file '{}'. {}".format(cfg_file, e))
        array = None
    return array

# save config to file
def save_config(cfg_file, cfg):
    try:
        with open(cfg_file, 'w') as f:
            json.dumps(cfg)
        logging.info("Successfully saved config to file '{}'.".format(cfg_file))
    except Exception as e:
        logging.error("Error: could not save config to file '{}'. {}".format(cfg_file, e))


# function returning time in hh:mm:ss
def convertTime(seconds):
    if seconds < 0: seconds = seconds * -1
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "{:02d}:{:02d}".format(hours, minutes)

# put computer to sleep depending on OS
def computer_sleep():
    if psutil.OSX:
        os.system("pmset sleepnow")
    elif psutil.LINUX:
        os.system("systemctl suspend")
    elif psutil.WINDOWS:
        os.system("shutdown -h")
    else:
        logging.error("Operating system not supported (not OSX, Linux or Windows).")

# icon files
img_bat_low = os.path.abspath('bat_low.png')

# notify2 vars
n2_appname = 'Battery Alert'

# get battery infos
battery = psutil.sensors_battery()

# prepare notification
notify2.init(n2_appname)
n2_alert = notify2.Notification(n2_appname, "No battery available.", img_bat_low)

if __name__ == "__main__":
    # load config from file
    cfg = load_config(cfg_file)
    if cfg != None:
        if cfg.log_file != '': log_file = cfg.log_file
    else:
        cfg['log_file'] = log_file

    # init logging
    try:
        logging.basicConfig(filename=log_file, format=log_format, encoding=log_encoding, level=logging.DEBUG)
    except PermissionError as e:
        logging.basicConfig(filename=log_file_alt, format=log_format, encoding=log_encoding, level=logging.DEBUG)
    logging.info("Running {} v. {}.".format(n2_appname, __version__))
    logging.info("Log file is '{}'.".format(log_file))

    if battery == None:
        n2_alert.update(n2_appname, "No battery available.")
        logging.info("There is no battery available on this system. No further action.")
    else:
        bat_percent = "{:.1f}%".format(battery.percent)
        bat_time = 'N/A'
        if battery.secsleft != -1:
            bat_time = convertTime(battery.secsleft)
        logging.debug("Battery percentage : {}".format(bat_percent))
        logging.debug("Power plugged in :   {}".format(battery.power_plugged))
        logging.debug("Battery left :       {}".format(bat_time))
        # logging.info("")

        if battery.percent < 20.0 and not battery.power_plugged:
            n2_alert.update(n2_appname, "Battery power is {}. Going to sleep.".format(bat_percent), img_bat_low)
            # show alert
            n2_alert.show()
            computer_sleep
        elif battery.power_plugged:
            logging.info("Battery is plugged in. No further action.")
        else:
            logging.info("Battery is discharging but enough remaining at {}. No further action.".format(bat_percent))

    # save config
    save_config(cfg_file, cfg)

    # end of script
    logging.info("{} completed.".format(n2_appname))
