#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin plugin
#  log_plugin.py

#  Initial Copyright © Anaлl Verrier <elghinn@free.fr> 
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Modifications Copyright  © 2007 marcus <x-team@xtreme.im>
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import re, os, math, time

#LOG_FILENAME_CACHE = eval(read_file(LOG_CACHE_FILE))

LOG_CACHE_FILE = 'settings/logcache.txt'

initialize_file(LOG_CACHE_FILE, '{}')



def log_write_header(fp, source, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings)):
	date = time.strftime('%A, %B %d, %Y', (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
	fp.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dt">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>%s</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style type="text/css">
<!--
.userjoin {color: #009900; font-style: italic; font-weight: bold}
.userleave {color: #dc143c; font-style: italic; font-weight: bold}
.statuschange {color: #a52a2a; font-weight: bold}
.rachange {color: #0000FF; font-weight: bold}
.userkick {color: #FF7F50; font-weight: bold}
.userban {color: #DAA520; font-weight: bold}
.nickchange {color: #FF69B4; font-style: italic; font-weight: bold}
.timestamp {color: #aaa;}
.timestamp a {color: #aaa; text-decoration: none;}
.system {color: #090; font-weight: bold;}
.emote {color: #800080;}
.self {color: #0000AA;}
.selfmoder {color: #DC143C;}
.normal {color: #483d8b;}
#mark { color: #aaa; text-align: right; font-family: monospace; letter-spacing: 3px }
h1 { color: #369; font-family: sans-serif; border-bottom: #246 solid 3pt; letter-spacing: 3px; margin-left: 20pt;}
h2 { color: #639; font-family: sans-serif; letter-spacing: 2px; text-align: center }
a.h1 {text-decoration: none;color: #369;}
#//-->
</style>
</head>
<body>
<div id="mark">Talisman log</div>
<h1><a class="h1" href="xmpp:%s?join" title="Join room">%s</a></h1>
<h2>%s</h2>
<div>
<tt>
""" % (' - '.join([source, date]), source, source, date))

def log_write_footer(fp):
	fp.write('\n</tt>\n</div>\n</body>\n</html>')

def log_get_fp(type, source, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings)):
	if type == 'public':
		logdir = PUBLIC_LOG_DIR
	else:
		logdir = PRIVATE_LOG_DIR
	if logdir[-1] == '/':
		logdir = logdir[:-1]
	str_year = str(year)
	str_month = str(month)
	str_day = str(day)
	filename = '.'.join(['/'.join([logdir, source, str_year, str_month, str_day]), 'html'])
	alt_filename = '.'.join(['/'.join([logdir, source, str_year, str_month, str_day]), '_alt.html'])
	if not os.path.exists('/'.join([logdir, source, str_year, str_month])):
		os.makedirs('/'.join([logdir, source, str_year, str_month]))
	if LOG_FILENAME_CACHE.has_key(source):
		if LOG_FILENAME_CACHE[source] != filename:
			fp_old = file(LOG_FILENAME_CACHE[source], 'a')
			log_write_footer(fp_old)
			fp_old.close()
		if os.path.exists(filename):
			fp = file(filename, 'a')
			return fp
		else:
			LOG_FILENAME_CACHE[source] = filename
			write_file(LOG_CACHE_FILE, str(LOG_FILENAME_CACHE))
			fp = file(filename, 'w')
			log_write_header(fp, source, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
			return fp
	else:
		if os.path.exists(filename):
			LOG_FILENAME_CACHE[source] = filename
			write_file(LOG_CACHE_FILE, str(LOG_FILENAME_CACHE))
			fp = file(alt_filename, 'a')
			return fp
		else:
			LOG_FILENAME_CACHE[source] = filename
			fp = file(filename, 'w')
			log_write_header(fp, source, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
			return fp

def log_regex_url(matchobj):
	# 06.03.05(Sun) slipstream@yandex.ru urls parser
	return '<a href="' + matchobj.group(0) + '">' + matchobj.group(0) + '</a>'

def log_handler_message(type, source, body):
	if not body:
		return
	if type == 'public' and PUBLIC_LOG_DIR:
		groupchat = source[1]
		nick = source[2]
		if groupchat in GROUPCHATS and nick in GROUPCHATS[groupchat] and 'ismoder' in GROUPCHATS[groupchat][nick] and GROUPCHATS[groupchat][nick]['ismoder'] == 1:
			ismoder=1
		else:
			ismoder=0
		log_write(body, nick, type, groupchat, ismoder)
	elif type == 'private' and PRIVATE_LOG_DIR:
		jid = get_true_jid(source)
		log_write(body, jid.split('@')[0], type, jid)

def log_handler_outgoing_message(target, body, obody):
	if GROUPCHATS.has_key(target) or not body:
		return
	log_write(body, DEFAULT_NICK, 'private', get_true_jid(target))

def log_write(body, nick, type, jid, ismoder=0):
	if not jid in GROUPCHATS.keys():
		jid = get_true_jid(jid)
	decimal = str(int(math.modf(time.time())[0]*100000))
	(year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = time.localtime()
	# 06.03.05(Sun) slipstream@yandex.ru urls parser & line ends
	body = body.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
	body = re.sub('(http|ftp)(\:\/\/[^\s<]+)', log_regex_url, body)
	body = body.replace('\n', '<br/>')
	body = body.encode('utf-8');
	nick = nick.encode('utf-8');
	timestamp = '[%.2i:%.2i:%.2i]' % (hour, minute, second)
	fp = log_get_fp(type, jid, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
	fp.write('<span class="timestamp"><a id="t' + timestamp[1:-1] + '.' + decimal + '" href="#t' + timestamp[1:-1] + '.' + decimal + '">' + timestamp + '</a></span> ')
	if not nick:
		fp.write('<span class="system">' + body + '</span><br />\n')
	elif body[:3].lower() == '/me':
		fp.write('<span class="emote">* %s%s</span><br />\n' % (nick, body[3:]))
	elif type == 'public' or nick == DEFAULT_NICK:
		if nick=='▌leave▐':
			fp.write('<span class="userleave">' + body + '</span><br />\n')
		elif nick=='▌join▐':
			fp.write('<span class="userjoin">' + body + '</span><br />\n')
		elif nick=='▌status▐':
			fp.write('<span class="statuschange">' + body + '</span><br />\n')
		elif nick=='▌ra▐':
			fp.write('<span class="rachange">' + body + '</span><br />\n')
		elif nick=='▌userkick▐':
			fp.write('<span class="userkick">' + body + '</span><br />\n')
		elif nick=='▌userban▐':
			fp.write('<span class="userban">' + body + '</span><br />\n')
		elif nick=='▌nickchange▐':
			fp.write('<span class="nickchange">' + body + '</span><br />\n')
		else:
			if ismoder:
				fp.write('<span class="selfmoder">&lt;%s&gt;</span> %s<br />\n' % (nick, body))
			else:
				fp.write('<span class="self">&lt;%s&gt;</span> %s<br />\n' % (nick, body))
	else:
		fp.write('<span class="normal">&lt;%s&gt;</span> %s<br />\n' % (nick, body))
	fp.close()

def log_handler_join(groupchat, nick, aff, role):
	log_write('%s joins the room as %s and %s' % (nick, role, aff), '▌join▐', 'public', groupchat)

def log_handler_leave(groupchat, nick, reason, code):
	if code:
		if code == '307':
			if reason:
				log_write('%s has been kicked (%s)' % (nick,reason), '▌userkick▐', 'public', groupchat)
			else:
				log_write('%s has been kicked' % (nick), '▌userkick▐', 'public', groupchat)			
		elif code == '301':
			if reason:
				log_write('%s has been banned (%s)' % (nick,reason), '▌userban▐', 'public', groupchat)
			else:
				log_write('%s has been banned' % (nick), '▌userban▐', 'public', groupchat)			
	else:
		if reason:
			log_write('%s leaves the room (%s)' % (nick,reason), '▌leave▐', 'public', groupchat)
		else:
			log_write('%s leaves the room' % (nick), '▌leave▐', 'public', groupchat)

def log_handler_presence(prs):
	stmsg,status,code,reason,newnick='','','','',''
	groupchat = prs.getFrom().getStripped()
	nick = prs.getFrom().getResource()
	code = prs.getStatusCode()
	reason = prs.getReason()
	if code == '303':
		newnick = prs.getNick()
		log_write('%s now is known as %s' % (nick,newnick), '▌nickchange▐', 'public', groupchat)
	else:
		if not prs.getType()=='unavailable':
			try:
				stmsg = prs.getStatus()
			except:
				stmsg=''
			try:
				status = prs.getShow()
			except:
				status = 'online'
			if not status:
				status = 'online'
			if stmsg:
				log_write('%s is now %s (%s)' % (nick,status,stmsg), '▌status▐', 'public', groupchat)
			else:
				log_write('%s is now %s' % (nick,status), '▌status▐', 'public', groupchat)	
			
			
if PUBLIC_LOG_DIR:
	register_message_handler(log_handler_message)
	register_join_handler(log_handler_join)
	register_leave_handler(log_handler_leave)
	register_presence_handler(log_handler_presence)
if PRIVATE_LOG_DIR:
	register_outgoing_message_handler(log_handler_outgoing_message)
