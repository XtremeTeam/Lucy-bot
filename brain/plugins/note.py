#===islucyplugin===
# -*- coding: utf-8 -*-

#  note_plugin.py


#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import sqlite3 as db
import time, os

def querynote(dbpath,query):
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

def get_jid(gch, nick):
	nick = nick.replace('"','&quot;')
	sql = 'SELECT jid FROM users WHERE nick="%s";' % (nick)
	qres = querynote('settings/'+gch+'/users.db',sql)
	
	if qres:
		jid = qres[0][0]
		return jid
		
def show_notes(gch, notes, pref='',miff='',start=0,end=10):
	rng = []
	
	if notes:
		if start == 0 and end == 10:
			if len(notes) >= 10:
				rng = range(10)
			else:
				rng = range(len(notes))
		else:
			rng = range(end-start)
		
	nosli = ['%s) %s%s%s%s:\n%s' % (li+start+1,pref,time.strftime('%d.%m.%Y',time.localtime(float(notes[li+start][0]))),miff,time.strftime('%H:%M:%S',time.localtime(float(notes[li+start][0]))), notes[li+start][1].replace('&quot;','"')) for li in rng]
			
	return nosli
	
def del_note(gch, notes_id, note):
	del_sql = 'DELETE FROM %s WHERE note="%s";' % (notes_id, note)
	res=querynote('settings/'+gch+'/notes.db',del_sql)
	return res
	
def delall_notes(gch, notes_id):
	drop_sql = 'DROP TABLE %s;' % (notes_id)
	res=querynote('settings/'+gch+'/notes.db',drop_sql)
	return res

def get_notes(gch,notes_id):
	sql = 'SELECT * FROM %s ORDER BY ndate DESC;' % (notes_id)
	notes = querynote('settings/'+gch+'/notes.db',sql)
	return notes

def check_notes_id(gch,notes_id):
	sql = 'SELECT * FROM notes WHERE id="%s";' % (notes_id)
	qres = querynote('settings/'+gch+'/notes.db',sql)
	
	if qres:
		return False
	else:
		return True	
	
def get_notes_id(gch,jid):
	sql = 'SELECT id FROM notes WHERE jid="%s";' % (jid)
	notes_id = querynote('settings/'+gch+'/notes.db',sql)
	
	if notes_id:
		return notes_id[0][0]

def note_add(gch,jid,note,notes_id=''):
	if not notes_id:
		notes_id = 'notes'+str(random.randrange(10000000, 99999999))
		chk_ntsid = check_notes_id(gch,notes_id)
		
		while not chk_ntsid:
			notes_id = 'notes'+str(random.randrange(10000000, 99999999))
			chk_ntsid = check_notes_id(gch,notes_id)
		
		sql = 'INSERT INTO notes (jid,id) VALUES ("%s","%s");' % (jid,notes_id)
		res = querynote('settings/'+gch+'/notes.db',sql)
	
		sql = 'CREATE TABLE %s (ndate varchar not null, note varchar not null, unique(note));' % (notes_id)
		res = querynote('settings/'+gch+'/notes.db',sql)
	
	note = note.replace(r'"', r'&quot;')
	date = time.time()
	
	sql = 'INSERT INTO %s (ndate,note) VALUES ("%s","%s");' % (notes_id,date,note)
	res = querynote('settings/'+gch+'/notes.db',sql)
	
	if res == '':
		sql = 'CREATE TABLE %s (ndate varchar not null, note varchar not null, unique(note));' % (notes_id)
		res = querynote('settings/'+gch+'/notes.db',sql)
		
		sql = 'INSERT INTO %s (ndate,note) VALUES ("%s","%s");' % (notes_id,date,note)
		res = querynote('settings/'+gch+'/notes.db',sql)

	return res

def get_note_state(gch):
	if not os.path.exists('settings/'+gch+'/notes.db'):
		sql = 'CREATE TABLE notes (jid varchar not null, id varchar not null, unique(jid,id));'
		res = querynote('settings/'+gch+'/notes.db',sql)

def handler_notes(type, source, parameters, recover=False, jid='', rcts=''):
	groupchat = source[1]
	nick = source[2]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	jid = get_jid(groupchat,nick)
	
	notes_id = get_notes_id(groupchat,jid)
	notes = get_notes(groupchat,notes_id)
	tonos = len(notes)

#-----------------------Local Functions--------------

	def add_note(type,source,groupchat,jid,parameters,notes_id):
		res = note_add(groupchat,jid,parameters,notes_id)
		
		if res != '':
			reply(type, source, u'Successfully added!')
		else:
			reply(type, source, u'Failed adding! Perhaps this article already exists!')
			
	def out_notes(type,source,groupchat,notes,tonos,stn,enn):
		notl = show_notes(groupchat, notes, u'Записано ',u' в ',stn-1,enn)		

		head = ''
		foot = ''	
				
		if stn >= 2 and stn != enn:
			head = u'[<---beginning---]\n\n'
		
		if enn < tonos and stn != enn:
			foot = u'\n\n[---ending--->]'
		elif enn == tonos and tonos == 10:
			foot = ''
		
		if notl:
			if type == 'public':
				if stn == enn:
					rep = u'Note (total: %s):\n%s%s%s' % (tonos,head,'\n\n'.join(notl),foot)
				else:
					rep = u'Notes (total: %s):\n%s%s%s' % (tonos,head,'\n\n'.join(notl),foot)
				
				reply(type, source, u'Look in private!')
				reply('private', source, rep)
			else:
				if stn == enn:
					rep = u'Note (total: %s):\n%s%s%s' % (tonos,head,'\n\n'.join(notl),foot)
				else:
					rep = u'Notes (total: %s):\n%s%s%s' % (tonos,head,'\n\n'.join(notl),foot)
					
				reply(type, source, rep)
		else:
			rep = u'Нет заметок!'
			reply(type, source, rep)

#--------------------End Of Local Functions----------

	if parameters:
		spltdp = parameters.split(' ',1)
		nnote = spltdp[0]
		
		if len(spltdp) == 1:
			if '-' in nnote:
				nnote = nnote.split('-',1)
				nnote = [li for li in nnote if li != '']
				
				if len(nnote) == 2:
					if nnote[0].isdigit():
						stn = int(nnote[0])
						
						if not stn:
							add_note(type,source,groupchat,jid,parameters,notes_id)
							return
					else:
						add_note(type,source,groupchat,jid,parameters,notes_id)
						return

					if nnote[1].isdigit():
						enn = int(nnote[1])
						
						if enn > tonos:
							add_note(type,source,groupchat,jid,parameters,notes_id)
							return
					else:
						add_note(type,source,groupchat,jid,parameters,notes_id)
						return							
									
					if stn > enn:
						add_note(type,source,groupchat,jid,parameters,notes_id)
						return									
					
					out_notes(type,source,groupchat,notes,tonos,stn,enn)	
				elif len(nnote) == 1:
					if nnote[0].isdigit():
						nno = int(nnote[0])
						
						if nno > tonos or nno == 0:
							add_note(type,source,groupchat,jid,parameters,notes_id)
							return
						
						note = notes[nno-1][1].strip()
						res = del_note(groupchat, notes_id, note)
						
						if res != '':
							reply(type, source, u'Note number %s deleted!' % (nno))
						else:
							reply(type, source, u'Error deletion!')
					else:
						add_note(type,source,groupchat,jid,parameters,notes_id)	
				elif not nnote:
					delall_notes(groupchat, notes_id)
					reply(type, source, u'Notes cleaned!')
			else:
				if nnote.isdigit():
					if int(nnote) != 0 and int(nnote) <= tonos:
						nnote = int(nnote)
						
						out_notes(type,source,groupchat,notes,tonos,nnote,nnote)	
					else:
						add_note(type,source,groupchat,jid,parameters,notes_id)
				else:
					add_note(type,source,groupchat,jid,parameters,notes_id)
		else:
			add_note(type,source,groupchat,jid,parameters,notes_id)
	else:
		out_notes(type,source,groupchat,notes,tonos,1,10)

register_stage1_init(get_note_state)

register_command_handler(handler_notes, 'note', ['info','fun','all','*'], 11, 'Allows users (with access 11 and above) to keep personal notes. Without arguments displays the first 10 notes, if more than 10, or all if less than 10 or 10 if it is only 10. When you specify a number displays the article with that number: %snote 4. When you specify a minus sign before the number, delete a note of this number, example: %snote -7. When you specify a range in the format <beginning>-<ending>, displays notes beginning with a specified boundary <beginning> and to the number specified boundary <ending>, example: %snote 3-8. When you specify the text, adds a new note, example: %snote Sample notes.', 'note [<number>|<Beginning>-<ending>|-<number>|<text>]', ['note','note 5','note 3-7','note -4','note Note, anything.'])