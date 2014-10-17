#===islucyplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  ping_plugin.py

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Modifications Copyright © 2009 Lubagov <lubagov@yandex.ru>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#   aff_plugin.py
#   Modified by KiDo
#   best-rapper@qip.ru
#   best-rapper@jabber.org
#   konvict_massari@yahoo.com
#   www.facebook.com/KiDo.Konvict
#   www.twitter.com/KiDo3Konvict

acheck = 0
aff_pending=[]
def handler_aff(typ, source, parameters):
	aff_list={u"moder":{'role':'moderator'},u"member": {'affiliation':'member'},u"participant":{'role':'participant'},u"ban": {'affiliation':'outcast'},u'owner':{'affiliation':'owner'},u'admin':{'affiliation':'admin'}}
	splitdata = parameters.strip().split()
	if len(splitdata) == 1:
                affl = parameters
                jid = 1
        else:
                if parameters.split()[1] == 'clear':
                        affl = parameters.split()[0]
                        global acheck
                        jid = 'clear'
                else:
                        affl = parameters.split()[0]
                        jid = parameters.split()[1]
	if not aff_list.has_key(affl):
		reply(typ, source, u"i dont know that word!")
		return
	groupchat=source[1]
	id = 'a'+str(random.randrange(1, 1000))
	globals()['aff_pending'].append(id)
	iq=xmpp.Iq('get',to=groupchat,queryNS=xmpp.NS_MUC_ADMIN,xmlns=None)
	iq.getQueryChildren().append(xmpp.Protocol('item',attrs=aff_list[affl]))
	iq.setID(id)
	param=''
	if jid == 1:
                JCON.SendAndCallForResponse(iq, handler_aff_answ,{'mtype': typ, 'source': source, 'param': param})
                return
        elif jid == 'clear':
                reply(typ, source, u'Are you sure you want to remove all the JIDs in the '+affl+u'list?')
                for i in range(1, 60):
                        time.sleep(1)
                if acheck == 1:
                        JCON.SendAndCallForResponse(iq, handler_clear_list,{'mtype': typ, 'source': source, 'param': param})
                else:
                        reply(typ, source, u'OK, I won\'t remove it, But don\'t call me again if you\'re not sure.')
        else:
                JCON.SendAndCallForResponse(iq, handler_aff_inlist,{'mtype': typ, 'source': source, 'param': param, 'jid': jid})
                return
                

def handler_aff_answ(coze, res, mtype, source, param):
	id = res.getID()
	if id in globals()['aff_pending']:
		globals()['aff_pending'].remove(id)
	else:
		print 'someone is doing wrong...'
		return
	if res:
		if res.getType() == 'result':
		#-=
			aa=res.getTag("query")
                        if aa==None:
                                rep=u"fatal error, unable to query"
                        else:
                                m=aa.getTags("item")
                                if len(m)==0:
                                        rep=u"empty"
                                else:
                                        rep=""
                                        for t in m:
                                                ats=t.getAttrs()
                                                if ats.has_key("jid"):
                                                        rep+=t["jid"]+" "
                                                if ats.has_key("affiliation"):
                                                        rep+=t["affiliation"]+" "
                                                if ats.has_key("role"):
                                                        rep+=t["role"]+" "
                                                reas=t.getTag("reason")
                                                if reas!= None:
                                                        dt=reas.getData()
                                                        if dt!=None:
                                                                rep+=dt+" "
                                                rep+="\n"
		#-=
		else:
			rep = u'i can not!!!'
	if mtype=="public":
		reply(mtype, source, u"sent to private")
	reply("private", source, rep)

def handler_clear_list(coze, res, mtype, source, param):
	id = res.getID()
	if id in globals()['aff_pending']:
		globals()['aff_pending'].remove(id)
	else:
		print 'someone is doing wrong...'
		return
	if res:
		if res.getType() == 'result':
		#-=
			aa=res.getTag("query")
                        if aa==None:
                                rep=u"fatal error, unable to query"
                        else:
                                m=aa.getTags("item")
                                if len(m)==0:
                                        rep=u"empty"
                                else:
                                        rep=""
                                        for t in m:
                                                ats=t.getAttrs()
                                                if ats.has_key("jid"):
                                                        rep+=t["jid"]
                                                #if ats.has_key("affiliation"):
                                                #        rep+=t["affiliation"]+" "
                                                #if ats.has_key("role"):
                                                #        rep+=t["role"]+" "
                                                #reas=t.getTag("reason")
                                                #if reas!= None:
                                                #        dt=reas.getData()
                                                #        if dt!=None:
                                                #                rep+=dt+" "
                                                rep+="\n"
		#-=
		else:
			rep = u'i can not!!!'
	if mtype=="public":
		reply(mtype, source, u"Clearing started...")
	jid = ''
	for i in rep:
                if i != '\n':
                        jid+= i
                else:
                        reply(mtype, source, jid)
                        iq = xmpp.Iq('set')
                        iq.setID('ulti_ban')
                        iq.setTo(source[1])
                        query = xmpp.Node('query')
                        query.setNamespace('http://jabber.org/protocol/muc#admin')
                        query.addChild('item', {'jid':jid, 'affiliation':'none'})
                        iq.addChild(node=query)
                        JCON.SendAndCallForResponse(iq, handler_ban_answ, {'type': type, 'source': source})
                        jid = ''
   
def handler_ban_answ(coze, res, type, source):
   if res:
      if res.getType() == 'result':
         reply(type, source, u'Done.')
      else:
         
         reply(type, source, u'Error. Try again, or ban less quantity.')


def handler_aff_inlist(coze, res, mtype, source, param, jid):
	id = res.getID()
	if id in globals()['aff_pending']:
		globals()['aff_pending'].remove(id)
	else:
		print 'someone is doing wrong...'
		return
	if res:
		if res.getType() == 'result':
		#-=
			aa=res.getTag("query")
                        if aa==None:
                                rep=u"fatal error, unable to query"
                        else:
                                m=aa.getTags("item")
                                if len(m)==0:
                                        rep=u"empty"
                                else:
                                        rep=""
                                        for t in m:
                                                ats=t.getAttrs()
                                                if ats.has_key("jid"):
                                                        rep+=t["jid"]+" "
                                                if ats.has_key("affiliation"):
                                                        rep+=t["affiliation"]+" "
                                                if ats.has_key("role"):
                                                        rep+=t["role"]+" "
                                                reas=t.getTag("reason")
                                                if reas!= None:
                                                        dt=reas.getData()
                                                        if dt!=None:
                                                                rep+=dt+" "
                                                rep+="\n"
		#-=
		else:
			rep = u'i can not!!!'
	if jid in rep:
                reply("private", source, u'Yes')
        else:
                reply("private", source, u'No')


def acheck_message(type, source, parameters):
        if user_level(source,source[1]) >= 30 and parameters.lower() == 'yes':
                global acheck
                acheck = 1
        elif user_level(source,source[1]) >= 30 and parameters.lower() == 'no':
                global acheck
                acheck = 0
                
register_message_handler(acheck_message)
register_command_handler(handler_aff, COMM_PREFIX+'aff', ['aff','en','all'], 20, 'show affiliation list in the current conference.\nOr type aff <list> clear to remove all JIDs in that list', 'aff <type>', ['aff owner','aff admin','aff moderator','aff member','aff participant','aff outcast','aff member clear'])
register_command_handler(handler_aff, COMM_PREFIX+'inlist', ['aff','en','all'], 20, 'show affiliation list in the current conference', 'aff <type>', ['aff owner','aff admin','aff moderator','aff member','aff participant','aff outcast'])
