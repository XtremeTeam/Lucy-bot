#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  horoscope_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import urllib2,re

from re import compile as re_compile

strip_tags = re_compile(r'<[^<>]+>')


horodb={u'\u0432\u043e\u0434\u043e\u043b\u0435\u0439': u'11', u'\u0440\u0430\u043a': u'4', u'\u0432\u0435\u0441\u044b': u'7', u'\u043a\u043e\u0437\u0435\u0440\u043e\u0433': u'10', u'\u0434\u0435\u0432\u0430': u'6', u'\u0431\u043b\u0438\u0437\u043d\u0435\u0446\u044b': u'3', u'\u0441\u0442\u0440\u0435\u043b\u0435\u0446': u'9', u'\u0441\u043a\u043e\u0440\u043f\u0438\u043e\u043d': u'8', u'\u0442\u0435\u043b\u0435\u0446': u'2', u'\u043b\u0435\u0432': u'5', u'\u043e\u0432\u0435\u043d': u'1', u'\u0440\u044b\u0431\u044b': u'12'}

def handler_horoscope_globa(type, source, parameters):
	if parameters:
		if parameters==u'Signs':
			reply('private',source,', '.join(horodb.keys()))
			return
		if horodb.has_key(string.lower(parameters)):
			req = urllib2.Request('http://horo.gala.net/?lang=ru&sign='+horodb[string.lower(parameters)])
			req.add_header = ('User-agent', 'Mozilla/5.0')
			r = urllib2.urlopen(req)
			target = r.read()
			"""sign name"""
			od = re.search('<span class=SignName>',target)
			h1 = target[od.end():]
			h1 = h1[:re.search('</span>',h1).start()]
			h1 += '\n'
			"""day"""
			od = re.search('<td class=blackTextBold nowrap>',target)
			h2 = target[od.end():]
			h2 = h2[:re.search('</td>',h2).start()]
			h2 += '\n'
			"""horoscope"""
			od = re.search('<td class=stext>',target)
			h3 = target[od.end():]
			h3 = h3[:re.search('</td>',h3).start()]
			if len(h3)<5:
				reply(type,source,u'Meanwhile the horoscope is not present')
				return
			message = h1+h2+h3
			message = decode(message)
			message=message.strip()
			reply(type,source,u'private')
			reply('private',source,unicode(message,'windows-1251'))
		else:
			reply(type, source, u'is that a sign of the zodiac?')	
			return	
	else:
		reply(type,source,u'For what sign of the horoscope to look for?')
		return


def decode(text):
    return strip_tags.sub('', text.replace('<br>','\n')).replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('\t','').replace('>[:\n','')

register_command_handler(handler_horoscope_globa, 'horoscope', ['info','fun','all'], 0, 'Показывает гороскоп для указзаного знака гороскопа. Все знаки - "гороскоп знаки".', 'horoscope [знак]', ['horoscope козерог','horoscope рыбы'])
