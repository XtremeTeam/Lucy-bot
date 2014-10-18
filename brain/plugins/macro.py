#===islucyplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  macro_plugin.py

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def macroadd_handler(type, source, parameters):
	pl = MACROS.parse_cmd(parameters)
	if (len(pl)<2):
		reply(type, source, u'there is not enough arguments')
		return
	else:
		if pl[1].split()[0] in COMMAND_HANDLERS or pl[1].split()[0] in MACROS.gmacrolist or pl[1].split()[0] in MACROS.macrolist[source[1]]:
			real_access = MACROS.get_access(pl[1].split()[0], source[1])
			if real_access < 0 and pl[1].split()[0] in COMMAND_HANDLERS:
				real_access = COMMANDS[pl[1].split()[0]]['access']
			else:
				pass
			if real_access:
				if not has_access(source, real_access, source[1]):
					reply(type, source, u'Was lost in day-dreams ]:->')
					return
		else:
			reply(type, source, u'I do not see a command inside the macro')
			return				
		MACROS.add(pl[0], pl[1], source[1])
		MACROS.flush()		
		reply(type, source, u'Has added')
	
def gmacroadd_handler(type, source, parameters):
	pl = MACROS.parse_cmd(parameters)
	if (len(pl)<2):
		rep = u'there is not enough arguments'
	else:
		MACROS.add(pl[0], pl[1])
		write_file('settings/macros.txt', str(MACROS.gmacrolist))
		rep = u'Has added'
	reply(type, source, rep)

def macrodel_handler(type, source, parameters):
	if parameters:
		MACROS.remove(parameters, source[1])
#		write_file('dynamic/'+source[1]+'macros.txt', str(MACROS.macrolist[source[1]]))
		MACROS.flush()
		rep = u'Has left'
	else:
		rep = u'there is not enough arguments'
	reply(type, source, rep)
	
def gmacrodel_handler(type, source, parameters):
	if parameters:
		MACROS.remove(parameters)
		write_file('settings/macros.txt', str(MACROS.gmacrolist))
		rep = u'Has killed'
	else:
		rep = u'there is not enough arguments'
	reply(type, source, rep)

def macroexpand_handler(type, source, parameters):
	if parameters:
		rep=MACROS.comexp(parameters, source)
		if not rep:
			rep = u'Not экспандится. It is not enough rights?'
	else:
		rep = u'there is not enough arguments'
	reply(type, source, rep)
	
def gmacroexpand_handler(type, source, parameters):
	if parameters:
		rep=MACROS.comexp(parameters, source, '1')
	else:
		rep = u'there is not enough arguments'
	reply(type, source, rep)

def macroinfo_handler(type, source, parameters):
	rep=''
	if parameters:
		try:
			if MACROS.macrolist[source[1]].has_key(parameters):
				rep = parameters+' -> '+MACROS.macrolist[source[1]][parameters]
		except:
			rep = u'there is no such macro present'
	elif parameters == 'allmac':
		rep += '\n'.join([x+' -> '+ MACROS.macrolist[source[1]][x] for x in MACROS.macrolist[source[1]]])
	if not rep:
		rep=u'It is poorly written'
	reply(type, source, rep)
	
def gmacroinfo_handler(type, source, parameters):
	rep=''
	if parameters:
		if MACROS.gmacrolist.has_key(parameters):
			rep = parameters+' -> '+MACROS.gmacrolist[parameters]
		else:
			rep = u'no such macro'
	elif parameters == 'allmac':
		rep += '\n'.join([x+' -> '+ MACROS.macrolist[x] for x in MACROS.macrolist])
	reply(type, source, rep)
	
def macrolist_handler(type, source, parameters):
	groupchat = source[1]
	is_gch = True
	
	if not GROUPCHATS.has_key(groupchat):
		is_gch = False
	
	rep,dsbll,dsblg,glist,llist=u'List of aliases: ',[],[],[],[]
	tglist = MACROS.gmacrolist.keys()
	
	if is_gch:
		if MACROS.macrolist[groupchat]:
			for macro in MACROS.macrolist[groupchat].keys():
				if macro in COMMOFF[groupchat]:
					dsbll.append(macro)
				else:
					llist.append(macro)
			dsbll.sort()
			llist.sort()
			if llist:
				rep += u'\nLOCAL\n'+', '.join(llist)
			if dsbll:
				rep+=u'\n\nThe following local aliases are disabled in this conference:\n'+', '.join(dsbll)
		else:
			rep+=''
	
		for macro in tglist:
			if macro in COMMOFF[groupchat]:
				dsblg.append(macro)
			else:
				glist.append(macro)
		dsblg.sort()
		glist.sort()
	else:
		dsblg = []
		tglist.sort()
		glist = tglist
	
	if glist:
		rep+=u'\nGLOBAL\n'+', '.join(glist)
	else:
		rep+=''
	
	if dsblg:
		rep+=u'\n\n The following global aliases are disabled in this conference:\n'+', '.join(dsblg)

	if type=='public':
		reply(type, source, u'Look in private!')
	if glist or llist:
		reply('private', source, rep)
	elif not glist and not llist:
		rep='List of aliases is empty!'
		reply('private', source, rep)
	
def macroaccess_handler(type, source, parameters):
	if parameters:
		args,access = parameters.split(' '),10
		if len(args)==2:
			macro = args[0]
			if macro in COMMAND_HANDLERS:
				if not user_level(source,source[1])==100:
					reply(type,source,u'Was lost in day-dreams ]:->')
					return
				else:
					pass
			elif macro in MACROS.gmacrolist or macro in MACROS.macrolist[source[1]]:
				real_access = MACROS.get_access(macro, source[1])
				if real_access < 0:
					pass
				else:
					if not has_access(source, real_access, source[1]):
						reply(type,source,u'Was lost in day-dreams ]:->')
						return
			try:
				access = int(args[1])
			except:
				reply(type,source,u'invalid')
				return
			MACROS.give_access(macro,access,source[1])
			reply(type,source,u'Has given')
			time.sleep(1)
			MACROS.flush()
		else:
			reply(type,source,u'That for delirium?')
			
def gmacroaccess_handler(type, source, parameters):
	if parameters:
		args = parameters.split(' ')
		if len(args)==2:
			macro = args[0]
			access = args[1]
			MACROS.give_access(macro,access)
			reply(type,source,u'дал')
			time.sleep(1)
			write_file('settings/macroaccess.txt', str(MACROS.gaccesslist))
		else:
			reply(type,source,u'That for delirium?')


register_command_handler(macroadd_handler, 'macroadd', ['admin','macro','all'], 20, 'To add macro. the macro itself should be concluded in apostrophes `` !!!', 'macroadd [The name] [`macro`]', ['macroadd Glitch `To tell /me Has thought, that all is well`'])
register_command_handler(gmacroadd_handler, 'gmacroadd', ['superadmin','macro','all'], 100, 'to add a global macro. the macro itself should be concluded in apostrophes `` !!!', 'gmacroadd [name] [`macro`]', ['gmacroadd Glitch `To tell /me Has thought, that all is well`'])

register_command_handler(macrodel_handler, 'macrodel', ['admin','macro','all'], 20, 'delete a macro.', 'macrodel [name]', ['macrodel glitch'])
register_command_handler(gmacrodel_handler, 'gmacrodel', ['superadmin','macro','all'], 100, 'to delete a global macro.', 'macrodel [name of macro]', ['macrodel glitch'])

register_command_handler(macroexpand_handler, 'macroexp', ['admin','macro','info','all'], 20, 'To develop macro, i.e. to look at ready macro in a crude kind.', 'macroexp [name] [Parameters]', ['macroexp administrator bot'])
register_command_handler(gmacroexpand_handler, 'gmacroexp', ['superadmin','macro','info','all'], 100, 'To develop global macro, i.e. to look at ready macro in a crude kind.', 'gmacroexp [name of macro] [Parameters]', ['gmacroexp administrator bot'])

register_command_handler(macroinfo_handler, 'macroinfo', ['admin','macro','info','all'], 20, 'to view a certain macro.', 'macroinfo [name]', ['macroinfo glitch','macroinfo allmac'])
register_command_handler(gmacroinfo_handler, 'gmacroinfo', ['superadmin','macro','info','all'], 100, 'to view a global macro (any), т.е. to look at all macros write "allmac" .', 'macroinfo [name]', ['macroinfo glitch','macroinfo allmac'])

register_command_handler(macrolist_handler, 'macrolist', ['help','macro','info','all'], 10, 'view all macros. sent to private', 'macrolist', ['macrolist'])

register_command_handler(macroaccess_handler, 'macroaccess', ['admin','macro','all'], 20, 'To change access to certain macro.', 'macroaccess [macro] [access]', ['macroaccess glitch 10'])
register_command_handler(gmacroaccess_handler, 'gmacroaccess', ['superadmin','macro','all'], 100, 'to change access to a certain global macro (any).', 'gmacroaccess [macro] [access]', ['macroaccess glitch 20'])
