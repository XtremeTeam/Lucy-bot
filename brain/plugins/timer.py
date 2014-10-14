#--bot
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  timer_plugin.py	

#  Initial Copyright © 2010 Tuarisa <Tuarisa@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import time

def handler_timer (type, source, parameters):
	if not parameters:
		reply(type, source, u'Hey, learn to use the bot first!')
	str=0
	alarm = parameters.split()[0]
	if parameters.count (' '): str = parameters.split()[1]
	if alarm.count('*'):
		al=1
		for a in alarm.split('*'):
			al= al * int (a)
		alarm = al
	time.sleep(alarm)
	if str:
		reply(type, source, str)
	else:
		reply(type, source, u'Rise and shine!')
	
	
register_command_handler(handler_timer, 'timer', ['info','fan','all'], 10, 'Responds after a specified period of time with specified text.', 'timer <time> <text>', ['timer 10*60 wake up!'])
