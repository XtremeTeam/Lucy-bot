#===islucyplugin===
# -*- coding: utf-8 -*-

#  fatal plugin
#  muc_plugin.py

#  Initial Copyright © 2009 wd/lotusfeet <dao/yoga@conference.jabber.ru>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import sqlite3 as db
import re
import time

AKICK_COMP_EXP = {}
AMODER_COMP_EXP = {}
AVISITOR_COMP_EXP = {}
ABAN_COMP_EXP = {}

def querymuc(dbpath,query):
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

def compile_re_patt(gch,amuc):
	qli = show_amuc(gch,amuc)
	qli = [list(li)[0] for li in qli]
	
	if qli != '':
		amucreli = ['^'+li+'$' for li in qli]
		amuc_comp_exp = r'|'.join(amucreli)
		if amuc_comp_exp:
			amuc_comp_exp = re.compile(amuc_comp_exp)
		return amuc_comp_exp
	else:
		return qli

def split_reason(parameters):
	nijirel = parameters.split('|', 1)
	splited = ['','']	
		
	if len(nijirel) == 1:
		splited[0] = nijirel[0].strip()
		splited[1] = ''
	elif len(nijirel) == 2:
		splited[0] = nijirel[0].strip()
		splited[1] = nijirel[1].strip()
	return splited

def muc_set_role(func,type,source,parameters):
	groupchat = source[1]
	
	sparams = split_reason(parameters)
	nick = sparams[0]
	reason = sparams[1]
	
	if check_jid(nick):
		nick = get_nick(groupchat, nick)
	
	if GROUPCHATS[groupchat].has_key(nick):
		if GROUPCHATS[groupchat][nick]['ishere'] == 1:
			resp = func(groupchat,nick,reason)
		
			if func.func_name == 'kick':
				del_banned(groupchat,nick)
				del GROUPCHATS[groupchat][nick]
		
			if resp:
				reply(type, source, u'Done!')
			else:
				reply(type, source, u'Unable to perform the operation!')
	else:
		reply(type, source, u'And then?')

def muc_set_aff(func,type,source,parameters):
	groupchat = source[1]
	
	sparams = split_reason(parameters)
	nick_jid = sparams[0]
	reason = sparams[1]
	
	if GROUPCHATS[groupchat].has_key(nick_jid):
		if GROUPCHATS[groupchat][nick_jid]['ishere'] == 1:
			if func.func_name == 'none' and reason == 'unban':
				reply(type, source, u'Unable to perform the operation!')
				return
			
			resp = func(groupchat,nick_jid,reason)
		
			if func.func_name == 'ban':
				del_banned(groupchat,nick_jid)
				del GROUPCHATS[groupchat][nick_jid]
		
			if resp:
				reply(type, source, u'Done!')
			else:
				reply(type, source, u'Unable to perform the operation!')
		else:
			if func.func_name == 'none' and reason == 'unban':
				reply(type, source, u'Unable to perform the operation!')
				return
			
			jid = GROUPCHATS[groupchat][nick_jid]['jid'].split('/')[0]
			resp = func(groupchat,jid,reason)
			
			if func.func_name == 'ban':
				del_banned(groupchat,nick_jid)
				del GROUPCHATS[groupchat][nick_jid]
			
			if resp:
				reply(type, source, u'Done!')
			else:
				reply(type, source, u'Unable to perform the operation!')
	elif not check_jid(nick_jid):
		if func.func_name == 'none' and reason == 'unban':
			reply(type, source, u'Unable to perform the operation!')
			return
		
		jid = get_jid(groupchat, nick_jid)
		
		if jid:
			resp = func(groupchat,jid,reason)
			
			if func.func_name == 'ban':
				del_banned(groupchat,nick_jid)
			
			if resp:
				reply(type, source, u'Done!')
			else:
				reply(type, source, u'Unable to perform the operation!')
		else:
			reply(type, source, u'And, then??')
				
	else:
		resp = func(groupchat,nick_jid,reason)
			
		if resp:
			reply(type, source, u'Done!')
		else:
			reply(type, source, u'Unable to perform the operation!')

def del_banned(gch, nick):
	if not nick:
		nick = ''
	
	nick = nick.replace('"','&quot;')
	sql = 'DELETE FROM users WHERE nick="%s";' % (nick)
	qres = querymuc('settings/'+gch+'/users.db',sql)
	
	if qres == []:
		return True

def get_join_nick(gch, jid):
	nick = ''
	
	nickl = [li for li in GROUPCHATS[gch] if jid in GROUPCHATS[gch][li]['jid'] and GROUPCHATS[gch][li]['ishere'] == 1]
	
	if nickl:
		nick = nickl[-1]
		
	return nick		
		
def get_nick(gch, jid):
	jid = jid.replace('"','&quot;')
	sql = 'SELECT nick FROM users WHERE jid="%s" ORDER BY ujoin;' % (jid)
	qres = querymuc('settings/'+gch+'/users.db',sql)
	
	if qres:
		nick = qres[-1][0]
		return nick

def get_jid(gch, nick):
	nick = nick.replace('"','&quot;')
	sql = 'SELECT jid FROM users WHERE nick="%s";' % (nick)
	qres = querymuc('settings/'+gch+'/users.db',sql)
	
	if qres:
		jid = qres[0][0]
		return jid

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

def set_subject(groupchat, subject):
	msg = xmpp.Message(groupchat)
	msg.setType('groupchat')
	msg.setTagData('subject',subject)
	resp = JCON.send(msg)
	
	if resp:
		return True

def kick(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace(xmpp.NS_MUC_ADMIN)
	kick=query.addChild('item', {'nick':nick, 'role':'none'})	
	kick.setTagData('reason', reason)
	iq.addChild(node=query)
	resp = JCON.send(iq)
	
	if iq.getID() == resp:
		return True

def ban(groupchat, nick_jid, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('ban'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace(xmpp.NS_MUC_ADMIN)
	
	if check_jid(nick_jid):
		ban=query.addChild('item', {'jid':nick_jid, 'affiliation':'outcast'})		
	else:
		ban=query.addChild('item', {'nick':nick_jid, 'affiliation':'outcast'})
	
	ban.setTagData('reason', reason)
	iq.addChild(node=query)
	resp = JCON.send(iq)
	
	if iq.getID() == resp:
		return True

def none(groupchat, nick_jid,reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('none'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace(xmpp.NS_MUC_ADMIN)
	
	if check_jid(nick_jid):
		none=query.addChild('item', {'jid':nick_jid, 'affiliation':'none'})
	else:
		none=query.addChild('item', {'nick':nick_jid, 'affiliation':'none'})
	
	iq.addChild(node=query)
	resp = JCON.send(iq)
	
	if iq.getID() == resp:
		return True

def visitor(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('voice'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace(xmpp.NS_MUC_ADMIN)
	visitor=query.addChild('item', {'nick':nick, 'role':'visitor'})
	iq.addChild(node=query)
	resp = JCON.send(iq)
	
	if iq.getID() == resp:
		return True

def participant(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('part'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace(xmpp.NS_MUC_ADMIN)
	participant=query.addChild('item', {'nick':nick, 'role':'participant'})
	iq.addChild(node=query)
	resp = JCON.send(iq)
	
	if iq.getID() == resp:
		return True
	
def member(groupchat, nick_jid, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('member'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace(xmpp.NS_MUC_ADMIN)
	
	if check_jid(nick_jid):
		member=query.addChild('item', {'jid':nick_jid, 'affiliation':'member'})
	else:
		member=query.addChild('item', {'nick':nick_jid, 'affiliation':'member'})
	
	member.setTagData('reason', reason)
	iq.addChild(node=query)
	resp = JCON.send(iq)
	
	if iq.getID() == resp:
		return True	
	
def moderator(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('moder'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace(xmpp.NS_MUC_ADMIN)
	moderator=query.addChild('item', {'nick':nick, 'role':'moderator'})
	iq.addChild(node=query)
	resp = JCON.send(iq)
	
	if iq.getID() == resp:
		return True	

def admin(groupchat, nick_jid, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('admin'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace(xmpp.NS_MUC_ADMIN)
	
	if check_jid(nick_jid):
		admin=query.addChild('item', {'jid':nick_jid, 'affiliation':'admin'})
	else:
		admin=query.addChild('item', {'nick':nick_jid, 'affiliation':'admin'})
	
	admin.setTagData('reason', reason)
	iq.addChild(node=query)
	resp = JCON.send(iq)
	
	if iq.getID() == resp:
		return True	
	
def owner(groupchat, nick_jid, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('owner'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace(xmpp.NS_MUC_ADMIN)
	
	if check_jid(nick_jid):
		owner=query.addChild('item', {'jid':nick_jid, 'affiliation':'owner'})
	else:
		owner=query.addChild('item', {'nick':nick_jid, 'affiliation':'owner'})
	
	owner.setTagData('reason', reason)
	iq.addChild(node=query)
	resp = JCON.send(iq)
	
	if iq.getID() == resp:
		return True	

def save_amuc(gch,amuc,exp,reason=''):
	exp = exp.replace(r'"', r'&quot;')
	reason = reason.replace(r'"', r'&quot;')
	
	if amuc == 'akick' or amuc == 'aban':
		sql = 'INSERT INTO %s (exp,reason) VALUES ("%s","%s");' % (amuc,exp.strip(),reason.strip())
	else:
		sql = 'INSERT INTO %s (exp) VALUES ("%s");' % (amuc,exp.strip())
	
	rep = querymuc('settings/'+gch+'/amuc.db',sql)
	return rep
	
def show_amuc(gch,amuc):
	if amuc == 'akick' or amuc == 'aban':
		sql = 'SELECT exp,reason FROM %s;' % (amuc)
	else:
		sql = 'SELECT exp FROM %s;' % (amuc)
	
	rep = querymuc('settings/'+gch+'/amuc.db',sql)
	return rep

def del_amuc(gch,amuc,amucre):
	sql = 'DELETE FROM %s WHERE exp="%s";' % (amuc,amucre)
	rep = querymuc('settings/'+gch+'/amuc.db',sql)
	return rep

def clear_amuc(gch,amuc):
	sql = 'DELETE FROM '+amuc+';'
	rep = querymuc('settings/'+gch+'/amuc.db',sql)
	return rep

def set_amuc(gch,amfunc,cpatt,nick,jid):
	amucnifi = []
	
	if cpatt:
		amucnifi = cpatt.findall(nick)
		
	if amucnifi:
		if amfunc.func_name != 'moderator' and user_level(gch+'/'+nick,gch) <= 10:
			amfunc(gch, amucnifi[-1], '')
			return
		elif amfunc.func_name == 'moderator':
			amfunc(gch, amucnifi[-1], '')
			return
		
	amucjifi = []
		
	if cpatt:	
		amucjifi = cpatt.findall(jid)
	
	if amucjifi:
		if amfunc.func_name != 'ban': 
			nick = get_join_nick(gch, amucjifi[-1])
			
			if nick:
				if amfunc.func_name != 'moderator' and user_level(gch+'/'+nick,gch) <= 10:
					amfunc(gch, nick, '')
					return
				elif amfunc.func_name == 'moderator':
					amfunc(gch, nick, '')
					return
		else:
			if user_level(gch+'/'+nick,gch) <= 10:
				amfunc(gch, jid, '')
				del GROUPCHATS[groupchat][nick]

def handler_amuc_join(groupchat, nick, aff, role):
	jid = get_true_jid(groupchat+'/'+nick)
		
	if AMODER_COMP_EXP[groupchat]:
		set_amuc(groupchat,moderator,AMODER_COMP_EXP[groupchat],nick,jid)
	
	if AVISITOR_COMP_EXP[groupchat] and aff == 'none':
		set_amuc(groupchat,visitor,AVISITOR_COMP_EXP[groupchat],nick,jid)
	
	if AKICK_COMP_EXP[groupchat] and aff == 'none':
		set_amuc(groupchat,kick,AKICK_COMP_EXP[groupchat],nick,jid)
	
	if ABAN_COMP_EXP[groupchat] and aff == 'none':
		set_amuc(groupchat,ban,ABAN_COMP_EXP[groupchat],nick,jid)
	
def handler_amuc_presence(prs):
	ptype = prs.getType()
	groupchat = prs.getFrom().getStripped()
	nick = prs.getFrom().getResource()
	jid=get_true_jid(groupchat+'/'+nick)
	scode = prs.getStatusCode()

	if scode == '303' and ptype == 'unavailable':
		newnick = prs.getNick()
		
		if AMODER_COMP_EXP[groupchat]:
			set_amuc(groupchat,moderator,AMODER_COMP_EXP[groupchat],newnick,jid)
		
		if AVISITOR_COMP_EXP[groupchat]:
			set_amuc(groupchat,visitor,AVISITOR_COMP_EXP[groupchat],newnick,jid)
		
		if AKICK_COMP_EXP[groupchat]:
			set_amuc(groupchat,kick,AKICK_COMP_EXP[groupchat],newnick,jid)
		
		if ABAN_COMP_EXP[groupchat]:
			set_amuc(groupchat,ban,ABAN_COMP_EXP[groupchat],newnick,jid)
	
def get_amuc_state(gch):
	global AKICK_COMP_EXP
	global AMODER_COMP_EXP
	global AVISITOR_COMP_EXP
	global ABAN_COMP_EXP
	
	if not AKICK_COMP_EXP.has_key(gch):
		AKICK_COMP_EXP[gch] = ''
	if not AMODER_COMP_EXP.has_key(gch):
		AMODER_COMP_EXP[gch] = ''
	if not AVISITOR_COMP_EXP.has_key(gch):
		AVISITOR_COMP_EXP[gch] = ''
	if not ABAN_COMP_EXP.has_key(gch):
		ABAN_COMP_EXP[gch] = ''
	
	if not os.path.exists('settings/'+gch+'/amuc.db'):
		sql = 'CREATE TABLE avisitor(id integer primary key autoincrement, exp varchar,unique (exp))'
		querymuc('settings/'+gch+'/amuc.db',sql)
		sql = 'CREATE TABLE akick(id integer primary key autoincrement, exp varchar, reason varchar, unique (exp))'
		querymuc('settings/'+gch+'/amuc.db',sql)
		sql = 'CREATE TABLE amoderator(id integer primary key autoincrement, exp varchar, unique (exp))'
		querymuc('settings/'+gch+'/amuc.db',sql)
		sql = 'CREATE TABLE aban(id integer primary key autoincrement, exp varchar, reason varchar, unique (exp))'
		querymuc('settings/'+gch+'/amuc.db',sql)
	else:
		AKICK_COMP_EXP[gch] = compile_re_patt(gch,'akick')
		AMODER_COMP_EXP[gch] = compile_re_patt(gch,'amoderator')
		AVISITOR_COMP_EXP[gch] = compile_re_patt(gch,'avisitor')
		ABAN_COMP_EXP[gch] = compile_re_patt(gch,'aban')

def handler_akick(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	global AKICK_COMP_EXP
	
	spltd = split_reason(parameters)
	exp = spltd[0]
	reason = spltd[1]
	
	if parameters and not parameters[1:].isdigit() and len(parameters) != 1:
		res = save_amuc(groupchat,'akick',exp,reason)
		
		if res != '':
			reply(type,source,u'Rule added!')
			AKICK_COMP_EXP[groupchat] = compile_re_patt(groupchat,'akick')
			
			nicks = [li for li in GROUPCHATS[groupchat] if GROUPCHATS[groupchat][li]['ishere'] == 1]
			jids = [GROUPCHATS[groupchat][li]['jid'].split('/')[0] for li in GROUPCHATS[groupchat] if GROUPCHATS[groupchat][li]['ishere'] == 1]
						
			I = 0			
						
			while I != len(nicks):
				set_amuc(groupchat,kick,AKICK_COMP_EXP[groupchat],nicks[I],jids[I])
				I += 1
		else:
			reply(type,source,u'Error adding rule!')
	elif parameters and parameters[1:].isdigit() and parameters[0] == '-':
		parameters = parameters[1:]
		akreli = show_amuc(groupchat,'akick')
		renum = int(parameters)
		
		if renum > len(akreli) or renum <= 0:
			reply(type,source,u' Wrong number of rules!')
			return
		
		amucre = akreli[renum-1][0]
		dres = del_amuc(groupchat,'akick',amucre)
		
		if dres != '':
			reply(type,source,u'The rule is removed from the list!')
			AKICK_COMP_EXP[groupchat] = compile_re_patt(groupchat,'akick')
		else:
			reply(type,source,u'Deleted!')
	elif parameters and '-' in parameters and len(parameters) == 1:
		qres = clear_amuc(groupchat,'akick')
		
		if qres != '':
			rep = u'List of rules autokick is purified!'
			AKICK_COMP_EXP[groupchat] = r''
		else:
			rep = u'Unable to clear the list  of akick!'
		
		reply(type,source,rep)
	else:
		akreli = show_amuc(groupchat,'akick')
		rng = range(len(akreli))
		nakreli = ['%s) %s' % (li+1, akreli[li][0]) for li in rng]
		
		if akreli:
			rep = u'List of rules akick (total: ' + str(len(nakreli))+ '):\n' + '\n'.join(nakreli)
		else:
			rep = u'List of rules akick is empty!'
			
		if type == 'public':	
			reply(type,source, u'Look in private!')
			
		reply('private',source,rep)

def handler_amoderator(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	global AMODER_COMP_EXP
	
	spltd = split_reason(parameters)
	exp = spltd[0]
	reason = spltd[1]
	
	if parameters and not parameters[1:].isdigit() and len(parameters) != 1:
		res = save_amuc(groupchat,'amoderator',exp)
		
		if res != '':
			reply(type,source,u'Rule added!')
			AMODER_COMP_EXP[groupchat] = compile_re_patt(groupchat,'amoderator')
			
			nicks = [li for li in GROUPCHATS[groupchat] if GROUPCHATS[groupchat][li]['ishere'] == 1]
			jids = [GROUPCHATS[groupchat][li]['jid'].split('/')[0] for li in GROUPCHATS[groupchat] if GROUPCHATS[groupchat][li]['ishere'] == 1]
						
			I = 0			
						
			while I != len(nicks):
				set_amuc(groupchat,moderator,AMODER_COMP_EXP[groupchat],nicks[I],jids[I])
				I += 1
		else:
			reply(type,source,u'Error adding rule!')
	elif parameters and parameters[1:].isdigit() and parameters[0] == '-':
		parameters = parameters[1:]
		amreli = show_amuc(groupchat,'amoderator')
		renum = int(parameters)
		
		if renum > len(amreli) or renum <= 0:
			reply(type,source,u'Wrong number of rules!')
			return
		
		amucre = amreli[renum-1][0]
		dres = del_amuc(groupchat,'amoderator',amucre)
		
		if dres != '':
			reply(type,source,u'The rule is removed from the list!')
			AMODER_COMP_EXP[groupchat] = compile_re_patt(groupchat,'amoderator')
		else:
			reply(type,source,u'Deleted!')
	elif parameters and '-' in parameters and len(parameters) == 1:
		qres = clear_amuc(groupchat,'amoderator')
		
		if qres != '':
			rep = u'List of rules amoderetor is purified!'
			AMODER_COMP_EXP[groupchat] = r''
		else:
			rep = u'Unable to clear the list amoderetor!'
		
		reply(type,source,rep)
	else:
		amreli = show_amuc(groupchat,'amoderator')
		rng = range(len(amreli))
		namreli = ['%s) %s' % (li+1, amreli[li][0]) for li in rng]
		
		if amreli:
			rep = u'List of rules amoderator (total: ' + str(len(namreli))+ '):\n' + '\n'.join(namreli)
		else:
			rep = u'List of rules amoderator is empty!'	
		
		if type == 'public':	
			reply(type,source, u'Look in private!')
			
		reply('private',source,rep)

def handler_avisitor(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	global AVISITOR_COMP_EXP
	
	spltd = split_reason(parameters)
	exp = spltd[0]
	reason = spltd[1]
	
	if parameters and not parameters[1:].isdigit() and len(parameters) != 1:
		res = save_amuc(groupchat,'avisitor',exp)
		
		if res != '':
			reply(type,source,u'Rule added!')
			AVISITOR_COMP_EXP[groupchat] = compile_re_patt(groupchat,'avisitor')
			
			nicks = [li for li in GROUPCHATS[groupchat] if GROUPCHATS[groupchat][li]['ishere'] == 1]
			jids = [GROUPCHATS[groupchat][li]['jid'].split('/')[0] for li in GROUPCHATS[groupchat] if GROUPCHATS[groupchat][li]['ishere'] == 1]
						
			I = 0			
						
			while I != len(nicks):
				set_amuc(groupchat,visitor,AVISITOR_COMP_EXP[groupchat],nicks[I],jids[I])
				I += 1
		else:
			reply(type,source,u'Error adding rule!')
	elif parameters and parameters[1:].isdigit() and parameters[0] == '-':
		parameters = parameters[1:]
		avreli = show_amuc(groupchat,'avisitor')
		renum = int(parameters)
		
		if renum > len(avreli) or renum <= 0:
			reply(type,source,u'Wrong number of rules!')
			return
		
		amucre = avreli[renum-1][0]
		dres = del_amuc(groupchat,'avisitor',amucre)
		
		if dres != '':
			reply(type,source,u'The rule is removed from the list!')
			AVISITOR_COMP_EXP[groupchat] = compile_re_patt(groupchat,'avisitor')
		else:
			reply(type,source,u'Deleted!')
	elif parameters and '-' in parameters and len(parameters) == 1:
		qres = clear_amuc(groupchat,'avisitor')
		
		if qres != '':
			rep = u'List of rules avisitor is purified!'
			AVISITOR_COMP_EXP[groupchat] = r''
		else:
			rep = u'Unable to clear the list avisitor!'
		
		reply(type,source,rep)
	else:
		avreli = show_amuc(groupchat,'avisitor')
		rng = range(len(avreli))
		navreli = ['%s) %s' % (li+1, avreli[li][0]) for li in rng]
		
		if avreli:
			rep = u'List of rules avisitor (total: ' + str(len(navreli))+ '):\n' + '\n'.join(navreli)
		else:
			rep = u'List of rules avisitor is empty empty!'	
		
		if type == 'public':	
			reply(type,source, u'Look in private!')
			
		reply('private',source,rep)

def handler_aban(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	global ABAN_COMP_EXP
	
	spltd = split_reason(parameters)
	exp = spltd[0]
	reason = spltd[1]
	
	if parameters and not parameters[1:].isdigit() and len(parameters) != 1:
		res = save_amuc(groupchat,'aban',exp,reason)
		
		if res != '':
			reply(type,source,u'Rule added!')
			ABAN_COMP_EXP[groupchat] = compile_re_patt(groupchat,'aban')
			
			nicks = [li for li in GROUPCHATS[groupchat] if GROUPCHATS[groupchat][li]['ishere'] == 1]
			jids = [GROUPCHATS[groupchat][li]['jid'].split('/')[0] for li in GROUPCHATS[groupchat] if GROUPCHATS[groupchat][li]['ishere'] == 1]
						
			I = 0			
						
			while I != len(nicks):
				set_amuc(groupchat,ban,ABAN_COMP_EXP[groupchat],nicks[I],jids[I])
				I += 1
		else:
			reply(type,source,u'Deleted!')
	elif parameters and parameters[1:].isdigit() and parameters[0] == '-':
		parameters = parameters[1:]
		abreli = show_amuc(groupchat,'aban')
		renum = int(parameters)
		
		if renum > len(abreli) or renum <= 0:
			reply(type,source,u'Wrong number of rules!')
			return
		
		amucre = abreli[renum-1][0]
		dres = del_amuc(groupchat,'aban',amucre)
		
		if dres != '':
			reply(type,source,u'The rule is removed from the list!')
			ABAN_COMP_EXP[groupchat] = compile_re_patt(groupchat,'aban')
		else:
			reply(type,source,u'Deleted!')
	elif parameters and '-' in parameters and len(parameters) == 1:
		qres = clear_amuc(groupchat,'aban')
		
		if qres != '':
			rep = u'Unable to clear the list of avisitor!'
			ABAN_COMP_EXP[groupchat] = r''
		else:
			rep = u'List of avisitor cleared!'
		
		reply(type,source,rep)
	else:
		abreli = show_amuc(groupchat,'aban')
		rng = range(len(abreli))
		nabreli = ['%s) %s' % (li+1, abreli[li][0]) for li in rng]
		
		if abreli:
			rep = u'List of rules aban (total: ' + str(len(nabreli))+ '):\n' + '\n'.join(nabreli)
		else:
			rep = u'A list of rules is empty!'	
		
		if type == 'public':	
			reply(type,source, u'Look in private!')
			
		reply('private',source,rep)

def handler_set_subject(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	if parameters:
		resp = set_subject(groupchat, parameters)
		
		if resp:
			reply(type, source, u'Done!')
		else:
			reply(type, source, u'Unable to change theme!')
	else:
		reply(type, source, u'And, then?')
	
def handler_kick(type, source, parameters):
	groupchat=source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	if parameters:
		muc_set_role(kick,type,source,parameters)
	else:
		reply(type, source, u'And, who?')
	
def handler_ban(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	if parameters:
		muc_set_aff(ban,type,source,parameters)	
	else:
		reply(type, source, u'And, who?')
	
def handler_none(type, source, parameters):
	groupchat=source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	if parameters:
		muc_set_aff(none,type,source,parameters)
	else:
		reply(type, source, u'And, who?')
	
def handler_member(type, source, parameters):
	groupchat=source[1]

	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return

	if parameters:
		muc_set_aff(member,type,source,parameters)
	else: 
		reply(type, source, u'And, who?')
	
def handler_admin(type, source, parameters):
	groupchat=source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	if parameters:
		muc_set_aff(admin,type,source,parameters)
	else: 
		reply(type, source, u'And, who?')
	
def handler_owner(type, source, parameters):
	groupchat=source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	if parameters:
		muc_set_aff(owner,type,source,parameters)
	else: 
		reply(type, source, u'And, who?')

def handler_moderator(type, source, parameters):
	groupchat=source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	if parameters:
		muc_set_role(moderator,type,source,parameters)
	else: 
		reply(type, source, u'And, who?')

def handler_visitor(type, source, parameters):
	groupchat=source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	if parameters:
		muc_set_role(visitor,type,source,parameters)
	else: 
		reply(type, source, u'And, who?')
	
def handler_participant(type, source, parameters):
	groupchat=source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	if parameters:
		muc_set_role(participant,type,source,parameters)
	else: 
		reply(type, source, u'And, who?')
	
def handler_unban(type, source, parameters):
	groupchat=source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	if parameters:
		muc_set_aff(none,type,source,parameters + '|unban')
	else:
		reply(type, source, u'And, who?')
	
register_command_handler(handler_kick, 'kick', ['admin','all','*','muc'], 16, 'Kick a user!', 'kick <nick[|reason]>', ['kick guy', 'kick guy|Первый пошел!'])
register_command_handler(handler_ban, 'ban', ['admin','all','*','muc'], 20, 'Banned a nick or jid!', 'ban <nick|jid[|reason]>', ['ban guy', 'ban guy|Пшел отседова!', 'ban guy@jsmart.web.id', 'ban guy@jsmart.web.id|Свободен!'])
register_command_handler(handler_visitor, 'visitor', ['admin','all','*','muc'], 16, 'Refuse a user right to speak!', 'visitor <nick>', ['visitor guy'])
register_command_handler(handler_participant, 'participant', ['admin','all','*','muc'], 16, 'Returns the position taken by the participant in the original condition, ie participant!!', 'participant <nick>', ['participant guy'])
register_command_handler(handler_unban, 'unban', ['admin','all','*','muc'], 20, 'Release an asshole JID out from quarantine!', 'unban <jid>', ['unban guy@jsmart.web.id!'])
register_command_handler(handler_none, 'none', ['admin','all','*','muc'], 20, 'Change a user position to the lowest role!', 'none <nick>', ['none guy'])
register_command_handler(handler_member, 'member', ['admin','all','*','muc'], 20, 'Change a user position to a permanent member!', 'member <nick[|reason]>', ['member guy', 'member guy|Congratulation, be a good member!'])
register_command_handler(handler_moderator, 'moderator', ['admin','all','*','muc'], 20, 'Increase the position of participant or member, ie to make the interim moderator!', 'moderator <nick>', ['moderator guy'])
register_command_handler(handler_admin, 'admin', ['superadmin','all','*','muc'], 30, 'Change a user position to admin of conference and permanent moderator!', 'admin <nick [|reason]>', ['admin guy', 'admin guy|Congratulation, now you are admin!'])
register_command_handler(handler_owner, 'owner', ['superadmin','all','*','muc'], 30, 'Change a user position to Owner of conference and permanent moderator!', 'owner <nick[|reason]>', ['owner guy', 'owner guy|Congratulation, now you are owner!'])
register_command_handler(handler_set_subject, 'set_subject', ['admin','all','*','muc'], 16, 'Sets the subject (topic) in the conference!', 'set_subject <subject>', ['set_subject Welcome!'])
register_command_handler(handler_akick, 'akick', ['admin','all','*','amuc'], 20, 'Adds a rule to the list autokick, can be any word or regular expression. without parameters shows list of rules. When you specify a negative number removes the rule number after the "-" from the list of rules. When you specify "-" without number clears the list of rules.', 'akick <word|regexp> [|reason]', [r'akick .*@jabber\.ru',r'akick guy',r'akick .*@jabber\..* | you are not welcome here!',r'akick -3',r'akick -',r'akick'])
register_command_handler(handler_amoderator, 'amoderator', ['admin','all','*','amuc'], 20, 'Adds a rule to the list automoderator, can be any word or regular expression. Without arguments displays list of rules. When you specify a negative number removes the rule with the number after "-" from the list of rules. When you specify "-" without a number of clears the list of rules.', 'amoderator <word|regexp>', [r'amoderator .*@jabber\.ru',r'amoderator guy',r'amoderator -3',r'amoderator -',r'amoderator'])
register_command_handler(handler_avisitor, 'avisitor', ['admin','all','*','amuc'], 20, 'Adds a rule to the list avisitor, can be any word or regular expression. without parameters shows list of rules. When you specify "-" without a number of clears the list of rules. When you specify a negative number removes the rule with the number after "-" from the list of rules.', 'avisitor <word|regexp>', [r'avisitor .*@jabber\.ru',r'avisitor guy',r'avisitor -3',r'avisitor -',r'avisitor'])
register_command_handler(handler_aban, 'aban', ['admin','all','*','amuc'], 20, 'Adds a rule to the list of aban, can be any word as well as regular expression. Without arguments displays list of rules. When you specify a negative number removes the rule with the number after "-" from the list of rules. When you specify "-" without a number of clears the list of rules.', 'aban <word|regexp>', [r'aban .*@jabber\.ru',r'aban guy',r'aban guy | you are not welcome here!',r'aban -3',r'aban -',r'aban'])

register_stage1_init(get_amuc_state)
register_join_handler(handler_amuc_join)
register_presence_handler(handler_amuc_presence)