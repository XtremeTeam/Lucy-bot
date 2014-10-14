#===islucyplugin===
# -*- coding: utf-8 -*-



#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

MSUBS_QUERY = 0

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

def parse_subs_par(params):
	jid = ''
	name = ''
	access = ''
	
	if params:
		spltdp = params.strip().split(':',1)
		
		if len(spltdp) == 1:
			spltdp = spltdp[0].strip().split(' ',1)
			
			if len(spltdp) == 1:
				jid = spltdp[0]
			elif len(spltdp) == 2:
				jid = spltdp[0]
				name = spltdp[1]
		elif len(spltdp) == 2:
			jid_name = spltdp[0].strip()
			access = spltdp[1]
			spltdp = jid_name.split(' ',1)
			
			if len(spltdp) == 1:
				jid = spltdp[0]
			elif len(spltdp) == 2:
				jid = spltdp[0]
				name = spltdp[1]

	return (jid.strip(),name.strip(),access.strip())
		
def handler_subscribe(type, source, parameters):
	cont_jids = ROSTER.getItems()
	
	global MANUAL_SUBSCRIBE
	global GTEMP_SUBS_NAME
	global MSUBS_QUERY
	MANUAL_SUBSCRIBE = 1
	MSUBS_QUERY = 1
	
	if parameters:
		parsed_par = parse_subs_par(parameters)
		jid = parsed_par[0]
		name = parsed_par[1]
		access = parsed_par[2]
		
		if check_jid(jid):
			if jid in cont_jids:
				gsubs = ROSTER.getSubscription(jid)
				
				if gsubs != 'both':
					if not name:
						name = jid.split('@',1)[0]
					
					GTEMP_SUBS_NAME = name
					ROSTER.Subscribe(jid)
					
					if access and access.isdigit():
						change_access_perm_glob(jid, int(access))
					else:
						change_access_perm_glob(jid, 11)
						
					rep = u'Contact %s sent an authorization request!' % (jid)
					reply(type, source, rep)
				else:
					cont_groups = ROSTER.getGroups(jid)
					
					if not 'bot-users' in cont_groups:
						old_name = ROSTER.getName(jid)
						
						if old_name:
							name = old_name
						elif not name:
							name = jid.split('@',1)[0]
							
						GTEMP_SUBS_NAME = name	
						ROSTER.setItem(jid,GTEMP_SUBS_NAME,['bot-users'])
						
						if access and access.isdigit():
							change_access_perm_glob(jid, int(access))
						else:
							change_access_perm_glob(jid, 11)
						
						rep = u'Contatc %s already in the roster bot, but moved to the group bot-users!' % (jid)
						reply(type, source, rep)
					else:
						rep = u'Contact %s already in the roster bot and authorized!' % (jid)
						reply(type, source, rep)
			else:
				if not name:
					name = jid.split('@',1)[0]
				
				if access and access.isdigit():
					change_access_perm_glob(jid, int(access))
				else:
					change_access_perm_glob(jid, 11)
				
				GTEMP_SUBS_NAME = name
				ROSTER.Subscribe(jid)
							
				rep = u'Contact %s added to the roster of a bot and he sent an authorization request!' % (jid)
				reply(type, source, rep)
		else:
			reply(type, source, u'Invalid syntax!')
	else:
		reply(type, source, u'Invalid syntax!')
		
def handler_usubscribe(type, source, parameters):
	cont_jids = ROSTER.getItems()
	
	global MANUAL_USUBSCRIBE
	MANUAL_USUBSCRIBE = 1
	
	if parameters:
		if check_jid(parameters):
			ajid = parameters
			
			if ajid in cont_jids:
				gsubs = ROSTER.getSubscription(ajid)			
				
				if gsubs == 'both':
					if 'bot-users' in ROSTER.getGroups(ajid):
						change_access_perm_glob(ajid)
					
					ROSTER.Unsubscribe(ajid)
					ROSTER.delItem(ajid)
				else:
					ROSTER.delItem(ajid)
					
				rep = u'Subscription and contact %s removed from the roster of bot!' % (ajid)
				reply(type, source, rep)	
			else:
				rep = u'Contact %s not found in the roster of bot!' % (ajid)
				reply(type, source, rep)
		else:
			reply(type, source, u'Invalid syntax!')
	else:
		reply(type, source, u'Invalid syntax!')		
		
register_command_handler(handler_subscribe, COMM_PREFIX+'subscribe', ['roster','superadmin','all','*'], 100, ' Allows you to add a contact from the roster of bot and sends the contact request authorization.', COMM_PREFIX+'subscribe <jid [name][:access]>', [COMM_PREFIX+'subscribe guy@jsmart.web.id',COMM_PREFIX+'subscribe guy@jsmart.web.id: 20',COMM_PREFIX+'subscribe guy@jsmart.web.id Friend',COMM_PREFIX+'subscribe guy@jsmart.web.id Friend: 80'])
register_command_handler(handler_usubscribe, COMM_PREFIX+'usubscribe', ['roster','superadmin','all','*'], 100, 'Allows you to delete a contact from the roster and the subscription of bot.', COMM_PREFIX+'usubscribe <jid>', [COMM_PREFIX+'usubscribe guy@jsmart.web.id'])