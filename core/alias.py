# -*- coding: utf-8 -*-

#  fatal module
#  alias.py

#  Initial Copyright © 2007 dimichxp <dimichxp@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>
#  Modifications Copyright © 2009 wd/lotusfeet <dao/yoga>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

from __future__ import with_statement
import random,string,re,os

try:
	from fatalapi25 import *
except ImportError:
	try:
		from fatalapi26 import *
	except ImportError:
		print "Can't find proper fatalapi module. Exit!"
		os.abort()

dbmtx = threading.Lock()

def alias_exists(alias,gch=''):
	alias = alias.replace('"','&quot;')
	
	sql = 'SELECT * FROM aliasdb WHERE alias="%s";' % (alias)
	
	if gch:
		qres = sqlquery('dynamic/'+gch+'/alias.db',sql)
	else:
		qres = sqlquery('dynamic/alias.db',sql)
	
	if qres:
		return True
	else:
		return False

def set_alias(alias,body,gch=''):
	alias = alias.replace('"','&quot;')
	body = body.replace('"','&quot;')
	
	if not alias_exists(alias,gch):
		sql = 'INSERT INTO aliasdb (alias,body,access) VALUES ("%s","%s","");' % (alias.strip(),body.strip())
	else:
		sql = 'UPDATE aliasdb SET "body"="%s" WHERE alias="%s";' % (body.strip(),alias.strip())
	
	if gch:
		with semph(dbmtx):
			qres = sqlquery('dynamic/'+gch+'/alias.db',sql)
	else:
		with semph(dbmtx):
			qres = sqlquery('dynamic/alias.db',sql)
	
	return qres
	
def set_access(alias,access,gch=''):
	alias = alias.replace('"','&quot;')
	access = str(access)
	
	if alias_exists(alias,gch):
		sql = 'UPDATE aliasdb SET "access"="%s" WHERE alias="%s";' % (access.strip(),alias.strip())
	else:
		return
	
	if gch:
		with semph(dbmtx):
			qres = sqlquery('dynamic/'+gch+'/alias.db',sql)
	else:
		with semph(dbmtx):
			qres = sqlquery('dynamic/alias.db',sql)
	
	return qres
	
def remove_alias(alias,gch=''):
	sql = 'DELETE FROM aliasdb WHERE alias="%s";' % (alias)
	
	if gch:
		with semph(dbmtx):
			rep = sqlquery('dynamic/'+gch+'/alias.db',sql)
	else:
		with semph(dbmtx):
			rep = sqlquery('dynamic/alias.db',sql)
		
	return rep

def get_alias_list(gch='',oer={}):
	alias_list = {}
	
	sql = 'SELECT alias,body FROM aliasdb;'
	
	if gch:
		qres = sqlquery('settings/'+gch+'/alias.db',sql)
	else:
		qres = sqlquery('settings/alias.db',sql)
	
	if qres == '':
		return oer
	else:
		if qres:
			for al in qres:
				alias = al[0].replace('&quot;','"')
				abody = al[1].replace('&quot;','"')
				alias_list[alias] = abody 
			return alias_list
		else:
			return oer

def get_access_list(gch='',oer={}):
	access_list = {}
	
	sql = 'SELECT alias,access FROM aliasdb;'
	
	if gch:
		qres = sqlquery('dynamic/'+gch+'/alias.db',sql)
	else:
		qres = sqlquery('dynamic/alias.db',sql)
	
	if qres == '':
		return oer
	else:
		if qres:
			for acc in qres:
				acc = list(acc)
				if acc[1].isdigit():
					acc[1] = int(acc[1])
				else:
					acc[1] = -1
				access_list[acc[0]] = acc[1]
			return access_list
		else:
			return oer

def shell_esc(s):
	for c in [';', '&', '|', '`', '$']:
		s = s.replace(c, '#')
	return s

def xml_esc(s):
	s = s.replace('\'', '&apos;')
	s = s.replace('>', '&gt;')
	s = s.replace('<', '&lt;')
	s = s.replace('&', '&amp;')
	s = s.replace('\"', '&quot;')
	return s
	
def alias_get_rand(args, source):
	try:
		f=int(args[0])
		t=int(args[1])
		return str(random.randrange(f, t))
	except:
		return ''

def alias_replace(args, source):
	try:
		rstr = args[0]
		sfro = args[1]
		srto = args[2]
		return rstr.replace(sfro,srto)
	except:
		return ''

def alias_shell_escape(args, source):
	return shell_esc(args[0])

def alias_xml_escape(args, source):
	return xml_esc(args[0])

def alias_context(args, source):
	arg = args[0]
	if arg == 'conf':
		return xml_esc(source[1])
	elif arg == 'nick':
		return xml_esc(source[2])
	elif arg == 'conf_jid':
		return xml_esc(source[0])
	else:
		return ''
		
class AliasCommands:
	commands={
	          'replace':      [3, alias_replace     ],
		  'rand':         [2, alias_get_rand    ],
                  'shell_escape': [1, alias_shell_escape],
                  'xml_escape':   [1, alias_xml_escape  ],
		  'context':      [1, alias_context     ]
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

class Alias:
	galiaslist={}
	gaccesslist={}
	
	aliaslist={}
	accesslist={}
	aliascmds = AliasCommands()
		
	def init(self,gch):
		self.galiaslist = get_alias_list()
		self.gaccesslist = get_access_list()

		ali = get_alias_list(gch=gch)
		if not ali=='{}':
			self.aliaslist[gch]=ali
		else:
			self.aliaslist[gch]={}

		aliac = get_access_list(gch=gch)
		if not aliac=='{}':
			self.accesslist[gch]=aliac
		else:
			self.accesslist[gch]={}

	def load(self,gch):
		ali = get_alias_list(gch=gch)
		if not ali=='{}':
			self.aliaslist[gch]=ali
		else:
			self.aliaslist[gch]={}

		aliac = get_access_list(gch=gch)
		if not aliac=='{}':
			self.accesslist[gch]=aliac
		else:
			self.accesslist[gch]={}
				
	def add(self, alias, body, gch=''):
		if gch:
			res = set_alias(alias,body,gch)
			
			if res == '':
				return False
			
			if not self.aliaslist.has_key(gch):
				self.aliaslist[gch]={}
			self.aliaslist[gch][alias]=body
			
			return True
		else:
			res = set_alias(alias,body)
			
			if res == '':
				return False
						
			self.galiaslist[alias]=body
			
			return True
		
	def remove(self, alias, gch=''):
		if gch:
			res = remove_alias(alias,gch)
			
			if res == '':
				return False
			
			if self.aliaslist[gch].has_key(alias):
				del self.aliaslist[gch][alias]
			
			return alias_exists(alias,gch)
		else:
			res = remove_alias(alias)
			
			if res == '':
				return False
			
			if self.galiaslist.has_key(alias):
				del self.galiaslist[alias]
				
			return alias_exists(alias)

	def map_char(self, x, i):
		ret=i['level']
		if i['esc']:
			i['esc']=False
		elif x == '\\':
			i['esc']=True
			ret=0
		elif x == '=':
			i['larg'] = not i['larg']
			i['level']+=1
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
		if args:
			args = [arli.strip() for arli in args if arli]
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
			for alias in self.aliaslist[source[1]]:
				if len(command)<=len(alias) and command == alias[0:len(alias)]:
					if self.aliaslist[source[1]][alias]:
						exp = self.apply(self.aliaslist[source[1]][alias], args, source)
		except:
			pass
		try:
			for alias in self.galiaslist:
				if len(command)<=len(alias) and command == alias[0:len(alias)]:
					if self.galiaslist[alias]:
						exp = self.apply(self.galiaslist[alias], args, source)
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
			for alias in self.aliaslist[source[1]]:
				if len(command)<=len(alias) and command == alias[0:len(alias)]:
					if self.aliaslist[source[1]][alias]:
						exp = self.apply(self.aliaslist[source[1]][alias], args, source)
		except:
			pass
		try:
			for alias in self.galiaslist:
				if len(command)<=len(alias) and command == alias[0:len(alias)]:
					if self.galiaslist[alias]:
						exp = self.apply(self.galiaslist[alias], args, source)
		except:
			pass
		if not exp:
			return cmd
		rexp = self.comexp(exp, source, key)
		return rexp
		
	def apply(self, alias, args, source):
		expanded = alias
		expanded = expanded.replace('$*', ' '.join(args));
		m=self.aliascmds.parse_cmd(expanded)
		for i in m:
			cmd = [x.strip() for x in i.split(',')]
			for j in re.findall('\$[0-9]+', i):
				index = int(j[1:])-1
				if len(args)<=index:
					return expanded
				cmd = [x.replace(j, args[index]) for x in cmd]
			res = self.aliascmds.proccess(cmd, source)
			if res:
				expanded = expanded.replace('%('+i+')', res)
		for j in re.findall('\$[0-9]+', expanded):
			index = int(j[1:])-1
			if len(args)<=index:
				return expanded
			expanded = expanded.replace(j, args[index])
		return expanded
		
	def get_access(self, alias, gch):
		try:
			if self.accesslist[gch].has_key(alias):
				return self.accesslist[gch][alias]
		except:
			return -1
		try:
			if self.gaccesslist.has_key(alias):
				return self.gaccesslist[alias]
		except:
			return -1
		
	def give_access(self, alias, access, gch=''):
		if gch:
			res = set_access(alias,access,gch)
			
			if res == '':
				return False
			
			if not self.accesslist.has_key(gch):
				self.accesslist[gch]={}	
			self.accesslist[gch][alias] = access
			
			return True
		else:
			res = set_access(alias,access)
			
			if res == '':
				return False

			if not self.gaccesslist.has_key(alias):
				self.gaccesslist[alias]=alias
			self.gaccesslist[alias]=access
			
			return True
			
	def remove_access(self, alias, gch=None):
		if gch:
			if self.accesslist[gch].has_key(alias):
				del self.accesslist[gch][alias]
		else:
			if self.gaccesslist.has_key(alias):
				del self.gaccesslist[alias]