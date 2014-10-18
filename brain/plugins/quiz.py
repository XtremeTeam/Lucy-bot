#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  quiz = 33693 lines


##############################################################
## Настройка плагина #########################################
QUIZ_FILE = 'settings/questions.txt' # путь к БД ###############
QUIZ_TOTAL_LINES = 29 # количество вопросов в БД ##########
QUIZ_TIME_LIMIT = 200 # таймаут в секундах ###################
QUIZ_IDLE_LIMIT = 3 # количество таймаутов до OFF ############
##############################################################
QUIZ_RECURSIVE_MAX = 20 # empty ##############################
QUIZ_CURRENT_ANSWER = {} #####################################
QUIZ_CURRENT_HINT = {} #######################################
QUIZ_CURRENT_HINT_NEW = {} ###################################
QUIZ_CURRENT_TIME = {} #######################################
QUIZ_IDLENESS = {} ###########################################
QUIZ_IDLE_ANSWER = {}
QUIZ_START = {}
QUIZ_IDLE_ANSWER_FIRSR = {}
QUIZ_NOWORD = '*' # символ заменяет "не открытые буквы" ######
##############################################################
MODE = 'M1' # ХИНТЫ. M1 - новый вих хинтов, M2 - старый вид ##
PTS = 'P2'  # Начисление очков: ##############################
ACC = 'A2'  # Уровень доступа к !сл: A1 - все, A2 - ток стар##
############# товавший викторину или модератор              ##
## P1 - таймаут / время_ответа / 3+1 / кол-во открытых букв ##
## P2 - (таймаут / время_ответа) / (прцнт_откр._слова / 10) ##
## * Первая формула рубит балы в пределах 0 - 5 в основном ###
## * Вторая формула даёт более широкую оценку ответу, размах #
##   баллов при этом от 0 до 50 (может кому то показаться не #
##   не честным, но мне это более нравится чем 1) ############
##############################################################
###%%%%%%###%%%%%%#####%%%%%%#################################
##%%####%%####%%######%%####%%################################
##%%##########%%######%%######################################
##%%##%%%%####%%######%%##%%%%################################
##%%##%%%%####%%######%%##%%%%################################
##%%####%%####%%######%%####%%################################
###%%%%%%###%%%%%%#####%%%%%%#################################
##############################################################

import threading

HELP = u'help of command > "!quiz"'


def sectomin(time):
        m = 0
        s = 0
        if time >= 60:
                m = time / 60
                
                if (m * 60) != 0:
                        s = time - (m * 60)
                else:
                        s = 0
        else:
                m = 0
                s = time
                

        return str(m)+u'min. in '+str(s)+u'sec.'


def quiz_timer(groupchat, start_time):
        global QUIZ_TIME_LIMIT
        global QUIZ_CURRENT_TIME
        
	time.sleep(QUIZ_TIME_LIMIT)
	if QUIZ_CURRENT_TIME.has_key(groupchat) and QUIZ_CURRENT_ANSWER.has_key(groupchat) and start_time == QUIZ_CURRENT_TIME[groupchat]:
		QUIZ_CURRENT_ANSWER[groupchat]
		msg(groupchat, u'(!) time out! ' + sectomin(QUIZ_TIME_LIMIT) + u' passed.\nCorrect answer: ' + QUIZ_CURRENT_ANSWER[groupchat])
		if QUIZ_IDLENESS.has_key(groupchat):
			QUIZ_IDLENESS[groupchat] += 1
		else:
			QUIZ_IDLENESS[groupchat] = 1
		if QUIZ_IDLENESS[groupchat] >= QUIZ_IDLE_LIMIT:
			msg(groupchat, u'(!) quiz will be automatically completed for inaction! ' + str(QUIZ_IDLE_LIMIT) + ' unanswered questions.')
			del QUIZ_CURRENT_ANSWER[groupchat]
			quiz_list_scores(groupchat)
		else:
			quiz_ask_question(groupchat)

def quiz_new_question():
        global QUIZ_RECURSIVE_MAX
        
	line_num = random.randrange(29)
	fp = file(QUIZ_FILE)
	for n in range(line_num + 1):
		if n == line_num:
			(question, answer) = string.split(fp.readline().strip(), '|', 1)
			return (unicode(question, 'utf-8'), unicode(answer, 'utf-8'))
		else:
			fp.readline()

def quiz_ask_question(groupchat):
        global answer
        global QUIZ_CURRENT_TIME
        global question
        global QUIZ_IDLE_ANSWER
        global QUIZ_IDLE_ANSWER_FIRSR
        QUIZ_IDLE_ANSWER = {groupchat:{}}
	(question, answer) = quiz_new_question()
	QUIZ_CURRENT_ANSWER[groupchat] = answer
	QUIZ_CURRENT_HINT[groupchat] = None
	QUIZ_CURRENT_HINT_NEW[groupchat] = None
	QUIZ_CURRENT_TIME[groupchat] = time.time()
	threading.Thread(None, quiz_timer, 'gch'+str(random.randrange(0,9999)), (groupchat, QUIZ_CURRENT_TIME[groupchat])).start()
	msg(groupchat, u'(?) question: \n' + question)

def quiz_ask_new_question(groupchat, ans):
        global QUIZ_CURRENT_TIME
        global answer
        global question
        global QUIZ_IDLE_ANSWER
        global QUIZ_IDLE_ANSWER_FIRSR
        QUIZ_IDLE_ANSWER = {groupchat:{}}
	(question, answer) = quiz_new_question()
	QUIZ_CURRENT_ANSWER[groupchat] = answer
	QUIZ_CURRENT_HINT[groupchat] = None
	QUIZ_CURRENT_HINT_NEW[groupchat] = None
	QUIZ_CURRENT_TIME[groupchat] = time.time()
	threading.Thread(None, quiz_timer, 'gch'+str(random.randrange(0,9999)), (groupchat, QUIZ_CURRENT_TIME[groupchat])).start()
	msg(groupchat, u'(!) correct answer: '+ans+u', change of question: \n' + question)
	
def quiz_answer_question(groupchat, nick, answer):
        global QUIZ_IDLE_ANSWER
        global QUIZ_IDLE_ANSWER_FIRSR
        
	DBPATH='settings/'+groupchat+'/quiz.cfg'
	if check_file(groupchat,'quiz.cfg'):
		QUIZ_SCORES = eval(read_file(DBPATH))
	jid = get_true_jid(groupchat+'/'+nick)
	jid = jid.lower()
	
	if QUIZ_CURRENT_ANSWER.has_key(groupchat):
                answer1 = QUIZ_CURRENT_ANSWER[groupchat].lower()
                answer2 = answer.lower()
                if answer1 == answer2:
                        if QUIZ_IDLE_ANSWER.has_key(groupchat):
                                if len(QUIZ_IDLE_ANSWER[groupchat]) != 0:
                                        if QUIZ_IDLE_ANSWER[groupchat].has_key(jid):
                                                if QUIZ_IDLE_ANSWER[groupchat][jid][1] == '1':
                                                        msg(groupchat, nick+u': you have answered correctly!')
                                                else:
                                                        razn = QUIZ_IDLE_ANSWER[groupchat][jid][0] - QUIZ_IDLE_ANSWER_FIRSR[groupchat]
                                                        msg(groupchat, nick+u': you have answered correctly, опоздав на %.3f sec' % razn)
                                        else:
                                                QUIZ_IDLE_ANSWER[groupchat][jid] = [time.time(), '0']
                                                
                                                razn = QUIZ_IDLE_ANSWER[groupchat][jid][0] - QUIZ_IDLE_ANSWER_FIRSR[groupchat]
                                                msg(groupchat, nick+u': you answered correctly, но опоздал на %.3f sec' % razn)
                                        return

			if QUIZ_IDLENESS.has_key(groupchat):
				del QUIZ_IDLENESS[groupchat]
			answer_time = int(time.time() - QUIZ_CURRENT_TIME[groupchat])
			try:
                                if MODE == 'M1':
                                        alen = len(QUIZ_CURRENT_HINT_NEW[groupchat])
                                        blen = QUIZ_CURRENT_HINT_NEW[groupchat].count('')
                                        a = alen - blen
                                if MODE == 'M2':
                                        a = 0
                                        a = a + QUIZ_CURRENT_HINT[groupchat]
                        except:
                                a = 1
                        if PTS == 'P1':
                                points = QUIZ_TIME_LIMIT / answer_time / 3 + 1 / a
                        if PTS == 'P2':
                                try:
                                        alen = len(QUIZ_CURRENT_HINT_NEW[groupchat])
                                        blen = QUIZ_CURRENT_HINT_NEW[groupchat].count('')
                                        a = alen - blen
                                        procent = a * 100 / alen
                                except:
                                        procent = 10
                                
                                points = (QUIZ_TIME_LIMIT / answer_time) / (procent / 10)

			if points == 0:
                                pts = '0'
                        else:
                                pts = '+'+str(points)
			msg(groupchat, u'(!) ' + nick + u', congratulations! You get ' + pts + u' points in the bank!\nCorrect answer is: ' + answer)			
			if not QUIZ_SCORES.has_key(groupchat):
				QUIZ_SCORES[groupchat] = {}
			if QUIZ_SCORES[groupchat].has_key(jid):
				QUIZ_SCORES[groupchat][jid][0] += points
				QUIZ_SCORES[groupchat][jid][1] += points
				QUIZ_SCORES[groupchat][jid][2] = nick
				QUIZ_SCORES[groupchat][jid][3] += 1
			else:
				QUIZ_SCORES[groupchat][jid] = [points, points, nick, 1]
			
#			quiz_list_scores(groupchat)


                        QUIZ_IDLE_ANSWER[groupchat][jid] = [time.time(), '1']
                        QUIZ_IDLE_ANSWER_FIRSR[groupchat] = time.time()

                        if QUIZ_IDLE_ANSWER.has_key(groupchat):
                                if len(QUIZ_IDLE_ANSWER[groupchat]) == 1:
                                        time.sleep(1.0)
                                        quiz_ask_question(groupchat)
	write_file(DBPATH, str(QUIZ_SCORES))

def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]
 
def sort(groupchat, mas, sort=1, count=10):
        base = mas[groupchat]
        arr = []
        str1 = ''
        for a in base:
                asd = base[a][sort]
                arr += [asd]
        i = len(arr)
        while i > 1:
                for j in xrange(i - 1):
                        if arr[j] < arr[j + 1]:
                                swap(arr, j, j + 1)
                i -= 1
        top10 = 1
        prim = ''
        charcount = 0

        for z in arr:                       
                for x in base:
                        nick = base[x][2]
                        if len(nick) > charcount:
                                charcount = len(nick)
                        
        for z in arr:                       
                for x in base:
                        nick = base[x][2]
                        if len(nick) < charcount:
                                nick += ' ' * (charcount - len(nick))
                        nick += ' '
                                
                        if base[x][sort] == z:
                                str1 += str(top10)+'. '+nick+' '+str(base[x][0])+'-'+str(base[x][1])+'-'+str(base[x][3])+'\n'
                                if top10 < count:
                                        top10 += 1
                                else:
                                        str1 = prim + str1
                                        return str1
        str1 = prim + str1
        return str1



def quiz_list_scores(groupchat, sort_=1, count=10):
	DBPATH='settings/'+groupchat+'/quiz.cfg'
	if check_file(groupchat,'quiz.cfg'):
		QUIZ_SCORES = eval(read_file(DBPATH))

        if QUIZ_SCORES.has_key(groupchat):
                if QUIZ_SCORES[groupchat]:
                        if QUIZ_IDLENESS.has_key(groupchat):
                                del QUIZ_IDLENESS[groupchat]
                        if QUIZ_CURRENT_ANSWER.has_key(groupchat):
                                result = u'(*) list of scores:\n[Nick][Current][Total][Answer]\n'
                        else:
                                result = u'(*) list of scores:\n[Nick][Last][Total][Answer]\n'
                        result = result+sort(groupchat, QUIZ_SCORES, sort_, count)

			msg(groupchat, result)

def handler_quiz_start(type, source, parameters):
	groupchat = source[1]
	DBPATH='settings/'+groupchat+'/quiz.cfg'
	if check_file(groupchat,'quiz.cfg'):
		QUIZ_SCORES = eval(read_file(DBPATH))
        jid = get_true_jid(source[1]+'/'+source[2])
        jid = jid.lower()
	if not groupchat:
		reply(type, source, u'not in private')
		return
	if QUIZ_CURRENT_ANSWER.has_key(groupchat):
		reply(type, source, u'quiz exists! '+HELP)
		return
	
	if not QUIZ_SCORES.has_key(groupchat):
                QUIZ_SCORES[groupchat] = {}
                write_file(DBPATH, str(QUIZ_SCORES))
        if QUIZ_SCORES.has_key(groupchat):
                if QUIZ_SCORES[groupchat].has_key(jid):
                        for kjid in QUIZ_SCORES[groupchat]:
                                QUIZ_SCORES[groupchat][kjid][0] = 0
                        
                        write_file(DBPATH, str(QUIZ_SCORES))
        QUIZ_START[groupchat] = jid
        
	if QUIZ_IDLENESS.has_key(groupchat):
		del QUIZ_IDLENESS[groupchat]
#	msg(groupchat, u'[Викторина] Викторина начата! Очки обнулены.')
	quiz_ask_question(groupchat)

def handler_quiz_stop(type, source, parameters):
	groupchat = source[1]
	if QUIZ_CURRENT_ANSWER.has_key(groupchat):
		del QUIZ_CURRENT_ANSWER[groupchat]
		msg(groupchat, u'(!) quiz stopped.')
		time.sleep(1.0)
		quiz_list_scores(groupchat, 0, 10)
	else:
		reply(type, source, u'no quiz, '+HELP)

def handler_quiz_next(type, source, parameters):
        if QUIZ_CURRENT_ANSWER.has_key(source[1]):
                jid = get_true_jid(source[1]+'/'+source[2])
                if ACC == 'A1':
                        quiz_ask_new_question(source[1], QUIZ_CURRENT_ANSWER[source[1]])
                if ACC == 'A2':
                        if (jid == QUIZ_START[source[1]]) | (user_level(source[1]+'/'+source[2], source[1]) >= 16):
                                quiz_ask_new_question(source[1], QUIZ_CURRENT_ANSWER[source[1]])
                        else:
                                reply(type, source, u'this command is allowed only for members, '+HELP)
        else:
                reply(type, source, u'no quiz, '+HELP)

def handler_quiz_hint(type, source, parameters):
        global ans
	groupchat = source[1]
        ans = QUIZ_CURRENT_ANSWER[groupchat]
	if QUIZ_CURRENT_ANSWER.has_key(groupchat):
		if QUIZ_IDLENESS.has_key(groupchat):
			del QUIZ_IDLENESS[groupchat]
		if QUIZ_CURRENT_HINT[groupchat] == None:
			QUIZ_CURRENT_HINT[groupchat] = 0
		if MODE == 'M1':
                        if QUIZ_CURRENT_HINT_NEW[groupchat] == None:
                                ms = ['']
                                QUIZ_CURRENT_HINT_NEW[groupchat] = []
                                for r in range(0, len(QUIZ_CURRENT_ANSWER[groupchat])):
                                        QUIZ_CURRENT_HINT_NEW[groupchat] += ms

                        ex = 1
                        while ex == 1:
                                a = random.choice(QUIZ_CURRENT_ANSWER[groupchat])
                                if not a in QUIZ_CURRENT_HINT_NEW[groupchat]:
                                        for t in range(0, len(QUIZ_CURRENT_ANSWER[groupchat])):
                                                if QUIZ_CURRENT_ANSWER[groupchat][t] == a:
                                                        QUIZ_CURRENT_HINT_NEW[groupchat][t] = a
                                                        ex = 0
                                hint = '' 
                        for hnt in QUIZ_CURRENT_HINT_NEW[groupchat]:
                                if hnt == '':
                                        hint += QUIZ_NOWORD
                                else:
                                        hint += hnt
                        if not '' in QUIZ_CURRENT_HINT_NEW[groupchat]:
                                quiz_ask_new_question(source[1], ans)
                        else:
                                msg(groupchat, u'(*) hint: ' + hint)
                if MODE == 'M2':
                        QUIZ_CURRENT_HINT[groupchat] += 1
                        hint = QUIZ_CURRENT_ANSWER[groupchat][0:QUIZ_CURRENT_HINT[groupchat]]
                        hint += ' *' * (len(QUIZ_CURRENT_ANSWER[groupchat]) - QUIZ_CURRENT_HINT[groupchat])
                        msg(groupchat, u'(*) hint: ' + hint)
                        if (len(QUIZ_CURRENT_ANSWER[groupchat]) - QUIZ_CURRENT_HINT[groupchat]) == 0:
                                quiz_ask_new_question(source[1], ans)
	else:
		reply(type, source, u'no quiz, '+HELP)

def handler_quiz_answer(type, source, parameters):
        global answer
        reply(type, source, answer)



def handler_quiz_scores(type, source, parameters):
	groupchat = source[1]
	
	DBPATH='settings/'+groupchat+'/quiz.cfg'
	if check_file(groupchat,'quiz.cfg'):
		QUIZ_SCORES = eval(read_file(DBPATH))

	if QUIZ_SCORES.has_key(groupchat):
                if QUIZ_SCORES[groupchat]:
                        if QUIZ_CURRENT_ANSWER.has_key(source[1]):
                                quiz_list_scores(groupchat, 0, 10)
                        else:
                                quiz_list_scores(groupchat, 1, 10)
                else:
                        reply(type, source, u'the database is empty, '+HELP)
        else:
                reply(type, source, u'the database is empty, '+HELP)

def handler_quiz_message(type, source, body):
	groupchat = source[1]
	if groupchat and QUIZ_CURRENT_ANSWER.has_key(groupchat):
		quiz_answer_question(source[1], source[2], body.strip())

def handler_quiz_resend(type, source, body):
        global question
        groupchat = source[1]
        if QUIZ_CURRENT_ANSWER.has_key(groupchat):
                res = u'(*) current question: \n'+question
                reply(type, source, res)
        else:
                reply(type, source, u'no quiz, '+HELP)

def handler_quiz_help(type, source, body):
        if QUIZ_CURRENT_ANSWER.has_key(source[1]):
                stat = u'running'
        else:
                stat = u'not running'
        res = u'Quiz v3.0\nQuiz now: '+stat+u'\nDatabase: '+str(QUIZ_TOTAL_LINES)+u' Questions\nCommand:\n- !start - start quiz\n- !stop - start quiz\n- !repeat - repeat question\n- !hint - find an answer tip (removes points)\n- !next - next question\n- !score - conclusion of the current score\n- !base_del - remove all the statistics for the conf (without parameter), or with user (jid parameter)\n+ sort statistics (during the game on the current account, at the end of the game on the current score)\n+ formatting statistics\n+ clearing statistics'
        if MODE == 'M1':
                m = u'* new type of hint (randomly)'
        if MODE == 'M2':
                m = u'* old type of hint'
        if PTS == 'P1':
                p = u'* old type of calculation points'
        if PTS == 'P2':
                p = u'* new type of calculation points'
        if ACC == 'A1':
                a = u'* access !next for all'
        if ACC == 'A2':
                a = u'* access !next only for user created the quiz and moderators'
        res+= u'\nConfiguration:\n'+m+'\n'+p+'\n'+a
        reply(type, source, res)


def handler_quiz_base_del(type, source, body):
	groupchat = source[1]
	
	DBPATH='settings/'+groupchat+'/quiz.cfg'
	if check_file(groupchat,'quiz.cfg'):
		QUIZ_SCORES = eval(read_file(DBPATH))

	if body == '':
                if QUIZ_SCORES.has_key(source[1]):
                        del QUIZ_SCORES[source[1]]
                        reply(type, source, u'<!> database has been completely cleared!')
                else:
                        reply(type, source, u'<!> database empty!')
        else:
                if QUIZ_SCORES.has_key(source[1]):
                        if QUIZ_SCORES[source[1]].has_key(body):
                                del QUIZ_SCORES[source[1]][body]
                                reply(type, source, u'<!> database jid has been removed')
                        else:
                                reply(type, source, u'<!> database empty!')


                else:
                        reply(type, source, u'<!> database has been completely cleared!')
        write_file(DBPATH, str(QUIZ_SCORES))
        
        

register_command_handler(handler_quiz_start, 'qstart', ['new','quiz','all'], 20, 'Start quiz.', '!start', ['!start'])
register_command_handler(handler_quiz_help, 'quiz', ['new','quiz','all'], 0, 'Conclusion HELP.', '!quiz', ['!quiz'])
register_command_handler(handler_quiz_resend, 'repeat', ['new','quiz','all'], 0, 'Repeat current question.', '!repeat', ['!repeat'])
register_command_handler(handler_quiz_stop, 'stop', ['new','quiz','all'], 20, 'Stop quiz.', '!stop', ['!stop'])
register_command_handler(handler_quiz_hint, 'hint', ['new','quiz','all'], 0, 'Find an answer tip (ХЭ).', '!hint', ['!hint'])
register_command_handler(handler_quiz_scores, 'score', ['new','quiz','all'], 0, 'Display conclusion of the current score (nickname, total points).', '!score', ['!score'])
register_command_handler(handler_quiz_next, 'next', ['new','quiz','all'], 0, 'Next question.', '!next', ['!next'])
register_command_handler(handler_quiz_answer, 'answer', ['new','quiz','all'], 100, 'Display correct answer <CHEAT>.', '!answer', ['!answer'])
register_command_handler(handler_quiz_base_del, 'base_del', ['new','quiz','all'], 100, 'Delete all the database.', '!base_del [JID]', ['!base_del guy@jsmart.web.id', '!base_del'])

register_message_handler(handler_quiz_message)
