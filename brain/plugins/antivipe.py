#===islucyplugin===
# -*- coding: utf-8 -*-

# Endless / talisman rev 79+
# version 1.0
# Ported from AntiVipe bot by Avinar (avinar@xmpp.ru)

# licence show in another plugins ;)

AVIPES={}
AVSERVERS=['xtreme.im', 'jabber.ru', 'xmpp.ru', 'jabbers.ru', 'xmpps.ru', 'qip.ru', 'talkonaut.com', 'jabbus.org', 'jabber.org','gtalk.com','jabber.cz','jabberon.ru','jabberid.org','linuxoids.net','jabber.kiev.ua','jabber.ufanet.ru','jabber.corbina.ru']

def order_unban_v(groupchat, jid):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('ban'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	query.addChild('item', {'jid':jid, 'affiliation':'none'})
	iq.addChild(node=query)
	JCON.send(iq)
	
def order_ban_v(groupchat, jid):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('ban'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'jid':jid, 'affiliation':'outcast'})
	ban.setTagData('reason', u'dicurigai menyerang dengan dengan metode wipe!')
	iq.addChild(node=query)
	JCON.send(iq)
		
def get_serv(serv):
	if serv.count('@'):
		serv=serv.split('@')[1]
	if serv.count('/'):
		serv=serv.split('/')[0]
	return serv		
		
def findPresenceItemV(node):
	for p in [x.getTag('item') for x in node.getTags('x',namespace='http://jabber.org/protocol/muc#user')]:
              if p != None:
                      return p
        return None


		
def avipe_prs(prs):
	ptype = prs.getType()
	if ptype == 'unavailable' and prs.getStatusCode() == '303':
		nick = prs.getNick()
		fromjid = prs.getFrom()
		groupchat = fromjid.getStripped()		
		afl=prs.getAffiliation()
		role=prs.getRole()
		avipe_join(groupchat, nick, afl, role)


def avipe_join(groupchat, nick, afl, role):		
	global AVIPES
	if not AVIPES.has_key(groupchat):
		return
	
	if afl != 'none':
		return
	jid = get_true_jid(groupchat+'/'+nick)		
	if not jid or jid.count('@xtreme.im'):
		return
	
	global INFO	
	ttime=int(time.time())	
	if ttime - INFO['start'] < 60:	
		return
	
	if (ttime - AVIPES[groupchat]['ltime']) > 20:
		AVIPES[groupchat]['ltime']=ttime
		AVIPES[groupchat]['num']=0
		AVIPES[groupchat]['jids']=[jid]
		return
	AVIPES[groupchat]['num']+=1
	AVIPES[groupchat]['jids'].append(jid)
	joined=AVIPES[groupchat]['jids']
	
	global GROUPCHATS
	if len(joined) > 2:
		AVIPES[groupchat]['ltime']=ttime
		x=len(joined)
		if (get_serv(joined[x-2]) == get_serv(joined[x-1])) and (get_serv(joined[x-3]) == get_serv(joined[x-1])):    #and joined[x-2] != joined[x-1]:
			serv=get_serv(joined[x-2])
			if not serv in AVSERVERS:			
				node='<item affiliation="outcast" jid="'+serv+u'"><reason>dicurigai menyerang dengan dengan metode wipe.</reason></item>'
				node=xmpp.simplexml.XML2Node(unicode('<iq from="'+JID+'/'+RESOURCE+'" id="ban1" to="'+groupchat+'" type="set"><query xmlns="http://jabber.org/protocol/muc#admin">'+node+'</query></iq>').encode('utf8'))
				JCON.send(node)						
			node=''
			for nick in GROUPCHATS[groupchat].keys():
				if get_serv(get_true_jid(groupchat+'/'+nick)) == serv and GROUPCHATS[groupchat][nick]['ishere']:
					node+='<item role="none" nick="'+nick+u'"><reason>dicurigai menyerang dengan dengan metode wipe.</reason></item>'
			if node:
				node=xmpp.simplexml.XML2Node(unicode('<iq from="'+JID+'/'+RESOURCE+'" id="kick1" to="'+groupchat+'" type="set"><query xmlns="http://jabber.org/protocol/muc#admin">'+node+'</query></iq>').encode('utf8'))
				JCON.send(node)

			if not serv in AVSERVERS:
				for nick in GROUPCHATS[groupchat].keys():
					if user_level(groupchat+'/'+nick, groupchat) > 19:
						#if GROUPCHATS[groupchat][nick]['status'] in [u'online',u'chat',u'away']:
						msg(groupchat+'/'+nick, u'Peringatan! Server '+serv+u' masuk antrian daftar ban antivipe!')

	if AVIPES[groupchat]['num'] > 4:
		order_ban_v(groupchat, jid)
		threading.Timer(60, order_unban_v,(groupchat, jid, )).start()
		

def avipe_call(type, source, parameters):
	global AVIPES
	PATH='settings/'+source[1]+'/antivipe.txt'
	parameters=parameters.strip().lower()
	if parameters:
		if check_file(source[1],'antivipe.txt'):
			if parameters=='off' or parameters=='0':# or parameters==u'вкл':
				write_file(PATH, 'off')
				AVIPES[source[1]]={'ltime':0, 'num':0, 'jids': []}
				reply(type, source, u'fungsi antivipe dinon-aktifkan!')
			elif parameters=='on' or parameters=='1':# or parameters==u'выкл':
				write_file(PATH, 'on')
				if AVIPES.has_key(source[1]):
					del AVIPES[source[1]]
				reply(type, source, u'fungsi antivipe diaktifkan!')
			else:
				reply(type, source, u'baca "help antivipe"!')
	else:
		if not AVIPES.has_key(source[1]):
			reply(type, source, u'anda telah menon-aktifkan fungsi antivipe!')
		else:
			reply(type, source, u'anda telah mengaktifkan fungsi antivipe!')


def avipe_init(groupchat):
	if check_file(groupchat,'antivipe.txt'):
		if not read_file('settings/'+groupchat+'/antivipe.txt')=='off':
			AVIPES[groupchat]={'ltime':0, 'num':0, 'jids': []}

	
		
register_presence_handler(avipe_prs)
register_join_handler(avipe_join)
register_command_handler(avipe_call, COMM_PREFIX+'antivipe', ['all', 'admin'], 100, 'aktif/non-aktif fungsi perlindungan terhadap vipe attacks.\nSetting default adalah OFF.', 'antivipe [<1/on/||0/off/]', ['antivipe on','antivipe off'])
register_stage1_init(avipe_init)	




"""	
	global GROUPCHATS
	if len(joined) > 2:
		x=len(joined)
		if (get_serv(joined[x-2]) == get_serv(joined[x-1])) and (get_serv(joined[x-3]) == get_serv(joined[x-1])):                   #and joined[x-2] != joined[x-1]:
			serv=get_serv(joined[x-2])
			if not serv in AVSERVERS:			
				node='<item affiliation="outcast" jid="'+serv+u'"><reason>Подозрение на вайп атаку.</reason></item>'
				for nick in GROUPCHATS[groupchat].keys():
					if get_serv(get_true_jid(groupchat+'/'+nick)) == serv and GROUPCHATS[groupchat][nick]['ishere']:
						print nick,
						node+='<item role="none" nick="'+nick+u'"><reason>Подозрение на вайп атаку.</reason></item>'				
				
				node=xmpp.simplexml.XML2Node(unicode('<iq from="'+USERNAME+'@'+SERVER+'/'+RESOURCE+'" id="ban1" to="'+groupchat+'" type="set"><query xmlns="http://jabber.org/protocol/muc#admin">'+node+'</query></iq>').encode('utf8'))
				JCON.send(node)						
				for nick in GROUPCHATS[groupchat].keys():
					if user_level(groupchat+'/'+nick, groupchat) > 19:
						if GROUPCHATS[groupchat][nick]['status'] in [u'online',u'chat',u'away']:
							msg(groupchat+'/'+nick, u'Внимание! Сервер '+serv+u' занесен в бан лист!')
"""
