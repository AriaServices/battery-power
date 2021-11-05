#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description
License info
With code from: https://www.geeksforgeeks.org/python-script-to-shows-laptop-battery-percentage/

Requirements:
- psutil: sudo pip3 install psutil
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

# function returning time in hh:mm:ss
def convertTime(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)

# returns a tuple
battery = psutil.sensors_battery()

if __name__ == "__main__":
    if battery == None:
        print("No battery present on system.")
    else:
        print("Battery percentage : ", battery.percent)
        print("Power plugged in : ", battery.power_plugged)

        # converting seconds to hh:mm:ss
        print("Battery left : ", convertTime(battery.secsleft))
