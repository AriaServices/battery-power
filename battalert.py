#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description
License info
With code from: https://www.geeksforgeeks.org/python-script-to-shows-laptop-battery-percentage/

TODO:
- add settings file
- add cmd line params
- add action on low bat
- define low bat threshold
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

import os

# python script showing battery details
import psutil

# desktop notifications
import notify2

# function returning time in hh:mm:ss
def convertTime(seconds):
    if seconds < 0: seconds = seconds * -1
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes)

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
    if battery == None:
        n2_alert.update(n2_appname, "No battery available.")
    else:
        bat_percent = "{:.1f}%".format(battery.percent)
        bat_time = 'N/A'
        if battery.secsleft != -1:
            bat_time = convertTime(battery.secsleft)
        print("Battery percentage : {}".format(bat_percent))
        print("Power plugged in :   {}".format(battery.power_plugged))
        print("Battery left :       {}".format(bat_time))

        if battery.percent < 20.0 and not battery.power_plugged:
            n2_alert.update(n2_appname, "Battery power is {}. Plug-in power or hibernate in 1 minute.".format(bat_percent), img_bat_low)
        # else:
        #     n2_alert.update(n2_appname, "Battery power is {}. Continue working.".format(bat_percent))


    # show alert
    n2_alert.show()
