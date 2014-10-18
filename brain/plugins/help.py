#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin plugin
#  help.py

#  Initial Copyright © 2013-2014 x-team <x-team.im>


#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def handler_help_help(type, source, parameters):
	groupchat = source[1]
	
	ctglist = []
	if parameters and COMMANDS.has_key(parameters.strip()):
		rep = COMMANDS[parameters.strip()]['desc'].decode("utf-8") + u'\nCategories: '
		for cat in COMMANDS[parameters.strip()]['category']:
			ctglist.append(cat)
		rep += ', '.join(ctglist).decode('utf-8')+u'\nUse: ' + COMMANDS[parameters.strip()]['syntax'].decode("utf-8") + u'\nExample:'
		for example in COMMANDS[parameters]['examples']:
			rep += u'\n  >  ' + example.decode("utf-8")
		rep += u'\nNecessary level of access: ' + str(COMMANDS[parameters.strip()]['access'])
		
		if GROUPCHATS.has_key(groupchat):
			if parameters.strip() in COMMOFF[groupchat]:
				rep += u'\nThis command has been turned off in this conference!'
			else:
				pass
	else:
		rep = u'Write a word "%scommands" (without quotation marks), to get the list of commands, "%shelp <commands without "%s">" for the receipt of help on a command, %salias_list for a list of aliases, and %salias_acc <alias> to obtain the level of access to certain local aliases and %sgalias_acc <alias> to obtain the level of access to a specific global alias.'
				
	reply(type, source, rep)

def handler_help_commands(type, source, parameters):
	date=time.strftime('%d %b %Y (%a)', time.gmtime()).decode('utf-8')
	groupchat=source[1]
	if parameters:
		rep,dsbl = [],[]
		total = 0
		param=parameters.encode("utf-8")
		catcom=set([((param in COMMANDS[x]['category']) and x) or None for x in COMMANDS]) - set([None])
		if not catcom:
			reply(type,source,u'Please write the command again')
			return
		for cat in catcom:
			if has_access(source, COMMANDS[cat]['access'],groupchat):
				if groupchat in COMMOFF:
					if cat in COMMOFF[groupchat]:
						dsbl.append(cat)
					else:
						rep.append(cat)
						total += 1
				else:
					rep.append(cat)
					total += 1					
		if rep:
			if type == 'public':
				reply(type,source,u'Messeged you in private')
			rep.sort()
			answ=u'List of commands is in a category "%s" on %s (total: %s):\n\n%s.' %(parameters,date,total,', '.join(rep))
			if dsbl:
				dsbl.sort()
				answ+=u'\n\nThe followings commands has been turned off in this conference (total: %s):\n\n%s.' %(len(dsbl),', '.join(dsbl))
			reply('private', source,answ)
		else:
			reply(type,source,u'You do not have the right permissions')
	else:
		cats = set()
		
		for x in [COMMANDS[x]['category'] for x in COMMANDS]:
			cats = cats | set(x)
			
		qcats = len(cats)
		cats = ', '.join(cats).decode('utf-8')
		
		if type == 'public':
			reply(type,source,u'Look in your private!')

		reply('private', source, u'List of categories on %s (total: %s):\n\n%s.\n\no view a list of commands contained in the category, type "%scommands <category>" without the quotation marks, example "%scommands *"' % (date,qcats,cats))
		
register_command_handler(handler_help_help, 'help', ['help','info','all','*'], 0, 'Show detail information about a certain command.', 'help [command]', ['help', 'help ping'])
register_command_handler(handler_help_commands, 'commands', ['help','info','all','*'], 0, 'Shows the list of all of categories of commands. At the query of category shows the list of commands being in it.', 'commands [category]', ['commands','commands *'])