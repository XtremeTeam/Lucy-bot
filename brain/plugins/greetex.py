#===islucyplugin===
# -*- coding: utf-8 -*-
# Плагин для talisman бота
# Назначение рандомных приветствий на AFFILIATION (owner, admin, member, none)
# Написал: Gigabyte
# 

def greetex_work_2(aff='',greet='',gch=''):
	gr = ''
	q = 0
	mas = ['0']
	DBPATH='settings/'+gch+'/greetex.txt'
	if check_file(gch,'greetex.txt'):
		greetexdb = eval(read_file(DBPATH))
		if aff and greet:
			if aff == 'show':
				try:
					res = string.split(greet, ' ', 1)
					q = int(res[1])
					if (res[0] != 'none') & (res[0] != 'member') & (res[0] != 'admin') & (res[0] != 'owner'):
						msg(gch, u'about title "'+greet+u'" :-O i dont know =(')
						return
					if len(greetexdb[res[0]]) == 0:
						msg(gch, u'welcome '+res[0]+u' not yet created!')
						return
					if q < len(greetexdb[res[0]]):
						gr = greetexdb[res[0]][q]
					else:
						msg(gch, u'welcome '+res[0]+u', with indeks '+res[1]+u' not available!')
						return
					msg(gch, u'<'+str(q)+u'> '+gr)
				except:
					if (greet != 'none') & (greet != 'member') & (greet != 'admin') & (greet != 'owner'):
						msg(gch, u'are there exist the affiliation "'+greet+u'" :-O i dont know about this =(')
						return
					if len(greetexdb[res[0]]) == 0:
						msg(gch, u'welcome '+res[0]+u' not yet created!')
						return
					for i in range(0, len(greetexdb[greet]) ):
						gr +='<'+str(i)+'> '+greetexdb[greet][i] + '\n'
					msg(gch, gr)
			if aff == 'del':
				try:
					res = string.split(greet, ' ', 1)
					q = int(res[1])
					if q < len(greetexdb[res[0]]):
						del greetexdb[res[0]][q]
					else:
						msg(gch, u'welcome '+res[0]+u', with indeks '+res[1]+u' not available!')
						return
					msg(gch, u'deleted')
					write_file(DBPATH, str(greetexdb))
				except:
					msg(gch, u'what should ido?')




def greetex_work(aff='',greet='',gch=''):
	mas = ['0']
	DBPATH='settings/'+gch+'/greetex.txt'
	if check_file(gch,'greetex.txt'):
		greetexdb = eval(read_file(DBPATH))
		if aff and greet:
			if not aff in greetexdb.keys():
				try:
					mas = greetexdb[aff]
				except:
					msg('x-team@muc.xtreme.im', str(len(mas)))
					mas[ len(mas)  - 1] = greet
				mas[ len(mas) - 1 ] = greet
				greetexdb[aff]=mas
				write_file(DBPATH, str(greetexdb))
				return 1
			else:
				try:
					mas = greetexdb[aff]
					mas = mas + [greet]
				except:
#					msg('stalker@conference.jabber.ru', str(len(mas)))
					mas[0] = greet
				greetexdb[aff]=mas
				write_file(DBPATH, str(greetexdb))
				return 1
		elif aff:
			if aff in greetexdb.keys():
				del greetexdb[aff]
				write_file(DBPATH, str(greetexdb))
				return 1
			return 0
		else:
			return 0


def handler_greetex_black(type, source, parameters):
	levels = [u' ', u'Флудераст', u'Почётный флудераст', u'Мудило', u'Жертва', u'Недотёпа', u'Тупишка', u'Глупый человек', u'Нарушитель', u'Злостный нарушитель', u'Мразь']
	a = 0
	raw = string.split(parameters, ' ', 2)
	if (len(raw)<2):
		reply(type, source, u'Should be 2 parameters!')
		return
	DBPATH='settings/'
	if check_file_ex(DBPATH,'blacklist.list'):
		data = eval(read_file(DBPATH+'blacklist.list'))
	if (raw[0].count('@') == 1) & (raw[0].count('.') >=1):
		try:
			a = int(raw[1])
			if (a>=0) & (a<=10):
				data[raw[0].lower()] = raw[1]
				if raw[1] == '0':
					del data[raw[0].lower()]
					reply(type, source, u'JID <'+raw[0].lower()+u'> removed from BLACK LIST U2')
					write_file(DBPATH + 'blacklist.list', str(data))
					return
				reply(type, source, u'JID <'+raw[0].lower()+u'> successfully added to BLACK LIST U2 level '+ raw[1] +' (' +levels[int(raw[1]) ]+')' )
			else:
				reply(type, source, u'JID <'+raw[0].lower()+u'> was not added to BLACK LIST U2 because <'+ raw[1]+u'> is not the correct level (0 - 10)')
				return
		except:
			reply(type, source, u'JID <'+raw[0].lower()+u'>  was not added to BLACK LIST U2 because <'+ raw[1]+u'> is not the correct level (0 - 10)')
			return
	else:
		nicks = GROUPCHATS[source[1]].keys()
		if raw[0] in nicks:
			try:
				a = int(raw[1])
				if (a>=0) & (a<=10):
					data[get_true_jid(source[1]+'/'+raw[0]).lower()] = raw[1]
					if raw[1] == '0':
						del data[get_true_jid(source[1]+'/'+raw[0]).lower()]
						reply(type, source, u'<'+raw[0].lower()+u'> удалён из BLACK LIST U2')
						write_file(DBPATH + 'blacklist.list', str(data))
						return
					reply(type, source, u'<'+raw[0].lower()+u'> successfully added to the BLACK LIST U2 level '+ raw[1]+' (' +levels[int(raw[1]) ]+')')
				else:
					reply(type, source, u'<'+raw[0].lower()+u'> was not added to the BLACK LIST U2 because <'+ raw[1]+u'> is not the correct level (0 - 10)')
					return
			except:
				reply(type, source, u'<'+raw[0].lower()+u'> was not added to BLACK LIST U2 because <'+ raw[1]+u'> is not the correct level (0 - 10)')
				return
		else:
			reply(type, source, u'User with nick <'+raw[0]+u'> not exist here!')
			return

	write_file(DBPATH + 'blacklist.list', str(data))


def check_file_ex(gch='',file=''):
	pth,pthf='',''
	if gch:
		pthf=gch+file
		pth=gch
	else:
		pthf=gch+file
		pth='gch'
	if os.path.exists(pthf):
		return 1
	else:
		try:
			if not os.path.exists(pth):
				os.mkdir(pth,0755)
			if os.access(pthf, os.F_OK):
				fp = file(pthf, 'w')
			else:
				fp = open(pthf, 'w')
			fp.write('{}')
			fp.close()
			return 1
		except:
			return 0

def atjoin_greetex(groupchat, nick, aff, role):
	global mute
	global version
	version = ['[empty]','[empty]','[empty]']
	y = 0
	res_1 = ''
# terdapat stud Тут какой то косяк
	if 1==1:
#		mute = 0
		DBPATH='settings/'
		if check_file_ex(DBPATH, 'blacklist.list'):
			data = eval(read_file(DBPATH+'blacklist.list'))
		if (get_true_jid(groupchat+'/'+nick)).lower() in data.keys():
			if data[(get_true_jid(groupchat+'/'+nick)).lower()] == '3':
				reply('public', [groupchat+'/'+nick, groupchat, nick], u'Ты снова выходишь на связь, мудило?')
				return
			if data[(get_true_jid(groupchat+'/'+nick)).lower()] == '2':
				msg(groupchat, u'/me видит почётного флудераста - ' + nick)
				return
			if data[(get_true_jid(groupchat+'/'+nick)).lower()] == '1':
				reply('public', [groupchat+'/'+nick, groupchat, nick], u'Again, we will flood or?')
				return


		DBPATH='settings/'+groupchat+'/greetex.txt'
		if check_file(groupchat,'greetex.txt'):
			GREETEX = eval(read_file(DBPATH))
			if aff in GREETEX.keys():
				mas = GREETEX[aff]
				res = random.choice(mas)

				res_ = string.split(res, ' ', res.count(' '))



				while y != len(res_):
#					if '%NICK%' == res_[y]:
					if res_[y].count('%NICK%')>0:
						if res_[y].count(',')>0:
							res_[y] = nick+','
						if res_[y].count('.')>0:
							res_[y] = nick+'.'
						if res_[y].count('!')>0:
							res_[y] = nick+'!'
						if res_[y].count('?')>0:
							res_[y] = nick+'?'
						if (res_[y].count(',')==0) & (res_[y].count('.')==0) & (res_[y].count('!')==0) & (res_[y].count('?')==0):
							res_[y] = nick
					version[0] = '[empty]'
					version[1] = '[empty]'
					version[2] = '[empty]'
					if ( res.count('%VER_NAME%')>0 ) | ( res.count('%VER_VER%')>0 ) | ( res.count('%VER_OS%')>0 ):
						handler_version_ex('public', [groupchat+'/'+nick, groupchat, nick], '')
						time.sleep(6.0)

					if res_[y].count('%VER_NAME%')>0:
						if res_[y].count(',')>0:
							res_[y] = version[0]+','
						if res_[y].count('.')>0:
							res_[y] = version[0]+'.'
						if res_[y].count('!')>0:
							res_[y] = version[0]+'!'
						if res_[y].count('?')>0:
							res_[y] = version[0]+'?'
						if (res_[y].count(',')==0) & (res_[y].count('.')==0) & (res_[y].count('!')==0) & (res_[y].count('?')==0):
							res_[y] = version[0]


					if res_[y].count('%VER_VER%')>0:
						if res_[y].count(',')>0:
							res_[y] = version[1]+','
						if res_[y].count('.')>0:
							res_[y] = version[1]+'.'
						if res_[y].count('!')>0:
							res_[y] = version[1]+'!'
						if res_[y].count('?')>0:
							res_[y] = version[1]+'?'
						if (res_[y].count(',')==0) & (res_[y].count('.')==0) & (res_[y].count('!')==0) & (res_[y].count('?')==0):
							res_[y] = version[1]


					if res_[y].count('%VER_OS%')>0:
						if res_[y].count(',')>0:
							res_[y] = version[2]+','
						if res_[y].count('.')>0:
							res_[y] = version[2]+'.'
						if res_[y].count('!')>0:
							res_[y] = version[2]+'!'
						if res_[y].count('?')>0:
							res_[y] = version[2]+'?'
						if (res_[y].count(',')==0) & (res_[y].count('.')==0) & (res_[y].count('!')==0) & (res_[y].count('?')==0):
							res_[y] = version[2]

					res_1 = res_1 + res_[y]
					res_1 = res_1 + ' '
					y = y + 1
					
				msg(groupchat, res_1)

#			if groupchat in GREETEX.keys():
#	 			if aff in GREETEX[groupchat]:




def handler_greetex(type,source,parameters):
	if not parameters:
		reply(type, source, u'hmmm? Example: <greetex member=hello %NICK% welcome>')
		return

	if parameters.count('=')==0:
#		msg('stalker@conference.jabber.ru', u'Отладка: '+affi+u' '+str(answ)+u' '+source[1])
		answ=greetex_work(parameters, gch=source[1])
		if answ:
			reply(type, source, u'killed')
			return
		else:
			reply(type, source, u'who is it?')
			return

	parameters=parameters.strip()
	rawgreet = string.split(parameters, '=', 1)
	if not len(rawgreet)==2:
		reply(type, source, u'what is that?')
		return
	greet=rawgreet[1].strip()
	affi=rawgreet[0].strip()
	if (affi != 'none') & (affi != 'member') & (affi != 'admin') & (affi != 'owner') & (affi != 'show') & (affi != 'del'):
		msg(source[1], u'are there exist the affiliation "'+affi+u'" :-O i dont know about this =(')
		return
	if (affi == 'show') | (affi == 'del'):
		greetex_work_2(affi, greet, source[1])
		return

	answ=greetex_work(affi, greet, source[1])
	if answ:
		reply(type, source, u'added '+affi)
	else:
		reply(type, source, u'i dont know! :-|')

	if not greet:
		answ=greetex_work(affi, gch=source[1])
		if answ:
			reply(type, source, u'killed')
			return
		else:
			reply(type, source, u'who is it?')
			return


register_join_handler(atjoin_greetex)
register_command_handler(handler_greetex, COMM_PREFIX+'greetex', ['admin','muc','all','new'], 20, 'Add greeting  according to affiliations (none, member, admin, owner).\nTo delete greeting, "gretex="', 'greetex <affiliation=greeting>', ['greetex owner=hello %NICK% welcome','greetex none=hello %NICK% welcome'])
register_command_handler(handler_greetex_black, COMM_PREFIX+'black_list', ['superadmin','all','new'], 100, 'Add a specify user onto black list globally!!!', 'black_list [nick] [level 1 - 10]', ['black_list joyo 3'])

