#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  update_plugin.py

#  Initial Copyright © 2009 Als//ъыь <als-als@ya.ru>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import urllib2

from re import compile as re_compile

strip_tags = re_compile(r'<[^<>]+>')


def update_lastrev():
	try:
		req = urllib2.Request('https://lucy-bot.googlecode.com/svn/trunk/')
		req.add_header = ('User-agent', 'Mozilla/5.0')
		r = urllib2.urlopen(req)
		target = r.read()
		od = re.search('<h2>Lucy-bot - Revision ',target)
		rev = target[od.end():]
		rev = rev[:re.search(': /trunk</h2>',rev).start()]
		return unicode(decode(rev),'windows-1251').strip()
	except:
		return ''
	
def update_lastrev_comment():
	try:
		req = urllib2.Request('https://lucy-bot.googlecode.com/svn/trunk/LAST')
		req.add_header = ('User-agent', 'Mozilla/5.0')
		r = urllib2.urlopen(req)
		target = r.read()
		return unicode(decode(target),'windows-1251').strip()	
	except:
		return ''
	
def handler_update_lastrev(type, source, parameters):
	if parameters=='+':
		update_work(state=True)
		reply(type,source,u'Check revisions every hour ON')
	elif parameters=='-':
		update_work(state=False)
		reply(type,source,u'Check new revisions every hour OFF')	
	elif parameters=='*':
		update_work(known=True)
		reply(type,source,u'did not update to the newest revision ...')	
	else:		
		reply(type,source,u'the latest available revision of the bot in trunk - %s\nYou %d revision\nComment to the audit:\n\n%s' % (update_lastrev(), BOT_VER['rev'], update_lastrev_comment()))
	
def update_lastrev_autonotify():
	lastrev=update_lastrev()
	updinfo=get_update_autonotify_state()
	if updinfo['state']:
		if updinfo['known']:
			if int(lastrev)!=updinfo['actual']:
				msg(ADMINS[0], u'the latest available revision of the bot in SVN trunk - %s\nYou have %d revision\nComment to audit:\n\n%s' % (lastrev, BOT_VER['rev'], update_lastrev_comment()))
				update_work(known=False, actual=int(lastrev))
		else:
			msg(ADMINS[0], u'the latest available revision of the bot in SVN branch trunk - %s\nYou have %d revision\nComment to the audit:\n\n%s' % (lastrev, BOT_VER['rev'], update_lastrev_comment()))
			update_work(actual=int(lastrev))
		threading.Timer(3600, update_lastrev_autonotify).start()
	
def get_update_autonotify_state():
	if check_file(file='updinfo.cfg'):
		updinfo = eval(read_file('settings/updinfo.cfg'))
	else:
		print 'error creating update info DB!!! default is always notify'
		return
	if not 'state' in updinfo:
		updinfo={'state': True, 'known': False, 'actual': None}
		write_file('settings/updinfo.cfg', str(updinfo))
	return updinfo
	
def update_work(state=None, known=None, actual=None):
	DBPATH='settings/updinfo.cfg'
	if check_file(file='updinfo.cfg'):
		updinfo = eval(read_file(DBPATH))
		if state!=None:
			updinfo['state']=state
		if known!=None:
			updinfo['known']=known
		if actual:
			updinfo['actual']=actual
		write_file(DBPATH, str(updinfo))	
	else:
		print 'error creating update info DB!!! default is always notify'
		return	

def decode(text):
    return strip_tags.sub('', text.replace('<br>','\n')).replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('\t','').replace('>[:\n','')

register_command_handler(handler_update_lastrev, COMM_PREFIX+'update', ['info','superadmin','all'], 100, 'Shows last audit of bot in it SVN to branch trunk. Parameters:\n+ TO INCLUDE updates about new audits (Check each hour)\n- TO DISCONNECT updates about new audits\n* To put a mark that is known to you about updating. Reminders on new audit will be gone before occurrence newer', 'botupd<+/*>', ['botupd +','botupd *','botupd -'])
register_stage2_init(update_lastrev_autonotify)
register_stage0_init(get_update_autonotify_state)
