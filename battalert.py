#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description
Informs user of low battery and starts hibernate process before complete poweroff.

License info
With code from: https://www.geeksforgeeks.org/python-script-to-shows-laptop-battery-percentage/
With code from: https://gist.github.com/zkneupper/8c1faed1296ff0eb8923e6f2ee6fb74c (computer_sleep)

TODO:
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

# defaults for app
def_app_warn_limit  = 15 # battery percentage for warning
def_app_warn_freq   =  5 # warn frequency in minutes
def_app_sleep_limit =  5 # battery percentage for sleep action

# for path.abspath
import os

# add logging
import logging
basename         = os.path.splitext(os.path.basename(__file__))[0]
log_console      = True # output log message to console
def_log_file     = '/var/log/{}.log'.format(basename)
log_file_alt     = "{}.log".format(basename)
def_log_level    = logging.DEBUG
def_log_encoding = 'utf-8'
def_log_format   = "%(asctime)s - %(module)s - %(process)d - %(levelname)s - %(message)s"

# import json for settings
import yaml
cfg_file = os.path.abspath('{}.yml'.format(basename))

# python script showing battery details
import psutil

# desktop notifications
import notify2

# log message to console and file
# do use before calling init_logging()
def log(message, msg_level=logging.INFO, log_level=def_log_level):
    logging.log(msg_level, message)
    if msg_level >= log_level: print(message)

# initialize logging facility
def init_logging(file=def_log_file, format=def_log_format, encoding=def_log_encoding, level=def_log_level):
    # init logging
    try:
        logging.basicConfig(filename=file, format=format, encoding=encoding, level=level)
    except PermissionError as e:
        file = "{}.log".format(os.path.splitext(__file__)[0])
        logging.basicConfig(filename=file, format=format, encoding=encoding, level=level)
    log("-------------------------------------------------")
    log("Running {} v. {}.".format(n2_appname, __version__))
    log("Log file is '{}'.".format(file))

# load settings
def load_config(cfg_file):
    try:
        with open(cfg_file, 'r') as f:
            cfg = yaml.safe_load(f)
        print("Successfully loaded config file '{}'.".format(cfg_file))
    except Exception as e:
        print("Warning: could load config file '{}'. {}.".format(cfg_file, e))
        cfg = None
    return cfg

# save config to file
def save_config(cfg_file, cfg):
    try:
        with open(cfg_file, 'w', encoding='utf-8') as f:
            yaml.dump(cfg, f, indent=4)
        log("Successfully saved config to file '{}'.".format(cfg_file))
    except Exception as e:
        log("Error: could save config to file '{}'. {}.".format(cfg_file, e), logging.ERROR)

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
        log("Operating system supported (not OSX, Linux or Windows).", logging.ERROR)

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
        cfg_init_msg = "Existing configuration was loaded from '{}'.".format(cfg_file)
    else:
        cfg_init_msg = "New configuration was created."
        cfg = {}

    # check config parts
    if not 'logging' in cfg: cfg['logging'] = {}
    if not 'app'     in cfg: cfg['app']     = {}

    if 'log_file'        in cfg['logging']: log_file        = cfg['logging']['log_file']
    else: cfg['logging']['log_file']     = def_log_file

    if 'log_level'       in cfg['logging']: log_level       = cfg['logging']['log_level']
    else: cfg['logging']['log_level']     = def_log_level

    if 'log_encoding'    in cfg['logging']: log_encoding    = cfg['logging']['log_encoding']
    else: cfg['logging']['log_encoding']     = def_log_encoding

    if 'log_format'      in cfg['logging']: log_format      = cfg['logging']['log_format']
    else: cfg['logging']['log_format']     = def_log_format

    if 'app_warn_limit'  in cfg['app']:     app_warn_limit  = cfg['app']['app_warn_limit']
    else: cfg['app']['app_warn_limit']     = def_app_warn_limit

    if 'app_warn_freq'   in cfg['app']:     app_warn_freq   = cfg['app']['app_warn_freq']
    else: cfg['app']['app_warn_freq']     = def_app_warn_freq

    if 'app_sleep_limit' in cfg['app']:     app_sleep_limit = cfg['app']['app_sleep_limit']
    else: cfg['app']['app_sleep_limit']     = def_app_sleep_limit
    init_logging()

    log("")

    if battery == None:
        n2_alert.update(n2_appname, "No battery available.")
        log("There is no battery available on this system. No further action.")
    else:
        bat_percent = "{:.1f}%".format(battery.percent)
        bat_time = 'N/A'
        if battery.secsleft != -1:
            bat_time = convertTime(battery.secsleft)
        log("Battery percentage : {}".format(bat_percent), logging.DEBUG)
        log("Power plugged in :   {}".format(battery.power_plugged), logging.DEBUG)
        log("Battery left :       {}".format(bat_time), logging.DEBUG)
        # log("")

        if battery.percent < 20.0 and not battery.power_plugged:
            n2_alert.update(n2_appname, "Battery power is {}. Going to sleep.".format(bat_percent), img_bat_low)
            # show alert
            n2_alert.show()
            computer_sleep
        elif battery.power_plugged:
            log("Battery is plugged in. No further action.")
        else:
            log("Battery is discharging but enough remaining at {}. No further action.".format(bat_percent))

    # save config
    save_config(cfg_file, cfg)

    # end of script
    log("{} completed.".format(n2_appname))
