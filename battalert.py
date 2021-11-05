#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description
License info
With code from: https://www.geeksforgeeks.org/python-script-to-shows-laptop-battery-percentage/

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

# python script showing battery details
import psutil

# desktop notifications
import notify2

# function returning time in hh:mm:ss
def convertTime(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)

# notify2 vars
n2_appname = 'Battery Alert'

# get battery infos
battery = psutil.sensors_battery()

# prepare notification
notify2.init(n2_appname)
n2_alert = notify2.Notification(n2_appname, "No battery available.", 'notification-battery-low')

if __name__ == "__main__":
    if battery == None:
        n2_alert.update(n2_appname, "No battery available.", 'notification-battery-low')
    else:
        print("Battery percentage : ", battery.percent)
        print("Power plugged in : ", battery.power_plugged)
        print("Battery left : ", convertTime(battery.secsleft))

        if battery.percent < 20 and battery.power_plugged:
            n2_alert.update(n2_appname, "Battery power is {}. Plug-in power or hibernate in 1 minute.".format(battery.percent), 'notification-battery-low')
        else:
            n2_alert.update(n2_appname, "Battery power is {}. Continue working.".format(battery.percent), 'notification-battery-low')


    # show alert
    n2_alert.show()
