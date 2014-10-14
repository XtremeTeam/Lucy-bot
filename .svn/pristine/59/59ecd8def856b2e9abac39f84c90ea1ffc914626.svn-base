#===islucyplugins===
# -*- coding: utf-8 -*-

#  Lucy pseudo AI plugin v1.0
#  ssh_plugin.py


#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import sqlite3 as db
import time

LAST_PHRASE_ID = {}
PAI_OCC = {}

#obscene_words = [u'бляд', u' блят', u' бля ', u' блять ', u' плять ', u' хуй', u' ибал', u' ебал', u'нахуй', u' хуй', u' хуи', u'хуител', u' хуя', u'хуя', u' хую', u' хуе', u' ахуе', u' охуе', u'хуев', u' хер ', u' хер', u'хер', u' пох ', u' нах ', u'писд', u'пизд', u'рizd', u' пздц ', u' еб', u' епана ', u' епать ', u' ипать ', u' выепать ', u' ибаш', u' уеб', u'проеб', u'праеб', u'приеб', u'съеб', u'сьеб', u'взъеб', u'взьеб', u'въеб', u'вьеб', u'выебан', u'перееб', u'недоеб', u'долбоеб', u'долбаеб', u' ниибац', u' неебац', u' неебат', u' ниибат', u' пидар', u' рidаr', u' пидар', u' пидор', u'педор', u'пидор', u'пидарас', u'пидараз', u' педар', u'педри', u'пидри', u' заеп', u' заип', u' заеб', u'ебучий', u'ебучка ', u'епучий', u'епучка ', u' заиба', u'заебан', u'заебис', u' выеб', u'выебан', u' поеб', u' наеб', u' наеб', u'сьеб', u'взьеб', u'вьеб', u' гандон', u' гондон', u'пахуи', u'похуис', u' манда ', u'мандав', u' залупа', u' залупог']
order_obscene_words = [u' babi ', u' memek ', u' vagina ', u' kontol ', u' bangsat ', u' perek ', u' tetek ', u' (_|_) ', u' fuck ', u' tai ', u' titit ', u' peler ', u' penis ', u' itil ', u' entot ', u' kentot ']

def check_obscene_words(body):
	body=body.lower()
	body=u' '+body+u' '
	for x in obscene_words:
		if body.count(x):
			return True
	return False

def queryphrase(dbpath,query):
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
		return '1'

def get_pai_phrases(gch):
	sql = 'SELECT * FROM phrases ORDER BY id DESC;'
	phrases = queryphrase('settings/'+gch+'/pai_phrases.db',sql)
	return phrases

def find_phrases(phrases,phrase):
	if phrases:
		fophli = [pli for pli in phrases if phrase in pli[1]]
		return fophli

def show_phrases(phrases,start=0,end=10):
	rng = []
	
	if phrases:
		if start == 0 and end == 10:
			if len(phrases) >= 10:
				rng = range(10)
			else:
				rng = range(len(phrases))
		else:
			rng = range(end-start)
	
	nphli = ['%s) %s: %s' % (li+start+1,phrases[li+start][0],phrases[li+start][1].replace('&quot;','"')) for li in rng]
			
	return nphli

def get_nicks(gch):
	sql = 'SELECT nick FROM users ORDER BY uleave;'
	qres = queryinfo('settings/'+gch+'/users.db',sql)
	
	if qres:
		nicks = [nil[0].replace('&quot;','"') for nil in qres]
		return nicks
		
def rmv_nick(gch, body):
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
	
def count_phrase(gch):
	sql = 'SELECT id FROM phrases;'
	count = queryphrase('settings/'+gch+'/pai_phrases.db',sql)
	return count

def save_phrase(phrase, gch):
	nicks = get_nicks(gch)
	
	for nil in nicks:
		if nil in phrase:
			return
	
	phrase = phrase.replace(r'"', r'&quot;')
	sql = 'INSERT INTO phrases (phrase) VALUES ("%s");' % (phrase.strip().encode('utf-8'))
	rep = queryphrase('settings/'+gch+'/pai_phrases.db',sql)
	return rep

def del_phrase(phrase_id,gch):
	sql = 'DELETE FROM phrases WHERE id="%s";' % (phrase_id)
	rep = queryphrase('settings/'+gch+'/pai_phrases.db',sql)
	return rep

def get_reply(phrase,gch):
	rep = ''
	rep_phrase=''
	words = phrase.split(' ')
	
	keyword = words[random.randrange(len(words))]
	length = len(words)
	src = random.randrange(length)

	keyword = keyword[src:src + random.randrange(length) + 2]

	sql = 'SELECT * FROM phrases WHERE phrase LIKE "%'+keyword+'%" ORDER BY RANDOM() LIMIT 1;'
	rep = queryphrase('settings/'+gch+'/pai_phrases.db',sql)
	
	if rep:
		rep = list(rep[0])
		if len(rep) >= 2:
			rep_phrase = rep[1].encode('utf-8')
		rep_phrase = rep_phrase.replace(r'&quot;',r'"')
		global LAST_PHRASE_ID
		LAST_PHRASE_ID[gch] = rep[0]
	return rep_phrase.strip()

def get_pai_state(gch):
	LAST_PHRASE_ID[gch] = 0
	
	if not os.path.exists('settings/'+gch+'/pai_phrases.db'):
		sql = 'CREATE TABLE phrases(id integer primary key autoincrement, phrase text not null,unique (phrase))'
		queryphrase('settings/'+gch+'/pai_phrases.db',sql)
	
	if not 'pai' in GCHCFGS[gch]:
		GCHCFGS[gch]['pai']={'on':0,'learning':0, 'occ':10, 'think':5,'ron':[],'roff':[]}
		PAI_OCC[gch] = 100 - GCHCFGS[gch]['pai']['occ']
	else:
		PAI_OCC[gch] = 100 - GCHCFGS[gch]['pai']['occ']

def handler_pai(type, source, body):
	groupchat = source[1]
	pai_on = 0
	
	if GROUPCHATS.has_key(groupchat):
		pai_on = GCHCFGS[groupchat]['pai']['on']
		
	global PAI_OCC
	
	if pai_on == 1:
		nick = source[2]
		bot_nick = get_bot_nick(groupchat)
		learning = GCHCFGS[groupchat]['pai']['learning']
		occurrence_freq = GCHCFGS[groupchat]['pai']['occ']
		reply_on = GCHCFGS[groupchat]['pai']['ron']
		reply_off = GCHCFGS[groupchat]['pai']['roff']
		think = GCHCFGS[groupchat]['pai']['think']
			
		if body:
			comm_alias = body.split(' ')[0]
	
		if type == 'public' and not nick in reply_off:
			if (nick != bot_nick and nick) and not (comm_alias.lower() in COMMANDS or comm_alias.lower() in MACROS.macrolist[groupchat] or comm_alias.lower() in MACROS.gmacrolist):

				if bot_nick in body:
					body = rmv_nick(groupchat, body)
					
					rep = get_reply(body,groupchat)
					
					if learning and body and len(body) <= 255 and len(body) >= 3:
						if check_obscene_words(body) == False:
							if body.split(' ')[0] == '/me':
								for I in GROUPCHATS[groupchat]:
									if I in body:
										body = body.replace(I,'%nick%')
										break
							
							if not body[0] in [COMM_PREFIX,'*','.','-','!']:
								save_phrase(body, groupchat)
						
					if rep:
						time.sleep(random.randrange(3,think))
						
						if rep.split(' ')[0] == '/me':
							if '%nick%' in rep:
								rep = rep.replace('%nick%',nick.encode('utf-8'))
							
							msg(groupchat, rep)
						else:	
							reply(type, source, rep)
					return
				elif [ron for ron in reply_on if ron in body] and not [roff for roff in reply_off if roff in body]:
					rep = get_reply(body,groupchat)
					
					if rep:
						time.sleep(random.randrange(3,think))
						
						if rep.split(' ')[0] == '/me':
							if '%nick%' in rep:
								rep = rep.replace('%nick%',nick.encode('utf-8'))
							
							msg(groupchat, rep)
						else:	
							reply(type, source, rep)
					return
				else:
					if PAI_OCC[groupchat] == 0:
						PAI_OCC[groupchat] = 100 - occurrence_freq
						
						body = rmv_nick(groupchat, body)
						
						rep = get_reply(body,groupchat)
						
						if learning and body and len(body) <= 255 and len(body) >= 3:
							if check_obscene_words(body) == False:
								if body.split(' ')[0] == '/me':
									for I in GROUPCHATS[groupchat]:
										if I in body:
											body = body.replace(I,'%nick%')
											break
							
								if not body[0] in [COMM_PREFIX,'*','.','-','!']:
									save_phrase(body, groupchat)
						
						if rep:
							time.sleep(random.randrange(3,think))
							
							if rep.split(' ')[0] == '/me':
								if '%nick%' in rep:
									rep = rep.replace('%nick%',nick.encode('utf-8'))
										
								msg(groupchat, rep)
							else:	
								reply(type, source, rep)
						return
						
				if PAI_OCC[groupchat] > 0:
					PAI_OCC[groupchat] = PAI_OCC[groupchat] - 1
		elif type == 'private': #here private
			if nick != bot_nick and not (comm_alias.lower() in COMMANDS or comm_alias.lower() in MACROS.macrolist[groupchat] or comm_alias.lower() in MACROS.gmacrolist):
				rep = get_reply(body,groupchat)
				
				if rep:
					if rep.split(' ')[0] == '/me':
						if '%nick%' in rep:
							rep = rep.replace('%nick%',nick.encode('utf-8'))

					time.sleep(random.randrange(3,think))
					reply(type, source, rep)

def handler_pai_control(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	if parameters:
		try:
			int(parameters)
		except:
			reply(type,source,u'Invalid syntax!')
			return
			
		if int(parameters)>1:
			reply(type,source,u'Invalid syntax!')
			return
		
		if parameters=="1":
			GCHCFGS[groupchat]['pai']['on']=1
			reply(type,source,u'Function chat-bot enabled!')
		else:
			GCHCFGS[groupchat]['pai']['on']=0
			reply(type,source,u'Function chat-bot disabled!')
		write_file('settings/'+groupchat+'/config.cfg', str(GCHCFGS[groupchat]))
	else:
		if GCHCFGS[groupchat]['pai']['on']==1:
			reply(type,source,u'Function chat-bot enabled!')
		else:
			reply(type,source,u'Function chat-bot disabled!')

def handler_pai_learn(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	if parameters:
		try:
			int(parameters)
		except:
			reply(type,source,u'Invalid syntax!')
			return
			
		if int(parameters)>1:
			reply(type,source,u'Invalid syntax!')
			return
		
		if parameters=="1":
			GCHCFGS[groupchat]['pai']['learning']=1
			reply(type,source,u'Chat-bot learning enabled!')
		else:
			GCHCFGS[groupchat]['pai']['learning']=0
			reply(type,source,u'Chat-bot learning disabled!')
		write_file('settings/'+groupchat+'/config.cfg', str(GCHCFGS[groupchat]))
	else:
		if GCHCFGS[groupchat]['pai']['learning']==1:
			reply(type,source,u'Chat-bot learning enabled!')
		else:
			reply(type,source,u'Chat-bot learning disabled!')
			
def handler_pai_occ(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	if parameters:
		try:
			int(parameters)
		except:
			reply(type,source,u'Invalid syntax!')
			return
			
		if int(parameters)>100:
			reply(type,source,u'Invalid syntax!')
			return
		
		GCHCFGS[groupchat]['pai']['occ']=int(parameters)
		PAI_OCC[groupchat] = 100 - int(parameters)
		reply(type,source,u'The level of chat-bot is set to '+str(parameters)+'%!')
		
		write_file('settings/'+groupchat+'/config.cfg', str(GCHCFGS[groupchat]))
	else:
		reply(type,source,u'The level of chat-bot is '+str(GCHCFGS[groupchat]['pai']['occ'])+'%!')
			
def handler_pai_think(type, source, parameters):
	groupchat = source[1]

	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	if parameters:
		try:
			int(parameters)
		except:
			reply(type,source,u'Invalid syntax!')
			return
			
		if int(parameters)>100 or int(parameters) <= 3:
			reply(type,source,u'Invalid syntax!')
			return
		
		GCHCFGS[groupchat]['pai']['think']=int(parameters)
		reply(type,source,u'Thinking time is set to '+str(parameters)+u' sec.!')
		
		write_file('settings/'+groupchat+'/config.cfg', str(GCHCFGS[groupchat]))
	else:
		reply(type,source,u'Thinking time is '+str(GCHCFGS[groupchat]['pai']['think'])+u' sec.!')

def handler_pai_ron(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	ron_list = parameters.split(' ')
	
	if parameters:
		if ',' in parameters or ':' in parameters:
			reply(type,source,u'Invalid syntax!')
			return
			
		t_ron_list = GCHCFGS[groupchat]['pai']['ron']
		ron_list = [ron for ron in ron_list if not ron in t_ron_list]	
			
		GCHCFGS[groupchat]['pai']['ron'].extend(ron_list)
		reply(type,source,u'Added the words which reacts bot (total: '+str(len(ron_list))+u'): '+', '.join(ron_list)+u'!')
		
		roff_list = GCHCFGS[groupchat]['pai']['roff']
		roff_list = [roff for roff in roff_list if not roff in ron_list]
		GCHCFGS[groupchat]['pai']['roff'] = roff_list
		
		write_file('settings/'+groupchat+'/config.cfg', str(GCHCFGS[groupchat]))
	else:
		if GCHCFGS[groupchat]['pai']['ron']:
			reply(type,source,u'Words which reacts bot (total: '+str(len(GCHCFGS[groupchat]['pai']['ron']))+u'): '+', '.join(GCHCFGS[groupchat]['pai']['ron'])+u'!')
		else:
			reply(type,source,u'The list of words which reacts bot is empty!')

def handler_pai_roff(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	roff_list = parameters.split(' ')
	
	if parameters:
		if ',' in parameters or ':' in parameters:
			reply(type,source,u'Invalid syntax!')
			return
			
		t_roff_list = GCHCFGS[groupchat]['pai']['roff']
		roff_list = [roff for roff in roff_list if not roff in t_roff_list]
			
		GCHCFGS[groupchat]['pai']['roff'].extend(roff_list)
		reply(type,source,u'Added the words that ignores the bot (total: '+str(len(roff_list))+u'): '+', '.join(roff_list)+u'!')
		
		ron_list = GCHCFGS[groupchat]['pai']['ron']
		ron_list = [ron for ron in ron_list if not ron in roff_list]
		GCHCFGS[groupchat]['pai']['ron'] = ron_list
		
		write_file('settings/'+groupchat+'/config.cfg', str(GCHCFGS[groupchat]))
	else:
		if GCHCFGS[groupchat]['pai']['roff']:
			reply(type,source,u'Words that ignores the bot (total: '+str(len(GCHCFGS[groupchat]['pai']['roff']))+u'): '+', '.join(GCHCFGS[groupchat]['pai']['roff'])+u'!')
		else:
			reply(type,source,u'List of words that ignores the boat is empty!')

def handler_pai_roffd(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	roff_word = parameters.split(' ')[0]
	
	if parameters:
		if ',' in parameters or ':' in parameters:
			reply(type,source,u'Invalid syntax!')
			return
		
		if roff_word in GCHCFGS[groupchat]['pai']['roff']:	
			GCHCFGS[groupchat]['pai']['roff'].remove(roff_word)
		else:
			reply(type,source,u'Word is not found?')
			return
		
		reply(type,source,u'Word "'+roff_word+u'"'+u' removed from the list!')
		
		write_file('settings/'+groupchat+'/config.cfg', str(GCHCFGS[groupchat]))
	else:
		if GCHCFGS[groupchat]['pai']['roff']:
			GCHCFGS[groupchat]['pai']['roff'] = []
			reply(type,source,u'The list of words that ignores the bot cleaned!')
		else:
			reply(type,source,u'List of words that ignores the bot is empty!')

def handler_pai_rond(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	ron_word = parameters.split(' ')[0]
	
	if parameters:
		if ',' in parameters or ':' in parameters:
			reply(type,source,u'Invalid syntax!')
			return
			
		if ron_word in GCHCFGS[groupchat]['pai']['ron']:	
			GCHCFGS[groupchat]['pai']['ron'].remove(ron_word)
		else:
			reply(type,source,u'And, what?')
			return
			
		reply(type,source,u'Word "'+ron_word+u'"'+u' removed from the list!')
		
		write_file('settings/'+groupchat+'/config.cfg', str(GCHCFGS[groupchat]))
	else:
		if GCHCFGS[groupchat]['pai']['ron']:
			GCHCFGS[groupchat]['pai']['ron'] = []
			reply(type,source,u'The list of words which reacts bot cleaned!')
		else:
			reply(type,source,u'The list of words which reacts bot is empty!')

def handler_pai_add(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	if parameters:
		res = save_phrase(parameters, groupchat)
		if not res:
			reply(type,source,u'The phrase is added!')
		else:
			reply(type,source,u'Error adding the phrase!')
	else:
		reply(type,source,u'Invalid syntax!')

def handler_pai_del(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	if parameters:
		res = del_phrase(parameters, groupchat)
		if not res:
			if parameters.isdigit():
				reply(type,source,u'Phrase number %s is removed from the database!' % (parameters))
			else:
				reply(type,source,u'Invalid syntax!')
		else:
			reply(type,source,u'Error removing phrase!')
	else:
		res = del_phrase(LAST_PHRASE_ID[groupchat], groupchat)
		if not res:
			reply(type,source,u'Phrase number %s removed from the database!' % (LAST_PHRASE_ID[groupchat]))
		else:
			reply(type,source,u'Error removing phrase!')

def handler_pai_count(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
	res = count_phrase(groupchat)
	count = len(res)
		
	if count:
		reply(type,source,u'The number of phrases in the database: %s!' % (count))
	else:
		reply(type,source,u'The database is empty!')

def handler_pai_show(type, source, parameters):
	groupchat = source[1]
	
	if not GROUPCHATS.has_key(groupchat):
		reply(type, source, u'This command can be used only in the conference!')
		return
	
#-----------------------Local Functions--------------
	
	def phrases_find(type,source,phrases,phrase):
		fophli = find_phrases(phrases,phrase)
					
		if fophli:
			nphli = show_phrases(fophli)
			rep = u'Found phrases (total: %s):\n%s' % (len(nphli),'\n'.join(nphli))
			reply(type,source,rep)	
		else:
			reply(type,source,u'Phrases not found!')

#--------------------End Of Local Functions----------
	
	phrases = get_pai_phrases(groupchat)
	tophs = len(phrases)
	
	if parameters:
		spltdp = parameters.split(' ',1)
		nphrase = spltdp[0]
		
		if len(spltdp) == 1:
			if '-' in nphrase:
				nphrase = nphrase.split('-',1)
				nphrase = [li for li in nphrase if li != '']
				
				if len(nphrase) == 2:
					if nphrase[0].isdigit():
						stn = int(nphrase[0])
						
						if not stn:
							reply(type,source,u'Invalid syntax!')
							return
					else:
						phrases_find(type,source,phrases,parameters)
						return

					if nphrase[1].isdigit():
						enn = int(nphrase[1])
						
						if enn > tophs:
							reply(type,source,u'Excess range!')
							return
					else:
						phrases_find(type,source,phrases,parameters)
						return							
									
					if stn > enn:
						reply(type,source,u'Invalid Range!')
						return									
					
					head = ''
					foot = ''	
							
					if stn >= 2 and stn != enn:
						head = u'[<---beginning---]\n\n'
					
					if enn < tophs and stn != enn:
						foot = u'\n\n[---ending--->]'
					elif enn == tophs and tophs == 10:
						foot = ''

					nphli = show_phrases(phrases,stn-1,enn)
					rep = u'List of phrases (total: %s):\n%s%s%s' % (tophs,head,'\n'.join(nphli),foot)
					reply(type,source,rep)
			else:
				if nphrase.isdigit():
					if int(nphrase) != 0 and int(nphrase) <= tophs:
						nphrase = int(nphrase)
						
						nphli = show_phrases(phrases,nphrase-1,nphrase)
						rep = u'Phrases (total: %s):\n%s' % (tophs,'\n'.join(nphli))
						reply(type,source,rep)	
					else:
						reply(type,source,u'Invalid syntax!')
				else:
					phrases_find(type,source,phrases,nphrase)
		else:
			phrases_find(type,source,phrases,parameters)
	else:
		foot = ''	
		
		if tophs > 10:
			foot = u'\n\n[---ending--->]'
			
		nphli = show_phrases(phrases)
		
		if nphli:
			rep = u'List of phrases (total: %s):\n%s%s' % (tophs,'\n'.join(nphli),foot)
		else:
			rep = u'List phrases is empty!'
		
		reply(type,source,rep)

#-------------------------------------Handlers---------------------------------------------

register_command_handler(handler_pai_control, COMM_PREFIX+'pai', ['fun','muc','all','*'], 30, 'Enables or disables chatter bot, that displays random phrases in messages users. Without parameters shows the current value.', COMM_PREFIX+'pai <1|0>', [COMM_PREFIX+'pai 1',COMM_PREFIX+'pai 0',COMM_PREFIX+'pai'])
register_command_handler(handler_pai_learn, COMM_PREFIX+'pai_learn', ['fun','muc','all','*'], 30, 'Enables or disables learning chatter bot, i.e saves the message in the database of users, which reacts. Without parameters shows the current value.', COMM_PREFIX+'pai_learn <1|0>', [COMM_PREFIX+'pai_learn 1',COMM_PREFIX+'pai_learn 0',COMM_PREFIX+'pai_learn'])
register_command_handler(handler_pai_occ, COMM_PREFIX+'pai_occ', ['fun','muc','all','*'], 30, 'Sets the level of chatter bot in percentage from 0% to 100%, i.e The higher the value, the more the bot will talk. Without parameters shows the current value.', COMM_PREFIX+'pai_occ <0-100>', [COMM_PREFIX+'pai_occ 50',COMM_PREFIX+'pai_occ 10',COMM_PREFIX+'pai_occ'])
register_command_handler(handler_pai_think, COMM_PREFIX+'pai_think', ['fun','muc','all','*'], 30, 'Sets the time to think of phrases users from 3 to 100 seconds, i.e minimum time for reflection - 4 seconds. Without parameters shows the current value.', COMM_PREFIX+'pai_think <4-100>', [COMM_PREFIX+'pai_think 10',COMM_PREFIX+'pai_think 4',COMM_PREFIX+'pai_think'])
register_command_handler(handler_pai_ron, COMM_PREFIX+'pai_ron', ['fun','muc','all','*'], 30, 'Adds to the list of words which reacts bot, that is is interested in the bot to a particular topic. Add words must be separated by a space! Without this parameter displays a list.', COMM_PREFIX+'pai_ron [word1 word2 ... words]', [COMM_PREFIX+'pai_ron master',COMM_PREFIX+'pai_ron pai_ron Bots are good for conference',COMM_PREFIX+'pai_ron'])
register_command_handler(handler_pai_roff, COMM_PREFIX+'pai_roff', ['fun','muc','all','*'], 30, 'Adds to the list of words that ignores the bot, i.e topics that are not interested in the bot. If you add a nickname, it will ignore posts with this nickname. Add words must be separated by a space! Without this parameter displays a list.', COMM_PREFIX+'pai_roff [word1 word2 ... words]', [COMM_PREFIX+'pai_roff master',COMM_PREFIX+'pai_roff pai_ron Bots are good for conference',COMM_PREFIX+'pai_roff'])
register_command_handler(handler_pai_rond, COMM_PREFIX+'pai_rond', ['fun','muc','all','*'], 30, 'Deletes a word from the list of words which reacts bot, i.e bot no longer interested at this or that topic. Without parameters clears the list!', COMM_PREFIX+'pai_rond [слово]', [COMM_PREFIX+'pai_rond master',COMM_PREFIX+'pai_rond'])
register_command_handler(handler_pai_roffd, COMM_PREFIX+'pai_roffd', ['fun','muc','all','*'], 30, 'Deletes a word from the list of words that ignores the boat, i.e bot no longer ignore the message with these words. Without parameters clears the list!', COMM_PREFIX+'pai_roffd [слово]', [COMM_PREFIX+'pai_roffd master',COMM_PREFIX+'pai_roffd'])
register_command_handler(handler_pai_add, COMM_PREFIX+'pai_add', ['fun','muc','all','*'], 30, 'Adds a phrase as base, i.e phrase which the bot will respond to messages from users!', COMM_PREFIX+'pai_add <phrase>', [COMM_PREFIX+'pai_add That is good',COMM_PREFIX+'pai_add Ehehehe'])
register_command_handler(handler_pai_del, COMM_PREFIX+'pai_del', ['fun','muc','all','*'], 30, 'Removes a phrase from the base by its number. No parameters removes the last sentence, which the bot replied to the message, the user, in the current conference', COMM_PREFIX+'pai_del <id>', [COMM_PREFIX+'pai_del 10',COMM_PREFIX+'pai_del'])
register_command_handler(handler_pai_count, COMM_PREFIX+'pai_count', ['fun','muc','all','*'], 30, 'Shows the number of phrases in the database.', COMM_PREFIX+'pai_count', [COMM_PREFIX+'pai_count'])
register_command_handler(handler_pai_show, COMM_PREFIX+'pai_show', ['fun','muc','all','*'], 30, 'Lets you view it in the database. Without parameters displays the first 10 sentences, if more than 10, or all if they are less than 10 and 10 if they total 10. When you specify a number displays the phrase with that number. When specifying a range in the format <start>-<end> displays the phrase beginning with a specified boundary <start> and to the number specified boundary <end>. When referring to the text, trying to find it in the database in which there is overlap with the text, displays the first 10 found words.', COMM_PREFIX+'pai_show [<number>|<start>-<end>|<text>]', [COMM_PREFIX+'pai_show',COMM_PREFIX+'pai_show 4',COMM_PREFIX+'pai_show 3-8',COMM_PREFIX+'pai_show any'])

register_stage1_init(get_pai_state)
register_message_handler(handler_pai)