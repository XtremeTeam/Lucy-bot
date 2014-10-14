#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  info_plugin.py

#  Initial Copyright © 2007 Als <Als@exploru.net>
#  Parts of code Copyright © Bohdan Turkynewych aka Gh0st <tb0hdan[at]gmail.com>
#  A lot parts of code Copyright © 1998-2009 wd/lotusfeet <dao/yoga>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import sqlite3 as db
import time, os, threading

TIMER_ID = {}

def check_jid(jid):
	parse_jid = jid.split('@')
	
	if len(parse_jid) == 2:
		if parse_jid[0] and parse_jid[1]:
			if parse_jid[1].count('.') >= 1 and parse_jid[1].count('.') <= 3:
				return True
			else:
				return False	
		else:
			return False
	else:
		return False

def queryinfo(dbpath,query):
	cursor,connection = None, None
	try:
		connection=db.connect(dbpath)
		cursor=connection.cursor()
		cursor.execute(query)
		result=cursor.fetchall()
		connection.commit()
		cursor.close()
		connection.close()
		return result
	except:
		if cursor:
			cursor.close()
		if connection:
			connection.commit()
			connection.close()
		return ''

def get_jids(gch, affiliation):
	iq=xmpp.Iq('get')
	ID = 'bot' + str(random.randrange(1000, 9999))
	iq.setID(ID)
	iq.setTo(gch)
	iq.setAttr('xml:encoding','utf-8')
	query = xmpp.Node('query') 
	query.setNamespace(xmpp.NS_MUC_ADMIN) 
	query.addChild('item', {'affiliation': affiliation}) 
	iq.addChild(node=query)
	
	response = JCON.SendAndWaitForResponse(iq, 10)
	
	ptype = response.getType()
	
	if ptype == 'result' and response.getID() == ID:
		return response

def parse_stanza(stanza):
	itlist = stanza.getTag('query').getTags('item')
	jlist = [li.getAttr('jid') for li in itlist]
	jlist.sort()
	rng = range(len(jlist))
	njlist = ['%s) %s' % (li+1, jlist[li]) for li in rng]
	return njlist

def check_timerid(gch,timerid):
	sql = 'SELECT * FROM reminds WHERE timerid="%s";' % (timerid)
	qres = queryinfo('dynamic/'+gch+'/reminds.db',sql)
	
	if qres:
		return False
	else:
		return True
	
def rem_timer(groupchat,cts,dts,nick,jid,mess,timerid=''):
	atime = time.strftime('%H:%M:%S',time.localtime(dts))
	rsecs = int(round(dts - cts))
	
	if not nick:
		nick = get_rem_nick(groupchat, jid)
		
	source = [groupchat+'/'+nick,groupchat,nick]
	
	if GROUPCHATS[groupchat].has_key(nick):
		if GROUPCHATS[groupchat][nick]['ishere'] == 1:
			del_remind(groupchat, jid, mess, timerid)
			rep = u'Reminder to %s later %s:\n\n%s' %(atime, timeElapsed(rsecs),mess)
			reply('private', source, rep)
	
def get_jid(gch, nick):
	nick = nick.replace('"','&quot;')
	sql = 'SELECT jid FROM users WHERE nick="%s";' % (nick)
	qres = queryinfo('dynamic/'+gch+'/users.db',sql)
	
	if qres:
		jid = qres[0][0]
		return jid

def get_rem_nick(gch, jid):
	nick = ''

	nickl = [li for li in GROUPCHATS[gch] if jid in GROUPCHATS[gch][li]['jid'] and GROUPCHATS[gch][li]['ishere'] == 1]
	
	if nickl:
		nick = nickl[-1]
		
	return nick		
		
def save_remind(gch,nick,jid,rtime,ctms,dsts,mess,status,timerid):
	mess = mess.replace(r'"', r'&quot;')
	sql = 'INSERT INTO reminds (nick,jid,rtime,ctms,dsts,mess,status,timerid) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s");' % (nick,jid,rtime,ctms,dsts,mess,status,timerid)
	rep = queryinfo('dynamic/'+gch+'/reminds.db',sql)
	
	if rep != '':
		return rep
	else:
		upd_sql = 'UPDATE reminds SET "nick"="%s", "jid"="%s", "rtime"="%s", "ctms"="%s", "dsts"="%s", "status"="%s", "timerid"="%s" WHERE mess="%s";' % (nick,jid,rtime,ctms,dsts,status,mess,timerid)
		rep = queryinfo('dynamic/'+gch+'/reminds.db',upd_sql)
		return rep

def recover_remind(gch, rem_handler, recover, reminds):
	for rem in reminds:
		type = 'private'
		
		jid = get_jid(gch, rem[0])
		nick = get_rem_nick(gch, rem[1])
		
		source = [gch+'/'+nick,gch,nick]
		rem2 = rem[2]
		
		if not ':' in rem2:
			rem2 = time.strftime('%H:%M:%S',time.localtime(float(rem[4])))
		
		parameters = rem2+' '+rem[5]
		
		with smph:
			INFO['thr'] += 1
			try:
				threading.Thread(None,rem_handler,'remind'+str(INFO['thr']),(type, source, parameters, recover,rem[1],rem[3],rem[7])).start()
			except RuntimeError:
				pass

def show_reminds(gch, jid, reminds, pref='', suff=''):
	freml = [rel for rel in reminds if rel[1] == jid and rel[6] == 'run']
	
	nick = get_rem_nick(gch, jid)
	
	sh_freml = []
	
	sh_freml = [rel for rel in freml if rel[1] in GROUPCHATS[gch][nick]['jid']]
	
	if sh_freml:
		rng = range(len(sh_freml))
		
		if suff:
			nremli = ['%s) %s%s%s:\n%s' % (li+1, pref, time.strftime('%H:%M:%S',time.localtime(float(sh_freml[li][4]))), suff+timeElapsed(float(sh_freml[li][4])-time.time()), sh_freml[li][5]) for li in rng]
		else:
			nremli = [u'%s) %s%s, %s ago:\n%s' % (li+1, pref, time.strftime('%H:%M:%S',time.localtime(float(sh_freml[li][4]))), timeElapsed(time.time()-float(sh_freml[li][4])), sh_freml[li][5]) for li in rng]
			
		return nremli
	else:
		return []

def exp_reminds(reminds,jid):
	ctm = time.time()
	chkreml = [rel for rel in reminds if float(rel[4]) <= ctm and rel[1] == jid]
	return chkreml

def check_reminds(reminds,jid):
	ctm = time.time()
	chkreml = [rel for rel in reminds if float(rel[4]) > ctm and rel[1] == jid]
	return chkreml

def del_remind(gch, jid, mess, timerid=''):
	if timerid:
		del_sql = 'DELETE FROM reminds WHERE jid="%s" AND mess="%s" AND timerid="%s";' % (jid, mess,timerid)
	else:
		del_sql = 'DELETE FROM reminds WHERE jid="%s" AND mess="%s";' % (jid, mess)
		
	res = queryinfo('dynamic/'+gch+'/reminds.db',del_sql)
	return res

def get_reminds(gch):
	del_sql = 'DELETE FROM reminds WHERE status="done";'
	queryinfo('dynamic/'+gch+'/reminds.db',del_sql)
	
	sql = 'SELECT * FROM reminds WHERE status="run" ORDER BY dsts;'
	reminds = queryinfo('dynamic/'+gch+'/reminds.db',sql)
	return reminds

def get_dm_nicks(gch):
	sql = 'SELECT nick FROM users ORDER BY uleave;'
	qres = queryinfo('dynamic/'+gch+'/users.db',sql)
	
	if qres:
		nicks = [nil[0].replace('&quot;','"') for nil in qres]
		return nicks
	
def rmv_dm_nick(gch, body):
	conf_nicks = GROUPCHATS[gch].keys()
	nicks = get_nicks(gch)
	nbody = body
	nbli = body.split(',')
	nbli = [nbl.split(':') for nbl in nbli]
	nbli2 = []
	
	for nbl in nbli:
		nbli2.extend(nbl)
	
	nbli = [nbl.strip() for nbl in nbli2]
	
	fonil = []
	
	for nil in nicks:
		for nbl in nbli:
			if nil == nbl:
				fonil.append(nil)
	
	for nil in fonil:
		body = body.replace(nil,'',1)
	
	for nil in conf_nicks:
		if nil in body.split(' ')[0]:
			fpar = body.split(' ')[0]
			body = body.replace(fpar,'',1)
			break
	
	if body:
		while body[0] == ':' or body[0] == ',':
			body = body[1:].strip()
		
	body = body.strip()
	return body

def get_hd_dm_nick(gch,body):
	conf_nicks = GROUPCHATS[gch].keys()
	nicks = get_nicks(gch)
	
	splbod = body.split(':',1)
	splbod = [sbli for sbli in splbod if sbli]

	if len(splbod) == 2:
		prob_nick = splbod[0].strip()
		
		if prob_nick in nicks:
			return prob_nick

	splbod = body.split(',',1)
	splbod = [sbli for sbli in splbod if sbli]

	if len(splbod) == 2:
		prob_nick = splbod[0].strip()
		
		if prob_nick in nicks:
			return prob_nick
	
	return ''

def del_dms(gch,jid):
	sql = 'DELETE FROM dmess WHERE djid="%s"' % (jid)
	qres = queryinfo('dynamic/'+gch+'/dmess.db',sql)
	
	return qres

def get_dms(gch,jid):
	sql = 'SELECT * FROM dmess WHERE djid="%s"' % (jid)
	qres = queryinfo('dynamic/'+gch+'/dmess.db',sql)
	
	return qres

def save_dm(gch,snick,sjid,dnick,djid,mess):
	date = time.time()
	mess = mess.replace('"','&quot;')
	
	sql = 'SELECT mess FROM dmess WHERE mess="%s"' % (mess)
	qres = queryinfo('dynamic/'+gch+'/dmess.db',sql)
	
	if not qres:
		sql = 'INSERT INTO dmess (snick,sjid,dnick,djid,mess,date) VALUES ("%s","%s","%s","%s","%s","%s");' % (snick,sjid,dnick,djid,mess,date)
	else:
		sql = 'UPDATE dmess SET "snick"="%s", "sjid"="%s", "dnick"="%s", "djid"="%s", "date"="%s" WHERE mess="%s";' % (snick,sjid,dnick,djid,date,mess)
	
	qres = queryinfo('dynamic/'+gch+'/dmess.db',sql)
	
	return qres
	
def show_dms(dms):
	if dms:
		ndmsli = [u'%d) Posted %s %s в %s:\n\n%s' % (dms.index(ndli)+1,ndli[0],time.strftime('%d.%m.%Y',time.localtime(float(ndli[5]))),time.strftime('%H:%M:%S',time.localtime(float(ndli[5]))),ndli[4].replace('&quot;','"')) for ndli in dms]
		return ndmsli
	
	return []
	
def handler_members(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return

	resp = get_jids(groupchat, 'member')
	njids = []
	
	if resp:
		njids = parse_stanza(resp)
	
	if type == 'public':
		reply(type, source, u'Look in private!')
		
	if njids:
		rep = u'Regular participants (total: ' + str(len(njids))+ '):\n' + '\n'.join(njids)
	else:
		rep = u'List of Permanent member empty!'	
		
	reply('private', source, rep)
	
def handler_admins(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return

	resp = get_jids(groupchat, 'admin')
	njids = []
	
	if resp:
		njids = parse_stanza(resp)
	
	if type == 'public':
		reply(type, source, u'Look in private!')
		
	if njids:
		rep = u'Admins (total: ' + str(len(njids))+ '):\n' + '\n'.join(njids)
	else:
		rep = u'List admins empty!'
		
	reply('private', source, rep)
	
def handler_owners(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return

	resp = get_jids(groupchat, 'owner')
	njids = []
	
	if resp:
		njids = parse_stanza(resp)
	
	if type == 'public':
		reply(type, source, u'Look in private!')
		
	reply('private', source, u'Owner (total: ' + str(len(njids))+ '):\n' + '\n'.join(njids))
	
def handler_outcasts(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return

	resp = get_jids(groupchat, 'outcast')
	njids = []
	
	if resp:
		njids = parse_stanza(resp)
	
	if type == 'public':
		reply(type, source, u'Look in private!')
		
	if njids:
		rep = u'Banned (total: ' + str(len(njids))+ '):\n' + '\n'.join(njids)
	else:
		rep = u'List of banned empty!'	
			
	reply('private', source, rep)

def get_info_state(gch):
	global TIMER_ID
	
	TIMER_ID[gch] = {}
	
	if not 'dmess' in GCHCFGS[gch]:
		GCHCFGS[gch]['dmess'] = 0
	if not os.path.exists('dynamic/'+gch+'/users.db'):
		sql = 'CREATE TABLE users (id integer primary key autoincrement, nick varchar(30) not null, jid varchar(30) not null, ujoin varchar(20) not null, uleave varchar(20) not null,reason varchar,unique(nick));'
		queryinfo('dynamic/'+gch+'/users.db',sql)
	if not os.path.exists('dynamic/'+gch+'/reminds.db'):
		sql = 'CREATE TABLE reminds (nick varchar(30) not null, jid varchar(30) not null, rtime varchar(20) not null, ctms varchar(20) not null, dsts varchar(20) not null, mess varchar not null, status varchar(10) not null, timerid varchar(20) not null, unique (timerid));'
		queryinfo('dynamic/'+gch+'/reminds.db',sql)
	if not os.path.exists('dynamic/'+gch+'/dmess.db'):
		sql = 'CREATE TABLE dmess (snick varchar(30) not null, sjid varchar(30) not null, dnick varchar(30) not null, djid varchar(30) not null, mess varchar not null, date varchar(20) not null);'
		queryinfo('dynamic/'+gch+'/dmess.db',sql)

def handler_dmess_control(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	if parameters:
		if not parameters.isdigit():
			reply(type,source,u'Invalid syntax!')
			return
			
		if int(parameters) > 1:
			reply(type,source,u'Invalid syntax!')
			return
		
		if parameters == "1":
			GCHCFGS[groupchat]['dmess'] = 1
			reply(type,source,u'Auto pending messages enabled!')
		else:
			GCHCFGS[groupchat]['dmess'] = 0
			reply(type,source,u'Auto pending messages disabled!')
		write_file('dynamic/'+groupchat+'/config.cfg', str(GCHCFGS[groupchat]))
	else:
		if GCHCFGS[groupchat]['dmess'] == 1:
			reply(type,source,u'Auto pending messages enabled!')
		else:
			reply(type,source,u'Auto pending messages disabled!')

def handler_dmess(type, source, body):
	groupchat = source[1]
	snick = source[2]
	sjid = get_true_jid(groupchat+'/'+snick)
	
	dmess = 0
	
	if GROUPCHATS.has_key(groupchat):
		dmess = GCHCFGS[groupchat]['dmess']
		
	if dmess and len(body) <= 512:
		nicks = get_nicks(groupchat)
		conf_nicks = GROUPCHATS[groupchat].keys()
		here_nicks = [hli for hli in conf_nicks if GROUPCHATS[groupchat][hli]['ishere'] == 1]
		here_jids = [GROUPCHATS[groupchat][hli]['jid'].split('/')[0] for hli in here_nicks]
		
		dnick = get_hd_dm_nick(groupchat,body)
		
		if dnick and dnick in nicks or dnick in conf_nicks:
			djid = get_jid(groupchat,dnick)
			mess = rmv_dm_nick(groupchat,body)
			
			if djid and not djid in here_jids:
				res = save_dm(groupchat,snick,sjid,dnick,djid,mess)
				
				if res != '':
					reply(type,source,u'Message has been saved and will be sent to the user in private the next time you log into a conference!')

def handler_tell(type, source, parameters):
	groupchat = source[1]
	snick = source[2]
	sjid = get_true_jid(groupchat+'/'+snick)
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	if parameters:
		nicks = get_nicks(groupchat)
		conf_nicks = GROUPCHATS[groupchat].keys()
		here_nicks = [hli for hli in conf_nicks if GROUPCHATS[groupchat][hli]['ishere'] == 1]
		here_jids = [GROUPCHATS[groupchat][hli]['jid'].split('/')[0] for hli in here_nicks]
		
		dnick = get_hd_dm_nick(groupchat,parameters)
		
		if dnick:
			djid = get_jid(groupchat,dnick)
			mess = rmv_dm_nick(groupchat,parameters)
			
			if djid and not djid in here_jids and mess:
				res = save_dm(groupchat,snick,sjid,dnick,djid,mess)
				
				if res != '':
					reply(type,source,u'Message has been saved and will be sent to the user in private the next time you log into a conference!')
			else:
				reply(type,source,u'Hey look, he is sitting here!')
		else:
			reply(type,source,u'Something wrong!')
	else:
		reply(type,source,u'And, who??')	
	
def handler_user_join(groupchat, nick, aff, role):
	jid = get_true_jid(groupchat+'/'+nick)
	
	qnick = nick.replace('"','&quot;')
	
	check_sql = 'SELECT nick FROM users WHERE nick="%s"' % (qnick)
	qres = queryinfo('dynamic/'+groupchat+'/users.db',check_sql)
	
	if GROUPCHATS[groupchat].has_key(nick):
		ujoin = GROUPCHATS[groupchat][nick]['joined']
	else:
		ujoin = time.time()
	
	if qres:
		upd_sql = 'UPDATE users SET "ujoin"="%s", "jid"="%s" WHERE nick="%s";' % (ujoin,jid,qnick.strip())
		queryinfo('dynamic/'+groupchat+'/users.db',upd_sql)
	else:
		ins_sql = 'INSERT INTO users (nick,jid,ujoin,uleave,reason) VALUES ("%s","%s","%s","%s","%s");' % (qnick.strip(),jid.strip(),ujoin,ujoin,'')
		queryinfo('dynamic/'+groupchat+'/users.db',ins_sql)
		
	reminds =get_reminds(groupchat)
	rems = check_reminds(reminds,jid)

	if rems:
		recover_remind(groupchat, handler_remind, True, rems)
	
	exp_rems = exp_reminds(reminds,jid)
	
	if exp_rems:
		for rel in exp_rems:
			del_remind(groupchat, rel[1], rel[5], rel[7])
	
	nexp_repl = show_reminds(groupchat, jid, exp_rems, pref=u'В ')		
		
	if nexp_repl:
		rep = u'Missed reminder:\n%s' % ('\n\n'.join(nexp_repl))
		msg(groupchat+'/'+nick,rep)
		
	dmsl = get_dms(groupchat,jid)
	ndmsl = show_dms(dmsl)
	
	if ndmsl:
		rep = u'Favorite posts:\n%s' % ('\n\n'.join(ndmsl))
		msg(groupchat+'/'+nick,rep)
		del_dms(groupchat,jid)
	
def handler_user_leave(groupchat, nick, reason, code):
	jid = get_true_jid(groupchat+'/'+nick)
	
	qnick = nick.replace('"','&quot;')
	
	check_sql = 'SELECT nick FROM users WHERE nick="%s"' % (qnick)
	qres = queryinfo('dynamic/'+groupchat+'/users.db',check_sql)
	
	uleave = time.time()
	
	if not reason:
		reason = ''
	
	if qres:
		upd_sql = 'UPDATE users SET "uleave"="%s", "reason"="%s"  WHERE nick="%s";' % (uleave,reason.strip(),qnick)
		queryinfo('dynamic/'+groupchat+'/users.db',upd_sql)

def handler_user_presence(prs):
	ptype = prs.getType()
	groupchat = prs.getFrom().getStripped()
	nick = prs.getFrom().getResource()
	jid=get_true_jid(groupchat+'/'+nick)
	scode = prs.getStatusCode()
	ujoin = time.time()
	
	if scode == '303' and ptype == 'unavailable':
		newnick = prs.getNick()	
				
		qnewnick = newnick.replace('"','&quot;')
				
		check_sql = 'SELECT nick FROM users WHERE nick="%s"' % (qnewnick)
		qres = queryinfo('dynamic/'+groupchat+'/users.db',check_sql)
			
		if GROUPCHATS[groupchat].has_key(nick):
			ujoin = GROUPCHATS[groupchat][nick]['joined']	
			
		if qres:
			upd_sql = 'UPDATE users SET "jid"="%s" WHERE nick="%s";' % (jid,qnewnick.strip())
			queryinfo('dynamic/'+groupchat+'/users.db',upd_sql)
		else:
			ins_sql = 'INSERT INTO users (nick,jid,ujoin,uleave,reason) VALUES ("%s","%s","%s","%s","%s");' % (qnewnick.strip(),jid.strip(),ujoin,ujoin,'')
			queryinfo('dynamic/'+groupchat+'/users.db',ins_sql)

def handler_seen(type, source, parameters):
	groupchat = source[1]
	nick_jid = parameters.strip()
	curr_time = time.time()
	
	if not parameters:
		reply(type, source, u'And, who?')
		return
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	jid = ''
	nick = ''
	
	if check_jid(nick_jid):
		jid = nick_jid
	else:
		nick = nick_jid
	
	qnick = nick.replace('"','&quot;')
	
	if jid:
		qres = []
		
		for I in GROUPCHATS[groupchat]:
			rjid = GROUPCHATS[groupchat][I]['jid'].split('/')[0]
			
			if jid == rjid:
				if GROUPCHATS[groupchat][I]['ishere'] == 1:
					nick = I
					check_sql = 'SELECT nick,ujoin,uleave FROM users WHERE nick="%s"' % (qnick)
					qres = queryinfo('dynamic/'+groupchat+'/users.db',check_sql)
					break
						
		if not qres:
			check_sql = 'SELECT nick,ujoin,uleave FROM users WHERE jid="%s" ORDER BY uleave' % (jid)
			qres = queryinfo('dynamic/'+groupchat+'/users.db',check_sql)

		
		if qres:
			qres = list(qres[-1])
			gnick = qres[0].replace('&quot;','"')
			join_time = float(qres[1])
			leave_time = float(qres[2])
			
			if not GROUPCHATS[groupchat].has_key(gnick):
				seen_time = curr_time - leave_time
				here_time = leave_time - join_time
				rep = u'User '+ gnick + u' was here %s ago and stay in the conference about %s.' % (timeElapsed(seen_time), timeElapsed(here_time))
				reply(type, source, rep)
				return
			elif GROUPCHATS[groupchat].has_key(gnick):
				gjid = GROUPCHATS[groupchat][gnick]['jid'].split('/')[0]
				
				if GROUPCHATS[groupchat][gnick]['ishere'] == 0 and gjid == jid:
					seen_time = curr_time - leave_time
					here_time = leave_time - join_time
					rep = u'User '+ gnick + u' was here %s ago and stay in the conference about %s.' % (timeElapsed(seen_time), timeElapsed(here_time))
					reply(type, source, rep)
					return
				else:
					rep = u'Open your eyes and you should look closely, he was sitting here!'
					reply(type, source, rep)
					return
					
			else:
				rep = u'User %s never been in this conference!' % (jid)
				reply(type, source, rep)
				return
		else:
			rep = u'User %s never been in this conference!' % (jid)
			reply(type, source, rep)	
	elif nick:
		check_sql = 'SELECT nick,ujoin,uleave,jid FROM users WHERE nick="%s"' % (qnick)
		qres = queryinfo('dynamic/'+groupchat+'/users.db',check_sql)
		
		if qres:
			jid = list(qres[0])[3]
		
		gnick = ''
		
		for I in GROUPCHATS[groupchat]:
			rjid = GROUPCHATS[groupchat][I]['jid'].split('/')[0]
			
			if jid == rjid:
				if GROUPCHATS[groupchat][I]['ishere'] == 1:
					gnick = I
					break
	
		check_sql = 'SELECT nick,ujoin,uleave,jid FROM users WHERE jid="%s" ORDER BY uleave' % (jid)
		qres = queryinfo('dynamic/'+groupchat+'/users.db',check_sql)
	
		if qres:
			qres = list(qres[-1])
			
			if not gnick:
				gnick = qres[0].replace('&quot;','"')
			
			join_time = float(qres[1])
			leave_time = float(qres[2])
			
			if not GROUPCHATS[groupchat].has_key(gnick):
				seen_time = curr_time - leave_time
				here_time = leave_time - join_time
				rep = u'User '+ nick + u' was here %s ago and stay in the conference about %s.' % (timeElapsed(seen_time), timeElapsed(here_time))
				reply(type, source, rep)
				return
			elif GROUPCHATS[groupchat].has_key(gnick):
				if GROUPCHATS[groupchat][gnick]['ishere'] == 0:
					seen_time = curr_time - leave_time
					here_time = leave_time - join_time
					rep = u'User '+ nick + u' was here %s ago and stay in the conference about %s.' % (timeElapsed(seen_time), timeElapsed(here_time))
					reply(type, source, rep)
					return
				else:
					rep = u'Open your eyes and you should look closely, he was sitting here!'
					reply(type, source, rep)
					return
		else:
			rep = u'Users %s never been in this conference!' % (nick)
			reply(type, source, rep)
			
def handler_here(type, source, parameters):
	groupchat = source[1]
	nick = source[2]
	here_nick = parameters.strip()
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	if parameters:
		if GROUPCHATS[groupchat].has_key(here_nick):
			if GROUPCHATS[groupchat][here_nick]['ishere'] == 1:
				join_time = GROUPCHATS[groupchat][here_nick]['joined']
				curr_time = time.time()
				here_time = timeElapsed(curr_time - join_time)
				
				if here_nick == nick:
					rep = u'You are stay in the conference: ' + here_time + u'.'
				else:
					rep =u'User '+ here_nick + u' stay in the conference: ' + here_time + u'.'
				
				reply(type, source, rep)
			else:
				reply(type, source, u'And, who?')
		else:
			reply(type, source, u'And, who?')		
	else:
		join_time = GROUPCHATS[groupchat][nick]['joined']
		curr_time = time.time()
		here_time = timeElapsed(curr_time - join_time)
		rep = u'You are stay in the conference: ' + here_time + u'.'
		reply(type, source, rep)

def handler_nicks(type, source, parameters):
	groupchat=source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	if parameters:
		prob_jid = parameters.strip()
		
		if check_jid(prob_jid):
			sql = 'SELECT nick,ujoin FROM users WHERE jid="%s" ORDER BY ujoin DESC;' % (prob_jid)
			qres = queryinfo('dynamic/'+groupchat+'/users.db',sql)
			
			if qres:
				qres = [li[0].replace('&quot;','"') for li in qres]
				rep=u'Users %s used here nicks (total: %d): %s.' % (prob_jid,len(qres),', '.join(qres))
			else:
				rep=u'Users %s never been here!' % (prob_jid)
		else:
			prob_nick = prob_jid
			jid = get_jid(groupchat, prob_nick)
			
			if jid:
				sql = 'SELECT nick,ujoin FROM users WHERE jid="%s" ORDER BY ujoin DESC;' % (jid)
				qres = queryinfo('dynamic/'+groupchat+'/users.db',sql)
				
				if qres:
					qres = [li[0].replace('&quot;','"') for li in qres]
					rep=u'Users %s used here nicks (total: %d): %s.' % (prob_nick,len(qres),', '.join(qres))
				else:
					rep=u'Unknown error!'
			else:
				rep=u'Users %s used here nicks!' % (prob_nick)
	else:
		sql = 'SELECT nick,ujoin FROM users ORDER BY nick;'
		qres = queryinfo('dynamic/'+groupchat+'/users.db',sql)
		ctm = time.time()
		
		if qres:
			qres = [li[0].replace('&quot;','"') for li in qres if (ctm - float(li[1])) <= 2592000]
			rep=u'There were seen nicks (total: %d): %s.' % (len(qres),', '.join(qres))
		else:
			rep=u'Unknown error!'
		
	reply(type, source, rep)
		
def handler_groupchats(type, source, parameters):
	groupchats = GROUPCHATS.keys()
	groupchats.sort()
	rep = u'I am currently in conferences (total: '+str(len(groupchats))+ u'): '+', '.join(groupchats).encode('utf8')+'.'
	reply(type, source, rep)

def handler_getrealjid(type, source, parameters):
	groupchat=source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	if not parameters:
		reply(type, source, u'And, who?')
		return
	
	nick = parameters.strip()
	
	sql = 'SELECT jid FROM users WHERE nick="%s";' % (nick.replace('"','&quot;'))
	qres = queryinfo('dynamic/'+groupchat+'/users.db',sql)
	
	if not qres:
		reply(type,source,u'Are you sure, that '+nick+u' was here?')
		return
	else:
		truejid=qres[0][0]
		
		if type == 'public':
			reply(type, source, u'Look in private!')
			
	reply('private', source, u'Real JID '+nick+u': '+truejid)
		
def handler_total_in_muc(type, source, parameters):
	groupchat=source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	ulist = [uli for uli in GROUPCHATS[groupchat].keys() if GROUPCHATS[groupchat][uli]['ishere'] == 1]
	ulist.sort()
	rep = u'Users (total: '+str(len(ulist))+u'): '+u', '.join(ulist)+'.'
	reply(type, source, rep)
		
def handler_bot_uptime(type, source, parameters):
	if INFO['start']:
		uptime=int(time.time() - INFO['start'])
		rep,mem = u'I have been working for '+timeElapsed(uptime),''
		rep += u'\nObtained %s messages, processed %s presence and %s iq-query, and holds %s commands.\n'%(str(INFO['msg']),str(INFO['prs']),str(INFO['iq']),str(INFO['cmd']))
		if os.name=='posix':
			try:
				pr = os.popen('ps -o rss -p %s' % os.getpid())
				pr.readline()
				mem = pr.readline().strip()
				pr.close()
			except:
				pass
			if mem: rep += u'I also consume %s Kb memory, ' % mem
		(user, system,qqq,www,eee,) = os.times()
		rep += u'spent %.2f CPU seconds, %.2f seconds system-wide time %.2f seconds of system time and eventually.\n' % (user, system, user + system)
		rep += u'I release total %s threads, currently active %s threads.' % (INFO['thr'], threading.activeCount())
	else:
		rep = u'Molding...'
	reply(type, source, rep)

def handler_remind(type, source, parameters, recover=False, jid='', rcts='', timerid=''):
	groupchat = source[1]
	nick = source[2]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	global TIMER_ID
	
	if not recover and not jid:
		jid = get_jid(groupchat,nick)
	
	if parameters:
		spltdp = parameters.split(' ',1)
		
		if len(spltdp) == 2 and not '-' in spltdp[0]:
			rtime = spltdp[0]
			rtimes = rtime
			ctm = list(time.localtime())			
			ctms = ctm
			
			if ':' in rtime:
				rtime = rtime.split(':')
				rtime = [li for li in rtime if li != '']
				
				if len(rtime) == 3:
					sc = int(rtime[2])
					mn = int(rtime[1])
					hr = int(rtime[0])
				elif len(rtime) == 2:
					sc = 0
					mn = int(rtime[1])
					hr = int(rtime[0])
				elif len(rtime) == 1:
					sc = 0
					mn = int(rtime[0])
					hr = ctm[3]
					
				if hr:
					ctm[3] = hr
					
				ctm[4] = mn
				ctm[5] = sc
					
				dst = tuple(ctm)
				cts = time.time()
				dts = time.mktime(dst)
				
				secs = int(round(dts - cts))
				
				if abs(secs) <> secs and not recover:
					reply(type, source, u'Overdue reminder!')
					return
			else:
				rtimes = spltdp[0]
				secs = int(rtimes)*60
				cts = time.time()
				dts = cts + secs
			
			mess = spltdp[1]
			
			if secs > 0:
				if not recover:
					reply(type, source, u'Saved!')
				
				if recover:
					cts = float(rcts)
					nick = ''
				
				if not recover:
					timerid = 'timer' + str(random.randrange(10000000, 99999999))
					chk_tmrid = check_timerid(groupchat,timerid)
					
					while not chk_tmrid:
						timerid = 'timer' + str(random.randrange(10000000, 99999999))
						chk_tmrid = check_timerid(groupchat,timerid)
				
				if not recover:
					save_remind(groupchat,nick,jid,rtimes,cts,dts,mess,'run',timerid)	
				
				TIMER_ID[groupchat][timerid] = threading.Timer(secs,rem_timer,[groupchat,cts,dts,nick,jid,mess,timerid])
				TIMER_ID[groupchat][timerid].start()
			else:
				if not recover:
					reply(type, source, u'Too short of time interval!')
		elif len(spltdp) == 1:
			nrem = spltdp[0]
			
			if '-' in nrem:
				nrem = nrem.split('-',1)
				nrem = [li for li in nrem if li != '']
				
				if len(nrem) == 1:
					nrem = nrem[0]
					
					if nrem.isdigit():
						nrem = int(nrem)
					else:
						reply(type, source, u'Invalid syntax!')
						return
					
					reminds = get_reminds(groupchat)
					rems = check_reminds(reminds,jid)
					
					if not rems:
						reply(type, source, u'List of reminders empty!')
						return
					elif nrem > len(rems):
						reply(type, source, u'Wrong number of reminder!')
						return
					
					timerid = rems[nrem-1][7]
					mess = rems[nrem-1][5]
					TIMER_ID[groupchat][timerid].cancel()
					del TIMER_ID[groupchat][timerid]
					res = del_remind(groupchat, jid, mess, timerid)
					
					if res == '':
						rep = u'Error removing!'	
					else:
						rep = u'Number of reminder %s deleted!' % (nrem)
						
					reply(type, source, rep)
				else:
					reminds = get_reminds(groupchat)
					rems = check_reminds(reminds,jid)
					
					if not rems:
						reply(type, source, u'List of reminders empty!')
						return
					
					for nrem in rems:
						timerid = nrem[7]
						mess = nrem[5]
						TIMER_ID[groupchat][timerid].cancel()
						del TIMER_ID[groupchat][timerid]
						del_remind(groupchat, jid, mess, timerid)
						
					rep = u' List of reminders purified!'
					reply(type, source, rep)
			else:
				reply(type, source, u'Invalid syntax!')
		else:
			reply(type, source, u'Invalid syntax!')
	else:
		reminds = get_reminds(groupchat)
		rems = check_reminds(reminds,jid)
		nrepl = show_reminds(groupchat, jid, rems, pref=u' Appointed ', suff=u', left ')		
		
		if nrepl:
			if type == 'public':
				rep = u'Reminders:\n%s' % ('\n\n'.join(nrepl))
				reply(type, source, u'Look in private!')
				reply('private', source, rep)
			else:
				rep = u'Reminders:\n%s' % ('\n\n'.join(nrepl))
				reply(type, source, rep)
		else:
			rep = u'No reminders!'
			reply(type, source, rep)

register_stage1_init(get_info_state)
register_join_handler(handler_user_join)
register_leave_handler(handler_user_leave)
register_presence_handler(handler_user_presence)

register_command_handler(handler_getrealjid, COMM_PREFIX+'realjid', ['info','admin','muc','all','*'], 20, 'Show real JID of indicated nick. Only works if the bot as role admin!', COMM_PREFIX+'realjid <nick>', [COMM_PREFIX+'realjid guy'])
register_command_handler(handler_total_in_muc, COMM_PREFIX+'users', ['info','muc','all','*'], 10, 'Show number of users in the conference.', COMM_PREFIX+'users', [COMM_PREFIX+'users'])
register_command_handler(handler_bot_uptime, COMM_PREFIX+'botup', ['info','admin','all','*'], 10, 'Show how long the bot works without falling.', COMM_PREFIX+'botup', [COMM_PREFIX+'botup'])
register_command_handler(handler_groupchats, COMM_PREFIX+'chatrooms', ['admin','info','all','*'], 20, 'Show where the bot!', COMM_PREFIX+'chatrooms', [COMM_PREFIX+'chatrooms'])
register_command_handler(handler_nicks, COMM_PREFIX+'nicks', ['admin','info','all','*'], 20, 'Show how many nicks, and what was the current conference!', COMM_PREFIX+'nicks', [COMM_PREFIX+'nicks'])
register_command_handler(handler_here, COMM_PREFIX+'here', ['muc','info','all','*'], 10, 'Shows how much time a user spent in the current conference.', COMM_PREFIX+'here [nick]', [COMM_PREFIX+'here guy',COMM_PREFIX+'here'])
register_command_handler(handler_seen, COMM_PREFIX+'seen', ['muc','info','all','*'], 10, 'Show the last time the user has been in the current conference.', COMM_PREFIX+'seen <nick|jid>', [COMM_PREFIX+'seen guy',COMM_PREFIX+'seen guy@jsmart.web.id'])
register_command_handler(handler_members, COMM_PREFIX+'members', ['muc','info','all','*'], 20, 'Show list of JIDs as permanent member in current conference.', COMM_PREFIX+'members', [COMM_PREFIX+'members'])
register_command_handler(handler_admins, COMM_PREFIX+'admins', ['muc','info','all','*'], 20, 'Show list of JIDs as admins in current conference.', COMM_PREFIX+'admins', [COMM_PREFIX+'admins'])
register_command_handler(handler_owners, COMM_PREFIX+'owners', ['muc','info','all','*'], 20, 'Show list of JIDs as owner in current conference.', COMM_PREFIX+'owners', [COMM_PREFIX+'owners'])
register_command_handler(handler_outcasts, COMM_PREFIX+'banned', ['muc','info','all','*'], 20, 'Show list of JIDs as banned in current conference.', COMM_PREFIX+'banned', [COMM_PREFIX+'banned'])
register_command_handler(handler_remind, COMM_PREFIX+'remind', ['muc','info','all','*'], 11, 'Displays a private message reminder, user-defined, after a certain period of time, or at a specified time. Specify in minutes (If you specify an integer), hen set the time interval in which you want to display a reminder, parameter 2 - recall in two minutes, or format: <hh:mm:ss|hh:mm|:mm>,  then set the exact time, when prompts, parameter 22:30 - recall in 22:30, :30 - recall in 30 minutes of this hour. To remove any reminders need to specify the number of reminders from the sign "-" before the number to clear the list of reminders, i.e remove all the reminders you need to specify the sign "-". Without arguments displays a list of appointment reminders.', COMM_PREFIX+'remind [<minutes|hh:mm:ss|hh:mm|:mm|-<number>|->] [<message>]', [COMM_PREFIX+'remind 10 Хватит ждать, пора!',COMM_PREFIX+'remind 22:30:10 Самое время для чая ^^',COMM_PREFIX+'remind 23:30 Так, 23:30, interesting TV programme!',COMM_PREFIX+'remind :20 Already done?',COMM_PREFIX+'remind -2',COMM_PREFIX+'remind -',COMM_PREFIX+'remind'])
register_command_handler(handler_dmess_control, COMM_PREFIX+'dmess', ['muc','info','all','*'], 20, ' Enables or disables the automatic system of deferred messages.', COMM_PREFIX+'dmess [<0>|<1>]', [COMM_PREFIX+'dmess',COMM_PREFIX+'dmess 1',COMM_PREFIX+'dmess 0'])
register_command_handler(handler_tell, COMM_PREFIX+'tell', ['muc','info','all','*'], 11, 'Allows you to leave the user is not located in the conference message, he will receive them the next time.', COMM_PREFIX+'tell <nick>:<message>', [COMM_PREFIX+'tell guy: How do I get this message, knocks on the roster.'])

register_message_handler(handler_dmess)