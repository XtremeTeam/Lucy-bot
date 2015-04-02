#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Talisman module
#  macros.py

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


import random,string,re,os

def shell_esc(s):
	for c in [';', '&', '|', '`', '$', '\\', '#']:
		s = s.replace(c, '')
	return s

def xml_esc(s):
	s = s.replace('\'', '&apos;')
	s = s.replace('>', '&gt;')
	s = s.replace('<', '&lt;')
	s = s.replace('&', '&amp;')
	s = s.replace('\"', '&quot;')
	return s
	
def macro_get_rand(args, source):
	try:
		f=int(args[0])
		t=int(args[1])
		return str(random.randrange(f, t))
	except:
		return ''

def macro_shell_escape(args, source):
	return shell_esc(args[0])

def macro_xml_escape(args, source):
	return xml_esc(args[0])

def macro_context(args, source):
	arg = args[0]
	if arg == 'conf':
		return xml_esc(source[1])
	elif arg == 'nick':
		return xml_esc(source[2])
	elif arg == 'conf_jid':
		return xml_esc(source[0])
	else:
		return ''

def read_file(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def write_file(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()
		
class MacroCommands:
	commands={
	          'rand':         [2, macro_get_rand    ],
                  'shell_escape': [1, macro_shell_escape],
                  'xml_escape':   [1, macro_xml_escape  ],
		  'context':      [1, macro_context     ]
		 }
	
	def map_char(self, x, i):
		st=i['state']
		if i['esc']:
			i['esc']=False
			ret=i['level']
		elif x == '\\':
			i['esc']=True
			ret=0
		elif x == '%':
			i['state']='cmd_p'
			ret=0
		elif x == '(':
			if i['state'] == 'cmd_p':
				i['level']+=1
				i['state'] = 'args'
			ret=0
		elif x == ')':
			if i['state'] == 'args':
				i['state'] = 'null'
			ret=0
		else:
			if i['state'] == 'args':
				ret = i['level']
			else:
				i['state'] = 'null'
				ret = 0
		return ret

	def get_map(self, inp):
		i={'level': 0, 'state': 'null', 'esc': False}
		return [self.map_char(x, i) for x in list(inp)]
	
	def parse_cmd(self, me):
		i = 0
		m = self.get_map(me)
		args=[''] * max(m)
		while i<len(m):
			if m[i] != 0:
				args[m[i]-1]+=me[i]
			i+=1
		return args
		
	def execute_cmd(self, cmd, args, source):
		if self.commands.has_key(cmd):
			if self.commands[cmd][0] <= len(args):
				return self.commands[cmd][1](args, source)
		return ''
		
	def proccess(self, cmd, source):
		command = cmd[0]
		args = cmd[1:]
		return self.execute_cmd(command, args, source)

class Macros:
	gmacrolist={}
	gaccesslist={}
	
	macrolist={}
	accesslist={}		
	macrocmds = MacroCommands()
	
	def init(self,gch):
		self.gmacrolist = eval(read_file("settings/macros.txt"))
		self.gaccesslist = eval(read_file("settings/macroaccess.txt"))

		mcrfile='settings/'+gch+'/macros.txt'
		mcracfile='settings/'+gch+'/macroaccess.txt'

		try:
			mcr = eval(read_file(mcrfile))
			if not mcr=='{}':
				self.macrolist[gch]=gch
				self.macrolist[gch]=mcr
			else:
				self.macrolist[gch]=gch
				self.macrolist[gch]={}
		except:
			pass

		try:
			mcrac = eval(read_file(mcracfile))
			if not mcrac=='{}':
				self.accesslist[gch]=gch
				self.accesslist[gch]=mcrac
			else:
				self.accesslist[gch]=gch
				self.accesslist[gch]={}
		except:
			pass

	def load(self,gch):
		mcrfile='settings/'+gch+'/macros.txt'
		mcracfile='settings/'+gch+'/macroaccess.txt'

		try:
			mcr = eval(read_file(mcrfile))
			if not mcr=='{}':
				self.macrolist[gch]=gch
				self.macrolist[gch]=mcr
			else:
				self.macrolist[gch]=gch
				self.macrolist[gch]={}
		except:
			pass

		try:
			mcrac = eval(read_file(mcracfile))
			if not mcrac=='{}':
				self.accesslist[gch]=gch
				self.accesslist[gch]=mcrac
			else:
				self.accesslist[gch]=gch
				self.accesslist[gch]={}
		except:
			pass		
		
	def flush(self):
		for x in self.macrolist.keys():
			write_file('settings/'+x+'/macros.txt', str(self.macrolist[x]))
		for x in self.accesslist.keys():
			write_file('settings/'+x+'/macroaccess.txt', str(self.accesslist[x]))
		
	def add(self, mapee, map, gch=''):
		if gch:
			if not self.macrolist.has_key(gch):
				self.macrolist[gch]=gch
				self.macrolist[gch]={}
			self.macrolist[gch][mapee]=map
		else:
			self.gmacrolist[mapee]=map
		
	def remove(self, mapee, gch=None):
		if gch:
			if self.macrolist[gch].has_key(mapee):
				del self.macrolist[gch][mapee]
		else:
			if self.gmacrolist.has_key(mapee):
				del self.gmacrolist[mapee]			
			
	def map_char(self, x, i):
		ret=i['level']
		if i['esc']:
			i['esc']=False
		elif x == '\\':
			i['esc']=True
			ret=0
		elif x == '`':
			i['larg'] = not i['larg']
			ret=0
		elif x == ' ':
			if not i['larg']:
				i['level']+=1
				ret=0
		return ret

	def get_map(self, inp):
		i={'larg': False, 'level': 1, 'esc': False}
		return [self.map_char(x, i) for x in list(inp)]
	
	def parse_cmd(self, me):
		i=0
		m = self.get_map(me)
		args=[''] * max(m)
		while i<len(m):
			if m[i] != 0:
				args[m[i]-1]+=me[i]
			i+=1
		return args

	def expand(self, cmd, source):
		if type(cmd) is None:
			return ''		
		exp=''
		cl=self.parse_cmd(cmd)
		if (len(cl)<1):
			return cmd
		command=cl[0].split()[0].lower()
		args=cl[1:]
		try:
			for macro in self.macrolist[source[1]]:
				if len(command)<=len(macro) and command == macro[0:len(macro)]:
					if self.macrolist[source[1]][macro]:
						exp = self.apply(self.macrolist[source[1]][macro], args, source)
		except:
			pass
		try:
			for macro in self.gmacrolist:
				if len(command)<=len(macro) and command == macro[0:len(macro)]:
					if self.gmacrolist[macro]:
						exp = self.apply(self.gmacrolist[macro], args, source)
		except:
			pass
		if not exp:
			return cmd
		rexp = self.expand(exp, source)
		return rexp
		
	def comexp(self, cmd, source, key=''):
		if type(cmd) is None:
			return ''
		cl=self.parse_cmd(cmd)
		if (len(cl)<1):
			return cmd
		command=cl[0].split(' ')[0]
		args=cl[1:]
		exp = ''
		try:
			for macro in self.macrolist[source[1]]:
				if len(command)<=len(macro) and command == macro[0:len(macro)]:
					if self.macrolist[source[1]][macro]:
						exp = self.apply(self.macrolist[source[1]][macro], args, source)
		except:
			pass
		try:
			for macro in self.gmacrolist:
				if len(command)<=len(macro) and command == macro[0:len(macro)]:
					if self.gmacrolist[macro]:
						exp = self.apply(self.gmacrolist[macro], args, source)
		except:
			pass
		if not exp:
			return cmd
		rexp = self.comexp(exp, source, key)
		return rexp
		
	def apply(self, macro, args, source):
		expanded = macro
		m=self.macrocmds.parse_cmd(macro)
		expanded = expanded.replace('$*', ' '.join(args));
		for i in m:
			cmd = [x.strip() for x in i.split(',')]
			for j in re.findall('\$[0-9]+', i):
				index = int(j[1:])-1
				if len(args)<=index:
					return expanded
				cmd = [x.replace(j, args[index]) for x in cmd]
			res = self.macrocmds.proccess(cmd, source)
			if res:
				expanded = expanded.replace('%('+i+')', res)
		for j in re.findall('\$[0-9]+', expanded):
			index = int(j[1:])-1
			if len(args)<=index:
				return expanded
			expanded = expanded.replace(j, args[index])
		return expanded
		
	def get_access(self, macro, gch):
		try:
			if self.accesslist[gch].has_key(macro):
				return self.accesslist[gch][macro]
		except:
			pass
		try:
			if self.gaccesslist.has_key(macro):
				return self.gaccesslist[macro]
		except:
			return -1
		
	def give_access(self, macro, access, gch=None):
		if gch:
			if not self.accesslist.has_key(gch):
				self.accesslist[gch]=gch
				self.accesslist[gch]={}			
			self.accesslist[gch][macro] = access
		else:
			if not self.gaccesslist.has_key(macro):
				self.gaccesslist[macro]=macro
			self.gaccesslist[macro]=access
