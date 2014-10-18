#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  disco_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  Help Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Modifications Copyright © 2009 wd/lotusfeet <dao/yoga>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

disco_pending=[]

def handler_disco(type, source, parameters):
	if parameters:
		parst=parameters.split(' ', 2)
		stop,srch,tojid='','',parst[0]
		if len(parst)==1:
			if type == 'public': stop=10
			else: stop=50
			srch=None
		elif len(parst)>1:
			try:
				stop=int(parst[1])
				try:
					srch=parst[2]
				except:
					srch=None
			except:
				srch=parst[1]
				if type == 'public': stop=10
				else: stop=50
			if type == 'public':
				if stop>50: stop='50'
			else:
				if stop>250: stop='250'			
		iq = xmpp.Iq('get')
		id='dis'+str(random.randrange(1, 9999))
		globals()['disco_pending'].append(id)
		iq.setID(id)
		query=iq.addChild('query', {}, [], xmpp.NS_DISCO_ITEMS)
		if len(tojid.split('#'))==2:
			query.setAttr('node',tojid.split('#')[1])
			iq.setTo(tojid.split('#')[0])
		else:
			iq.setTo(tojid)
		JCON.SendAndCallForResponse(iq, handler_disco_ext, {'type': type, 'source': source, 'stop': stop, 'srch': srch, 'tojid': tojid})
	else:
		reply(type,source,u'And?')
		return

def handler_disco_ext(coze, res, type, source, stop, srch, tojid):
	disco=[]
	rep,trig='',0
	id=res.getID()
	if id in globals()['disco_pending']:
		globals()['disco_pending'].remove(id)
	else:
		print 'someone is doing wrong...'
		reply(type, source, u'Вглюкнуло...')
		return
	if res:
		if res.getType() == 'result':
			props=res.getQueryChildren()
			for x in props:
				att=x.getAttrs()
				if att.has_key('name'):
					try:
						st=re.search('^(.*) \((.*)\)$', att['name']).groups()
						disco.append([st[0],att['jid'],st[1]])
						trig=1
					except:
						if not trig:
							temp=[]
							if att.has_key('name'):
								temp.append(att['name'])
							if att.has_key('jid') and not tojid.count('@'):
								temp.append(att['jid'])
							if att.has_key('node'):
								temp.append(att['node'])
							disco.append(temp)
				else:
					disco.append([att['jid']])
			if disco:
				handler_disco_answ(type,source,stop,disco,srch)
			else:
				reply(type, source, u'disco empty!')
			return
		else:
			rep = u'i can not!'
	else:
		rep = u'sorry...'
	reply(type, source, rep)
	
	
def handler_disco_answ(type,source,stop,disco,srch):
	total=0
	if total==stop:
		reply(type, source, u'total '+str(len(disco))+u' items.')
		return
	rep,dis,disco = u'disco routined:\n',[],sortdis(disco)
	for item in disco:
		if len(item)==3:
			total+=1
			if srch:
				if srch.endswith('@'):
					if item[1].startswith(srch):
						dis.append(str(total)+u') '+item[0]+u' ['+item[1]+u']: '+str(item[2]))
						break
					else:
						continue
				else:
					if not item[0].count(srch) and not item[1].count(srch):
						continue
			dis.append(str(total)+u') '+item[0]+u' ['+item[1]+u']: '+str(item[2]))
			if len(dis)==stop:
				break
		elif len(item)==2:
			total+=1
			if srch:
				if not item[0].count(srch) and not item[1].count(srch):
					continue
			dis.append(str(total)+u') '+item[0]+u' ['+item[1]+u']')
			if len(dis)==stop:
				break
		else:
			total+=1
			if srch:
				if not item[0].count(srch):
					continue
			dis.append(str(total)+u') '+item[0])
			if len(dis)==stop:
				break
	if dis:
		if len(disco)!=len(dis):
			dis.append(u'total '+str(len(disco))+u' items.')
	else:
		rep=u'disco empty!'
	reply(type, source, rep+u'\n'.join(dis))
	
def sortdis(dis):
	disd,diss,disr=[],[],[]
	for x in dis:
		try:
			int(x[2])
			disd.append(x)
		except:
			diss.append(x)
	disd.sort(lambda x,y: int(x[2]) - int(y[2]))
	disd.reverse()
	diss.sort()
	for x in disd:
		disr.append(x)
	for x in diss:
		disr.append(x)
	return disr
	
disco=[]

register_command_handler(handler_disco, 'disco', ['muc','info','all','*'], 10, 'Shows results of the review services for the specified JID.\nIt is also possible to browse on point (node). Request format jid#node.\nSecond or third (if the limiter is also given number of) option - search. Searches for a given word in the JID and description disco. If the search word to specify the name of the conference until the server name (example qwerty@), it will place the conference in overall rankings.\nIn the general chat can give max 50 results, without specifying the count - 10.\nIn private may give max 250, without specifying count 50.', 'disco <server> <count results> <search string>', ['disco smart.web.id','disco conference.jsmart.web.id 5','disco conference.jsmart.web.id qwerty','disco conference.jsmart.web.id 5 qwerty','disco conference.jsmart.web.id qwerty@', 'disco jsmart.web.id#services'])