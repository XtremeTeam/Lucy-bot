#===istalismanplugin===
# -*- coding: utf-8 -*-

#  BlackSmith plugin
#  plugin_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

OUT_COMMANDS = {}

def handler_out_list(type, source):
	if OUT_COMMANDS:
		repl = u'List of disabled commands: '+', '.join(sorted(OUT_COMMANDS.keys()))
	else:
		repl = u'No commands are disabled!'
	reply(type, source, repl)

def handler_command_out(type, source, body):
	if body:
		command = body.lower()
		if command in COMMANDS:
			OUT_COMMANDS[command] = COMMANDS[command]
			del COMMANDS[command]
			reply(type, source, u'Commands "%s" globally disabled' % (command))
		else:
			reply(type, source, u'No such command')
	else:
		handler_out_list(type, source)

def handler_from_out_com(type, source, body):
	if body:
		command = body.lower()
		if command in OUT_COMMANDS:
			COMMANDS[command] = OUT_COMMANDS[command]
			del OUT_COMMANDS[command]
			reply(type, source, u'Command "%s" is enabled now' % (command))
		else:
			reply(type, source, u'in the base of no return for this command')#No such command
	else:
		handler_out_list(type, source)

def handler_plug_list(type, source, body):
	ltc, tal, Ypl, Npl = [], [], [], []
	for Plugin in os.listdir(PLUGIN_DIR):
		Ext = Plugin[-3:].lower()
		if Ext == '.py':
			try:
				data = file('%s/%s' % (PLUGIN_DIR, Plugin)).read(20)
			except:
				data = '# |-| levaya shnyaga |-|'
			Plug = Plugin.split('_pl')
			if data.count('lytic'):
				ltc.append(Plug[0]); Ypl.append(Plugin)
			elif data.count('talis'):
				tal.append(Plug[0]); Ypl.append(Plugin)
			else:
				Npl.append(Plug[0])
	if body == 'get_valid_plugins':
		return sorted(Ypl)
	else:
		repl = ''
#		if ltc:
#			repl += u'\nДоступно %d плагинов BlackSmith бота:\n' % len(ltc)
#			repl += ', '.join(sorted(ltc))
		if tal:
			repl += u'\nAvailable %d Talisman plugins:\n' % len(tal)
			repl += ', '.join(sorted(tal))
		if Npl:
			repl += u'\nAttention! Unloadable %d plugins:\n' % len(Npl)
			repl += ', '.join(sorted(Npl))
		reply(type, source, repl)

def handler_load_plugin(type, source, body):
	if body:
		Plugin = '%s_plugin.py' % body.lower()
		if Plugin in handler_plug_list(type, source, 'get_valid_plugins'):
			try:
				execfile('%s/%s' % (PLUGIN_DIR, Plugin))
				repl = u'Plugin "%s" successfully loaded!' % (Plugin)
			except:
				exc = sys.exc_info()
				repl = u'Plugin "%s" failed to load!\nError: %s:\n%s' % (Plugin, exc[0].__name__, exc[1])
		else:
			repl = u'This plugin was not found in the list'
	else:
		repl = u'If you doubt - View the list (Command: pluglist)'
	reply(type, source, repl)

register_command_handler(handler_from_out_com, 'commadd', ['plugin','en','all'], 100,'Enable a command, that previously disabled.\nIf no parameters the bot will list disabled commands.', 'commadd [command]', ['commadd ping','commadd'])
register_command_handler(handler_command_out, 'commout', ['plugin','en','all'], 100,'Completely disable a command globally (can be enable by command loadpl or bot restart, or by comadd).\nNo parameters will show disabled commands.', 'commout [command]', ['comout ping','commout'])
register_command_handler(handler_plug_list, 'pluglist', ['plugin','en','all'], 40,'Shows a list of available plugins', 'pluglist', ['pluglist'])
register_command_handler(handler_load_plugin, 'loadpl', ['plugin','en','all'], 100,'Load one of the available plugins', 'loadpl [plugin_name]', ['loadpl admin'])
