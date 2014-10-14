#===islucyplugin===
# -*- coding: utf-8 -*-

#  fatal plugin
#  wtf_plugin.py

#  Copyright © 1998-2009 wd/lotusfeet <dao/yoga>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import sqlite3 as db
import os, time

DEFLIMIT = 2000
LISTLIMIT = 50

def querywtf(dbpath,query):
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

def wr_op_file(path, data):
	data = data.encode('cp1251')
	write_file(path, data)
	fp = open(path)
	return fp

def si_request(frm,fjid,sid,name,size,entity=''):
	iq = xmpp.Protocol(name = 'iq', to = fjid,
		typ = 'set')
	ID = 'si'+str(random.randrange(1000, 9999))
	iq.setID(ID)
	si = iq.setTag('si')
	si.setNamespace(xmpp.NS_SI)
	si.setAttr('profile', xmpp.NS_FILE)
	si.setAttr('id', sid)
	file_tag = si.setTag('file')
	file_tag.setNamespace(xmpp.NS_FILE)
	file_tag.setAttr('name', name)
	file_tag.setAttr('size', size)
	desc = file_tag.setTag('desc')
	desc.setData(u'Article "%s" from the base dictionary.' % (entity))
	file_tag.setTag('range')
	feature = si.setTag('feature')
	feature.setNamespace(xmpp.NS_FEATURE)
	_feature = xmpp.DataForm(typ='form')
	feature.addChild(node=_feature)
	field = _feature.setField('stream-method')
	field.setAttr('type', 'list-single')
	field.addOption(xmpp.NS_IBB)
	field.addOption('jabber:iq:oob')
	return iq

def check_reader_id(gch,reader_id):
	sql = 'SELECT * FROM readers WHERE rid="%s";' % (reader_id)
	qres = querywtf('settings/'+gch+'/readers.db',sql)
	
	if qres:
		return False
	else:
		return True	

def check_entity(gch,entity):
	sql = 'SELECT entity FROM defs WHERE entity="%s";' % (entity)
	qres = querywtf('settings/'+gch+'/def.db',sql)
	
	if qres:
		return True
	else:
		return False

def chk_rdr_ent(gch,entity,reader_id):
	sql = 'SELECT entity FROM %s WHERE entity="%s";' % (reader_id,entity)
	qres = querywtf('settings/'+gch+'/readers.db',sql)
	
	if qres:
		return True
	else:
		return False

def clear_nex(gch,all_wtf,reader_id):
	if all_wtf:
		nex_wtf = [nexwli for nexwli in all_wtf if not check_entity(gch,nexwli[0])]
		
		if nex_wtf:
			for nxi in nex_wtf:
				del_exp_wtf(gch,nxi[0],reader_id)
				all_wtf.remove(nxi)
	return all_wtf
		
def get_ent_count(gch):
	sql = 'SELECT entity FROM defs;'
	qres = querywtf('settings/'+gch+'/def.db',sql)
	
	return len(qres)
		
def get_last_wtf(gch,reader_id):
	sql = 'SELECT * FROM %s ORDER BY last DESC;' % (reader_id)
	qres = querywtf('settings/'+gch+'/readers.db',sql)
	
	qres = clear_nex(gch,qres,reader_id)
	
	if qres:
		return qres[0]
	else:
		return ''

def clr_rdr_blist(gch,reader_id):
	sql = 'DROP TABLE %s;' % (reader_id)
	qres = querywtf('settings/'+gch+'/readers.db',sql)
	
	return qres

def del_exp_wtf(gch,entity,reader_id):
	sql = 'DELETE FROM %s WHERE entity="%s";' % (reader_id,entity)
	qres = querywtf('settings/'+gch+'/readers.db',sql)
	
	return qres

def get_opened(gch,reader_id):
	sql = 'SELECT * FROM %s ORDER BY last DESC;' % (reader_id)
	qres = querywtf('settings/'+gch+'/readers.db',sql)
	
	qres = clear_nex(gch,qres,reader_id)
	
	if qres:
		return qres
	else:
		return ''

def show_opened(gch,opli):
	nopli = []
	
	if opli:
		nopli = [u'%s) %s, page: %s of %s (зн/с: %s)' % (opli.index(oli)+1,oli[0],oli[1],oli[3],oli[2]) for oli in opli if oli[1] != oli[3]]
		return nopli
	else:
		return ''
		
def get_rdr_wtf(gch,reader_id,entity):
	sql = 'SELECT * FROM %s WHERE entity="%s";' % (reader_id,entity)
	qres = querywtf('settings/'+gch+'/readers.db',sql)
	
	if qres:
		return qres[0]
	else:
		return ''

def get_reader_id(gch,jid):
	sql = 'SELECT rid FROM readers WHERE jid="%s";' % (jid)
	reader_id = querywtf('settings/'+gch+'/readers.db',sql)
	
	if reader_id:
		return reader_id[0][0]
	else:
		return ''

def save_pos(gch,jid,entity,last,part,spart,qop,reader_id=''):
	if not reader_id:
		reader_id = 'reader'+str(random.randrange(10000000, 99999999))
		chk_rid = check_reader_id(gch,reader_id)
		
		while not chk_rid:
			reader_id = 'reader'+str(random.randrange(10000000, 99999999))
			chk_rid = check_reader_id(gch,reader_id)
		
		sql = 'INSERT INTO readers (jid,rid) VALUES ("%s","%s");' % (jid,reader_id)
		res = querywtf('settings/'+gch+'/readers.db',sql)
	
		sql = 'CREATE TABLE %s (entity varchar not null, part varchar not null, spart varchar not null, qop varchar not null, last varchar not null,unique (entity))' % (reader_id)
		res = querywtf('settings/'+gch+'/readers.db',sql)
	
	sql = 'INSERT INTO %s (entity,part,spart,qop,last) VALUES ("%s","%s","%s","%s","%s");' % (reader_id,entity,part,spart,qop,last)
	res = querywtf('settings/'+gch+'/readers.db',sql)
	
	if res == '':
		upd_sql = 'UPDATE %s SET "part"="%s", "spart"="%s", "qop"="%s", "last"="%s" WHERE entity="%s";' % (reader_id,part,spart,qop,last,entity)
		res = querywtf('settings/'+gch+'/readers.db',upd_sql)
	
	if res == '':
		sql = 'CREATE TABLE %s (entity varchar not null, part varchar not null, spart varchar not null, qop varchar not null, last varchar not null,unique (entity))' % (reader_id)
		res = querywtf('settings/'+gch+'/readers.db',sql)
		
		sql = 'INSERT INTO %s (entity,part,spart,qop,last) VALUES ("%s","%s","%s","%s","%s");' % (reader_id,entity,part,spart,qop,last)
		res = querywtf('settings/'+gch+'/readers.db',sql)

	return res
		
def get_part_list(entli,part,quantity):
	if not entli:
		return entli
	
	qtt = len(entli)
	
	if qtt <= quantity:
		qofparts = 1
		quantity = qtt
	else:
		qofparts = qtt/quantity
		isadparts = qtt%quantity
		 
		if isadparts:
			qofparts += 1
			
	if part > qofparts:
		part = qofparts
	
	startind = part * quantity - quantity
	endind = part * quantity
	
	prtli = entli[startind:endind]
	
	return (prtli,part,quantity,qofparts,startind)		
		
def get_ent_list(gch):
	sql = 'SELECT entity FROM defs ORDER BY entity;'
	qres=querywtf('settings/'+gch+'/def.db',sql)
	
	if qres:
		qres = [li[0] for li in qres]
		return qres
	else:
		return ''
		
def get_book_list(gch):
	sql = u'SELECT entity FROM defs WHERE author="book" ORDER BY entity;'
	qres=querywtf('settings/'+gch+'/def.db',sql)
	
	if qres:
		qres = [li[0] for li in qres]
		return qres
	else:
		return ''
		
def get_part(gdef,part,spart=DEFLIMIT):
	if not gdef:
		return gdef
	
	gdef = gdef.encode('utf-8')
	
	qtt = len(gdef)
	
	if qtt <= spart:
		qofparts = 1
		spart = qtt
	else:
		qofparts = qtt/spart
		isadparts = qtt%spart
		 
		if isadparts:
			qofparts += 1
			
	if part > qofparts:
		part = qofparts
	
	startind = part * spart - spart
	endind = part * spart
	
	if part == 1 and qofparts != part:
		endind = gdef.find(' ',endind)
	elif part == 1 and qofparts == part:
		endind = qtt
	elif part == qofparts:
		startind = gdef.find(' ',startind)
		endind = qtt
	else:
		startind = gdef.find(' ',startind)
		endind = gdef.find(' ',endind)
	
	opart = gdef[startind:endind]
	opart = opart.decode('utf-8')
	
	if len(opart) < spart:
		spart = len(opart)	
	
	return (opart.strip(),part,spart,qofparts,startind)

def add_def(gch,entity,gdef,author=''):
#-----------------------Local Functions--------------
	
	def filter_ent(entity):
		for I in ['"','!','?','~','`','@','#','$','%','^','&','*','(',')','-','=','+','[',']','{','}','|','\\','/',';',':','\'','<','>','.']:
			entity = entity.replace(I,'')
		
		return entity.lower()
		
	def load_def(path):
		try:
			fp = open(path)
			fgdef = fp.read()
			fp.close
			return fgdef
		except:
			return ''
		
#-----------------------End Of Local Functions--------------
	
	if len(gdef) <= 255:
		if os.path.exists(gdef):
			tmp_gdef = load_def(gdef.strip())
			
			if tmp_gdef.strip():
				gdef = tmp_gdef.decode('utf-8')
	
	entity = filter_ent(entity)
	gdef = gdef.replace('"','&quot;')
	author = author.replace('"','&quot;')
	
	action = ''
	
	if not check_entity(gch,entity):
		sql = 'INSERT INTO defs (entity,def,author) VALUES ("%s","%s","%s");' % (entity.strip(),gdef.strip(),author)
		action = 'a'
	else:
		sql = 'UPDATE defs SET "def"="%s", "author"="%s" WHERE entity="%s";' % (gdef.strip(),author,entity.strip())
		action = 'u'
	
	qres = querywtf('settings/'+gch+'/def.db',sql)
	
	if qres != '':
		return (action,entity)
	else:	
		return qres
		
def del_def(gch,entity):
	del_sql = 'DELETE FROM defs WHERE entity="%s";' % (entity)
	qres = querywtf('settings/'+gch+'/def.db',del_sql)
	return qres		
		
def get_def(gch,entity):
	sql = 'SELECT def,entity FROM defs WHERE entity LIKE "'+entity+'%" ORDER BY entity LIMIT 1;'
	qres = querywtf('settings/'+gch+'/def.db',sql)
	
	if qres:
		return (qres[0][0],qres[0][1])
	else:
		return ''
		
def get_rnd_def(gch):
	sql = 'SELECT * FROM defs ORDER BY RANDOM() LIMIT 1;'
	qres = querywtf('settings/'+gch+'/def.db',sql)
	
	if qres:
		return (qres[0][0],qres[0][1],qres[0][2])
	else:
		return ''
		
def find_ent_def(gch,key):
	sql = 'SELECT entity FROM defs WHERE entity LIKE "%'+key+'%" ORDER BY entity;'
	ent_res = querywtf('settings/'+gch+'/def.db',sql)
	
	sql = 'SELECT entity FROM defs WHERE def LIKE "%'+key+'%" ORDER BY entity;'
	def_res = querywtf('settings/'+gch+'/def.db',sql)
	
	ent_list = []
	def_list = []
	
	if ent_res:
		ent_list = [eli[0] for eli in ent_res if eli[0]]
		
	if def_res:
		def_list = [dli[0] for dli in def_res if dli[0]]	
	
	return (ent_list,def_list)

def get_wtf_state(gch):
	if not os.path.exists('settings/'+gch+'/def.db'):
		sql = 'CREATE TABLE defs (entity varchar, def varchar, author varchar)'
		querywtf('settings/'+gch+'/def.db',sql)
	if not os.path.exists('settings/'+gch+'/readers.db'):
		sql = 'CREATE TABLE readers (jid varchar, rid varchar, unique (rid))'
		querywtf('settings/'+gch+'/readers.db',sql)

def handler_wtf(type, source, parameters):
	groupchat=source[1]
	nick = source[2]
	jid = get_true_jid(groupchat+'/'+nick)
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	if parameters:
		parsepar = parameters.split(' ')
		parsepar.append(' ')
		
		part = parsepar[0]
		spart = parsepar[1]
		
		if not spart.isalpha() and (spart[-1] == 'k'):
			spart = int(spart[:-1]) * 1000
			spart = str(spart)
		elif not part.isalpha() and (part[-1] == 'k'):
			part = int(part[:-1]) * 1000
			part = str(part)
			
		if part.isdigit() and not spart.isdigit():
			part = int(part)
			spart = DEFLIMIT			
			entity = parsepar[1:]
			entity = ' '.join(entity)
			entity = entity.strip()
		elif not part.isdigit() and not spart.isdigit():
			part = 1
			spart = DEFLIMIT
			entity = ' '.join(parsepar)
			entity = entity.strip()
		else:
			part = int(part)
			spart = int(spart)
			entity = parsepar[2:]
			entity = ' '.join(entity)
			entity = entity.strip()
		
		tdef = get_def(groupchat,entity)
		gdef = ''
		
		if tdef:
			gdef = tdef[0]
			entity = tdef[1]
		
		if gdef:
			prt = get_part(gdef,part,spart)
			
			reader_id = get_reader_id(groupchat,jid)
			
			if prt[3] > 1:
				save_pos(groupchat,jid,entity,time.time(),prt[1],spart,prt[3],reader_id)
			
			pref = ''
			suff = ''
			
			if prt[1] > 1:
				pref = '...] '
			if prt[1] != prt[3]:
				suff = ' [...'
			
			if pref or suff:
				rep = u'Article (title: %s; page: %s from %s): %s%s%s' % (entity,prt[1],prt[3],pref,prt[0].replace('&quot;','"'),suff)
			else:
				rep = u'Article (title: %s): %s' % (entity,prt[0].replace('&quot;','"'))
				
			reply(type, source, rep)
		else:
			reply(type, source, u'The article with the title "%s" not found in the dictionary!' % (entity))
	else:
		reply(type, source, u'Invalid syntax!')

def handler_prev(type, source, parameters):
	groupchat=source[1]
	nick = source[2]
	jid = get_true_jid(groupchat+'/'+nick)
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	decpart = 1
	reader_id = get_reader_id(groupchat,jid)
	last_wtf = get_last_wtf(groupchat,reader_id)
	
#-----------------------Local Functions--------------
	
	def out_part(groupchat,jid,entity,part,spart,reader_id,force=False,rnow=False):
		tdef = get_def(groupchat,entity)
		gdef = tdef[0]
		prt = get_part(gdef,part,spart)
		
		if prt[1] != 1 or force:
			save_pos(groupchat,jid,entity,time.time(),prt[1],spart,prt[3],reader_id)
		
		pref = ''
		suff = ''
		
		if prt[1] > 1:
			pref = '...] '
		if prt[1] != prt[3]:
			suff = ' [...'
		
		if not rnow:
			if pref or suff:
				rep = u'Article (title: %s; page: %s from %s): %s%s%s' % (entity,prt[1],prt[3],pref,prt[0].replace('&quot;','"'),suff)
			else:
				rep = u'Article (title: %s): %s' % (entity,prt[0].replace('&quot;','"'))
		else:
			if pref or suff:
				rep = u'- %s/%s -\n\n%s%s%s\n\n- %s/%s -' % (prt[1],prt[3],pref,prt[0].replace('&quot;','"'),suff,prt[1],prt[3])
			else:
				rep = u'Article (title: %s): %s' % (entity,prt[0].replace('&quot;','"'))
		
		return rep
			
#-----------------------End Of Local Functions--------------
	
	if not last_wtf:
		reply(type, source, u'Not specified article!')
		return
	
	if parameters:
		spltdp = parameters.split(' ',1)
		
		entity = ''
		
		if len(spltdp) >= 1:
			entstp = spltdp[0]
			
			if entstp.isdigit():
				decpart = int(entstp)
				
				if decpart <= 0:
					decpart = 1
			else:
				entity = parameters
				
			if entity:
				if chk_rdr_ent(groupchat,entity,reader_id):
					gwtf = get_rdr_wtf(groupchat,reader_id,entity)
					
					part = int(gwtf[1])
					spart = int(gwtf[2])
					rpos = int(gwtf[3])
					
					rep = out_part(groupchat,jid,entity,part,spart,reader_id,force=True)
					reply(type, source, rep)
				elif check_entity(groupchat,entity):
					part = 1
					spart = DEFLIMIT
					rpos = 0
					
					rep = out_part(groupchat,jid,entity,part,spart,reader_id)
					reply(type, source, rep)
				else:
					reply(type, source, u'Not Found: %s' % (entity))
					return
			else:
				entity = last_wtf[0]
				
				part = int(last_wtf[1])
				prev_part = part - decpart
				
				if prev_part <= 0:
					prev_part = 1

				spart = int(last_wtf[2])
				rpos = int(last_wtf[3])
				
				rep = out_part(groupchat,jid,entity,prev_part,spart,reader_id,rnow=True)
				reply(type, source, rep)
		else:	
			reply(type, source, u'Invalid syntax!')
	else:
		entity = last_wtf[0]
		
		currtm = time.time()
		last = float(last_wtf[4])
		tmlong = int(round(currtm - last))
		
		part = int(last_wtf[1])
		
		rnow = False
		
		if tmlong <= 900:
			rnow = True
			prev_part = part - decpart
		else:
			prev_part = part
		
		if prev_part <= 0:
			prev_part = 1
		
		spart = int(last_wtf[2])
		rpos = int(last_wtf[3])
		
		rep = out_part(groupchat,jid,entity,prev_part,spart,reader_id,rnow=rnow)
		reply(type, source, rep)

def handler_next(type, source, parameters):
	groupchat=source[1]
	nick = source[2]
	jid = get_true_jid(groupchat+'/'+nick)
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	incpart = 1
	reader_id = get_reader_id(groupchat,jid)
	last_wtf = get_last_wtf(groupchat,reader_id)
	
#-----------------------Local Functions--------------
	
	def out_part(groupchat,jid,entity,part,spart,reader_id,force=False,rnow=False):
		tdef = get_def(groupchat,entity)
		gdef = tdef[0]
		prt = get_part(gdef,part,spart)
		
		if prt[3] != prt[1] or force:
			save_pos(groupchat,jid,entity,time.time(),prt[1],spart,prt[3],reader_id)
		else:
			del_exp_wtf(groupchat,entity,reader_id)
		
		pref = ''
		suff = ''
		
		if prt[1] > 1:
			pref = '...] '
		if prt[1] != prt[3]:
			suff = ' [...'
		
		if not rnow:
			if pref or suff:
				rep = u'Article (title: %s; page: %s from %s): %s%s%s' % (entity,prt[1],prt[3],pref,prt[0].replace('&quot;','"'),suff)
			else:
				rep = u'Article (title: %s): %s' % (entity,prt[0].replace('&quot;','"'))
		else:
			if pref or suff:
				rep = u'- %s/%s -\n\n%s%s%s\n\n- %s/%s -' % (prt[1],prt[3],pref,prt[0].replace('&quot;','"'),suff,prt[1],prt[3])
			else:
				rep = u'Article (title: %s): %s' % (entity,prt[0].replace('&quot;','"'))
		
		return rep
			
#-----------------------End Of Local Functions--------------
	
	if not last_wtf:
		reply(type, source, u'Not specified article!')
		return
	
	if parameters:
		spltdp = parameters.split(' ',1)
		
		entity = ''
		
		if len(spltdp) >= 1:
			entstp = spltdp[0]
			
			if entstp.isdigit():
				incpart = int(entstp)
				
				if incpart <= 0:
					incpart = 1
			else:
				entity = parameters
				
			if entity:
				if chk_rdr_ent(groupchat,entity,reader_id) and check_entity(groupchat,entity):
					gwtf = get_rdr_wtf(groupchat,reader_id,entity)
					
					part = int(gwtf[1])
					spart = int(gwtf[2])
					rpos = int(gwtf[3])
					
					rep = out_part(groupchat,jid,entity,part,spart,reader_id,force=True)
					reply(type, source, rep)
				elif check_entity(groupchat,entity):
					part = 1
					spart = DEFLIMIT
					rpos = 0
					
					rep = out_part(groupchat,jid,entity,part,spart,reader_id)
					reply(type, source, rep)
				else:
					reply(type, source, u'The article with the title "%s" not found in the dictionary!' % (entity))
					return
			else:
				entity = last_wtf[0]
				
				part = int(last_wtf[1])
				next_part = part + incpart
				
				spart = int(last_wtf[2])
				rpos = int(last_wtf[3])
				
				rep = out_part(groupchat,jid,entity,next_part,spart,reader_id,rnow=True)
				reply(type, source, rep)
		else:	
			reply(type, source, u'Invalid syntax!')
	else:
		entity = last_wtf[0]
		
		currtm = time.time()
		last = float(last_wtf[4])
		tmlong = int(round(currtm - last))
		
		part = int(last_wtf[1])
		
		rnow = False
		
		if tmlong <= 900:
			rnow = True
			next_part = part + incpart
		else:
			next_part = part
		
		spart = int(last_wtf[2])
		rpos = int(last_wtf[3])
		
		rep = out_part(groupchat,jid,entity,next_part,spart,reader_id,rnow=rnow)
		reply(type, source, rep)

def handler_list(type, source, parameters):
	groupchat=source[1]
	nick = source[2]
	jid = get_true_jid(groupchat+'/'+nick)
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
#-----------------------Local Functions--------------

	def out_list(entli,part,quantity):
		if entli:
			prt = get_part_list(entli,part,quantity)
			elist = prt[0]
		
			pref = ''
			suff = '.'
			
			if prt[1] > 1:
				pref = '...] '
			if prt[1] != prt[3]:
				suff = ', [...'
			
			if pref or suff:
				rep =u'List articles (shown: %s of %s; page: %s of %s): %s%s%s' %(len(elist),len(entli),prt[1],prt[3],pref,', '.join(elist),suff)
			else:
				rep =u'List articles (total: %s): %s.' %(len(entli),', '.join(elist))
		else:
			rep = u'The database is empty!'
		
		return rep
			
#-----------------------End Of Local Functions--------------
	
	if parameters:
		parsepar = parameters.split(' ',2)
		
		part = parsepar[0]
		quantity = ''
		
		if len(parsepar) == 2:
			quantity = parsepar[1]
		
		if len(parsepar) == 2 and part.isdigit() and quantity.isdigit():
			part = int(part)
			quantity = int(quantity)			
		elif len(parsepar) == 1 and part.isdigit():
			part = int(part)
			quantity = LISTLIMIT
		else:
			reply(type, source, u'Invalid syntax!')
			return
			
		entli = get_ent_list(groupchat)
		
		rep = out_list(entli,part,quantity)
		reply(type, source, rep)
			
	else:
		entli = get_ent_list(groupchat)
		rep = out_list(entli,1,LISTLIMIT)
		reply(type, source, rep)

def handler_books(type, source, parameters):
	groupchat=source[1]
	nick = source[2]
	jid = get_true_jid(groupchat+'/'+nick)
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
#-----------------------Local Functions--------------

	def out_list(entli,part,quantity):
		if entli:
			prt = get_part_list(entli,part,quantity)
			elist = prt[0]
		
			pref = ''
			suff = '.'
			
			if prt[1] > 1:
				pref = '...] '
			if prt[1] != prt[3]:
				suff = ', [...'
			
			if pref or suff:
				rep =u'List articles (shown: %s of %s; page: %s of %s): %s%s%s' %(len(elist),len(entli),prt[1],prt[3],pref,', '.join(elist),suff)
			else:
				rep =u'List of books (total: %s): %s.' %(len(entli),', '.join(elist))
		else:
			rep = u'No books!'
		
		return rep
			
#-----------------------End Of Local Functions--------------
	
	if parameters:
		parsepar = parameters.split(' ',2)
		
		part = parsepar[0]
		quantity = ''
		
		if len(parsepar) == 2:
			quantity = parsepar[1]
		
		if len(parsepar) == 2 and part.isdigit() and quantity.isdigit():
			part = int(part)
			quantity = int(quantity)			
		elif len(parsepar) == 1 and part.isdigit():
			part = int(part)
			quantity = LISTLIMIT
		else:
			reply(type, source, u'Invalid syntax!')
			return
			
		entli = get_book_list(groupchat)
		
		rep = out_list(entli,part,quantity)
		reply(type, source, rep)	
	else:
		entli = get_book_list(groupchat)
		rep = out_list(entli,1,LISTLIMIT)
		reply(type, source, rep)

def handler_stat(type, source, parameters):
	groupchat=source[1]
	nick = source[2]
	jid = get_true_jid(groupchat+'/'+nick)
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	reader_id = get_reader_id(groupchat,jid)
	opli = get_opened(groupchat,reader_id)

	if not parameters:
		if opli:
			nopli = show_opened(groupchat,opli)
			
			if nopli:
				rep = u'Opened Book (total: %s):\n\n%s' % (len(nopli),'\n'.join(nopli))
			else:
				rep = u'No opened books!'
			
			reply(type, source, rep)
		else:
			reply(type, source, u'No opened books!')
	else:
		bnum = parameters[1:]
		
		if not opli:
			reply(type, source, u'No opened books!')
			return
		
		if bnum.isdigit() and parameters[0] == '-' and len(parameters) >= 2:
			if int(bnum) <= len(opli):
				dbki = int(bnum) - 1
				entity = opli[dbki][0]
				res = del_exp_wtf(groupchat,entity,reader_id)
				
				if res != '':
					reply(type, source, u'The book with the title "%s" closed!' % (entity))
				else:
					reply(type, source, u'Unable to close the book!')
			else:
				reply(type, source, u'Wrong number of open books!')
		elif len(parameters) == 1 and parameters[0] == '-':
			res = clr_rdr_blist(groupchat,reader_id)
			
			if res != '':
				reply(type, source, u'All open book closed!')
			else:
				reply(type, source, u'Unable to close the book!')
		else:
			reply(type, source, u'Invalid syntax!')
		
def handler_dfn(type, source, parameters):
	groupchat=source[1]
	nick = source[2]

	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return

	if parameters:
		parsepar = parameters.split('=',1)
		
		if len(parsepar) == 2:
			entity = parsepar[0]
			gdef = parsepar[1]
			author = nick
			
			if not entity.strip():
				reply(type, source, u'The article should be called!')
				return
			elif not gdef.strip():
				reply(type, source, u'Article can not be empty!')
				return
			
			ent_len = len(entity.split())
			
			if ent_len <= 5:
				res = add_def(groupchat,entity,gdef,author)
				
				if res:
					if res[0] == 'a':
						rep = u'A new article with the title "%s" added to the dictionary!' % (res[1])
					elif res[0] == 'u':
						rep = u'Article with the title "%s" in the dictionary is updated!' % (res[1])
				else:
					rep = u'Error adding!'
					
				reply(type, source, rep)
			else:
				reply(type, source, u'Title should be no longer than five words!')
		else:
			reply(type, source, u'Invalid syntax!')
	else:
		reply(type, source, u'Invalid syntax!')
		
def handler_del(type, source, parameters):
	groupchat=source[1]

	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return

	if parameters:
		entity = parameters.strip()
		
		if check_entity(groupchat,entity):
			res = del_def(groupchat,entity)
		else:
			reply(type, source, u'The article with the title "%s" not found in the dictionary!' % (entity))
			return
		
		if res != '':
			rep = u'Failed requests. Read help on using the command!' % (entity)
		else:
			rep = u'Deleted!'
			
		reply(type, source, rep)			
	else:
		reply(type, source, u'Invalid syntax!')
		
def handler_rnd(type, source, parameters):
	groupchat=source[1]
	nick = source[2]
	jid = get_true_jid(groupchat+'/'+nick)
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	if not parameters:
		res = get_rnd_def(groupchat)
		
		if res != '':
			entity = res[0]
			gdef = res[1]
			prt = get_part(gdef,1,DEFLIMIT)
			
			reader_id = get_reader_id(groupchat,jid)
			
			if prt[3] > 1:
				save_pos(groupchat,jid,entity,time.time(),prt[1],DEFLIMIT,prt[3],reader_id)
			
			pref = ''
			suff = ''
			
			if prt[1] > 1:
				pref = '...] '
			if prt[1] != prt[3]:
				suff = ' [...'
			
			if pref or suff:
				rep = u' Article chosen at random (name: %s; page: %s of %s): %s%s%s' % (entity,prt[1],prt[3],pref,prt[0].replace('&quot;','"'),suff)
			else:
				rep = u' Article chosen at random (name: %s): %s' % (entity,prt[0].replace('&quot;','"'))
				
			reply(type, source, rep)
		else:
			reply(type, source, u'Poorly!')
	else:
		reply(type, source, u'Invalid syntax!')

def handler_find(type, source, parameters):
	groupchat=source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	if parameters:
		key = parameters.strip()
		ent_def_res = find_ent_def(groupchat,key)
		
		rep = ''
		
		ent_list = ent_def_res[0]
		def_list = ent_def_res[1]
		
		if ent_list:
			rep += u'Found in the title (total: %d): %s.' % (len(ent_list),', '.join(ent_list))
			
		if def_list:
			rep += u'\n\nFound articles (total: %d): %s.' % (len(def_list),', '.join(def_list))
			
		if rep:
			reply(type, source, rep.strip())
		else:
			reply(type, source, u'Nothing found!')
	else:
		reply(type, source, u'Invalid syntax!')

def handler_search(type, source, parameters):
	groupchat=source[1]
	nick = source[2]
	jid = get_true_jid(groupchat+'/'+nick)

	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return

#-----------------------Local Functions--------------
	
	def out_part(groupchat,jid,entity,pgdef,part,qofparts,reader_id):
		if qofparts != part:
			save_pos(groupchat,jid,entity,time.time(),part,DEFLIMIT,qofparts,reader_id)
		
		pref = ''
		suff = ''
		
		if prt[1] > 1:
			pref = '...] '
		if prt[1] != prt[3]:
			suff = ' [...'
		
		if pref or suff:
			rep = u'Article (title: %s; page: %s from %s): %s%s%s' % (entity,part,qofparts,pref,pgdef.replace('&quot;','"'),suff)
		else:
			rep = u'Article (title: %s): %s' % (entity,pgdef.replace('&quot;','"'))
		
		return rep
			
#-----------------------End Of Local Functions--------------

	reader_id = get_reader_id(groupchat,jid)

	if parameters:
		parsepar = parameters.split(':',1)
		
		if len(parsepar) == 2:
			entity = parsepar[0].strip()
			qstr = parsepar[1].strip()
				
			if qstr:
				if entity:
					if check_entity(groupchat,entity):
						tdef = get_def(groupchat,entity)
						gdef = tdef[0]
						prt = get_part(gdef,1)
						
						qofparts = prt[3]
						pgdef = prt[0]
						pglist = []
						
						if pgdef.find(qstr) != -1:
							pglist.append(1)
						
						pind = 2
						prt = get_part(gdef,pind)
						pgdef = prt[0]
						
						while pind != qofparts + 1:
							if pgdef.find(qstr) != -1:
								pglist.append(pind)
							
							pind += 1
							prt = get_part(gdef,pind)
							pgdef = prt[0]
					
						if pglist:
							prt = get_part(gdef,pglist[0])
							strpgli = [str(sli) for sli in pglist[1:]]
							pgdef = prt[0]
							
							rep = out_part(groupchat,jid,entity,pgdef,prt[1],qofparts,reader_id)
							
							if strpgli:
								rep += u'\n\nAlso, a match is found on pages (total: %d): %s.' % (len(strpgli), ', '.join(strpgli))
								
							reply(type, source, rep.replace(qstr,' -> '+qstr.upper()+' <- '))
						else:
							reply(type, source, u'Nothing found!')
					else:
						reply(type, source, u'The article with the title "%s" not found in the dictionary!' % (entity))
				else:
					reply(type, source, u'Not specified article!')
			else:
				reply(type, source, u'Empty search string!')
		else:
			reply(type, source, u'Invalid syntax!')
	else:
		reply(type, source, u'Invalid syntax!')

def handler_count(type, source, parameters):
	groupchat=source[1]

	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return

	ent_count = get_ent_count(groupchat)
	
	if ent_count != 0:
		rep = u'Number of articles in the dictionary: %d'% (ent_count)
	else:
		rep = u'The database is empty!'
		
	reply(type, source, rep)

def handler_get_wtf(type, source, parameters):
	groupchat=source[1]
	nick = source[2]

	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can only be used in conference!')
		return
	
	if parameters:
		entity = parameters.strip()
		gdef = get_def(groupchat,entity)
		
		if gdef:
			data = gdef[0].replace('&quot;','"')
			entity = gdef[1]
		else:
			reply(type, source, u'The article with title "%s" not found in the dictionary!' % (entity))
			return
		
		to = ''
		
		if GROUPCHATS[groupchat].has_key(nick):
			to = GROUPCHATS[groupchat][nick]['jid']
		
		if not to:
			reply(type, source, u'Internal error, can not perform the operation!')
			return
		
		sid = 'file'+str(random.randrange(10000000, 99999999))
		name = sid+'.txt'
		
		fp = wr_op_file('settings/'+name, data)
		
		frm = JID+'/'+RESOURCE
		
		sireq = si_request(frm,to,sid,name,len(data),entity)
		JCON.SendAndCallForResponse(sireq, handler_load_answ, args={'type':type,'source':source,'sid':sid,'to':to,'fp':fp})
	else:
		reply(type, source, u'Invalid syntax!')
		
def handler_load_answ(coze,resp,type,source,sid,to,fp):
	rtype = resp.getType()
	
	if rtype == 'result':
		JCON.IBB.OpenStream(sid,to,fp,1024)
		name = fp.name
		os.remove(name)
	else:
		name = fp.name
		fp.close()
		os.remove(name)
		reply(type, source, u'Unsuccessful translated!')

register_command_handler(handler_wtf, COMM_PREFIX+'wtf', ['info','wtf','all','*'], 11, 'Conclusion of the article from the database. Entirely, if the article is small, or the first page size %s characters, by default, if the article is great. It also allows you to receive and the rest of the page and set the page size in symbols, if the article is more than %s characters.' %(DEFLIMIT,DEFLIMIT), COMM_PREFIX+'wtf [<page_number>[<page_size>[k]]] <article_name>', [COMM_PREFIX+'wtf article', COMM_PREFIX+'wtf 3 article', COMM_PREFIX+'wtf 44 article', COMM_PREFIX+'wtf 3 10k big article', COMM_PREFIX+'wtf 5 1000 big article'])
register_command_handler(handler_next, COMM_PREFIX+'next', ['info','wtf','all','*'], 11, 'Lets get the following page of the article. Without arguments displays the following page article from the database after the withdrawal of the command %swtf, if the page size is smaller than the article and do not specify a step. When you specify a step displays a page number equal to the current page number + step. When referring to title of article, it becomes the current, i.e at the next command %snext will see the following page of this article.' % (COMM_PREFIX,COMM_PREFIX), COMM_PREFIX+'next [<article_name>]|[<step>]', [COMM_PREFIX+'next',COMM_PREFIX+'next article', COMM_PREFIX+'next 2'])
register_command_handler(handler_prev, COMM_PREFIX+'prev', ['info','wtf','all','*'], 11, 'Lets get the previous page of the article. Without arguments displays the previous page article from the database, after the withdrawal of the command %swtf, if the page number is smaller than the article and not specified step. When you specify a step displays a page number equal to the number of the current page - step.  When referring to title of article, it becomes the current, i.e at the next command %sprev see previous page of this article.' % (COMM_PREFIX,COMM_PREFIX), COMM_PREFIX+'prev [<article_name>]|[<step>]', [COMM_PREFIX+'prev',COMM_PREFIX+'prev article', COMM_PREFIX+'prev 3'])
register_command_handler(handler_list, COMM_PREFIX+'list', ['info','wtf','all','*'], 11, 'Lets get a list of articles, in whole or in parts. Without arguments displays the entire list of articles if the articles less %s, or part of the list size %s names, if more articles %s.' % (LISTLIMIT,LISTLIMIT,LISTLIMIT), COMM_PREFIX+'list [<page>][<number>]', [COMM_PREFIX+'list', COMM_PREFIX+'list 3', COMM_PREFIX+'list 2 20'])
register_command_handler(handler_books, COMM_PREFIX+'books', ['info','wtf','all','*'], 11, 'Lets get a list of books, in whole or in part. Without parameters displays the entire list of books if the book is less %s, or part of the list size %s names, if more books %s.' % (LISTLIMIT,LISTLIMIT,LISTLIMIT), COMM_PREFIX+'books [<page>][<number>]', [COMM_PREFIX+'books', COMM_PREFIX+'books 3', COMM_PREFIX+'books 2 20'])
register_command_handler(handler_stat, COMM_PREFIX+'stat', ['info','wtf','all','*'], 11, 'Lets get statistics on the open books. When you specify a negative integer closes the book with this number.', COMM_PREFIX+'stat [-<number>]', [COMM_PREFIX+'stat',COMM_PREFIX+'stat -3'])
register_command_handler(handler_dfn, COMM_PREFIX+'dfn', ['info','wtf','all','*'], 11, ' Adds a new, or update existing, article. When you specify instead of article path to a text file with, adds an article from a text file.', COMM_PREFIX+'dfn <name>=<body_articles>', [COMM_PREFIX+'dfn first article=article, such article'])
register_command_handler(handler_del, COMM_PREFIX+'del', ['info','wtf','all','*'], 20, 'Deletes an article with the specified name from the dictionary.', COMM_PREFIX+'del <name>', [COMM_PREFIX+'del first article'])
register_command_handler(handler_rnd, COMM_PREFIX+'rnd', ['info','wtf','all','*'], 11, 'Displays a random article from the dictionary.', COMM_PREFIX+'rnd', [COMM_PREFIX+'rnd'])
register_command_handler(handler_find, COMM_PREFIX+'find', ['info','wtf','all','*'], 11, 'Looking for a word or phrase in the title and text of articles.', COMM_PREFIX+'find <word>|<phrase>', [COMM_PREFIX+'find life',COMM_PREFIX+'find something interesting'])
register_command_handler(handler_search, COMM_PREFIX+'search', ['info','wtf','all','*'], 11, 'Looking for a word or phrase in the text of the article and displays the page on which the precise word or phrase.', COMM_PREFIX+'search <article>:<word>|<phrase>', [COMM_PREFIX+'search book: riddle'])
register_command_handler(handler_count, COMM_PREFIX+'count', ['info','wtf','all','*'], 11, 'Displays the number of articles in the dictionary.', COMM_PREFIX+'count', [COMM_PREFIX+'count'])
register_command_handler(handler_get_wtf, COMM_PREFIX+'get_wtf', ['info','wtf','all','*'], 11, 'Send an article from the dictionary file via jabber.', COMM_PREFIX+'get_wtf <article_name>', [COMM_PREFIX+'get_wtf book'])

register_stage1_init(get_wtf_state)