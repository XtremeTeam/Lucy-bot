#===islucyplugin===
# -*- coding: utf-8 -*-

# [TALKERS FOR TALISMAN BOT BY GIGABYTE]
# Плагин подсчитывает болтунов

# Name: Talkers
# Version: 2.100 beta
# By: Gigabyte
# Official room: stalker@conference.jabbers.ru
# mail: gigabyte@ngs.ru
# www: http://jabbrik.ru


# Плагин является ксклюзивным для сайта http://jabbrik.ru

# Конфигурация
# Сохранение базы данных комнаты каждые X сообщений, это сделано для того чтобы разгрузить нагрузку на бота. Если поставить 1 то будет как обычно, -1 что бы БД вообще не сохранялась
SAVE_COUNT = 5

# Глобальные переменные
# База данных
TALKERS_BD = {}
# Конфиг
TALKERS_CONF = {}
T = {}
# Версия бота, ничего сюда писать не надо, она определяется автоматически (beta)
# Шаблон TALKERS_BOT_VERSION = {'JID':'bot@jabber.ru', 'VERSION':'73rev'}, {'JID':'bot@jabber.ru', 'VERSION':'up73rev'}
TALKERS_BOT_VERSION = {}
# Файд базы данных, %ROOM% - обязательная переменная
TALKERS_FILE = 'settings/%ROOM%/talkers.txt'
# Список жидов чью статистику вести не надо (наприер другие боты в комнате)
TALKERS_NOT_LOG = ['jid@server']
# Ключ (1 - вкл, 0 - выкл.) выключающий статистику по длинне слов
TALKERS_LOG_ON_LENGTH = 0
# Логировать ли сообщения в приват боту? (1 - да, 0 - нет)
TALKERS_LOG_PRIVATE = 0
# Сортировка в ТОПе по сообщениям - 1, по словам - 0
TALKERS_SORT_OF = 0

# - - - - - - НИЧЕГО ТУТ НЕ ИЗМЕНЯЙТЕ, ЕСЛИ У ВАС ПЛАГИН РАБОТАЕТ!!! - - - - - - -
# Если у вас 73 ревизия или любая другая без функции register_stage2_init то поставьте тут 1, в противном случае 0
# НЕ РАБОТАЕТ!!!
TALKERS_PASSIVE_TIMER = 0
# Таймаут даваемый боту на вход в комнаты (по дефолту 10 сек)
TIMEOUT = 10

# "Макет" базы данных
# Плагин считает слова (words), сообщения (messages), слова "/me" (mes)
# file = {'room@conference.jabber.ru':{'jid@jabber.ru':{'nick':'MyName', 'words':120, 'messages':10, 'mes':0, 'words_1_letter':0, 'words_2-3_letter':0, 'words_4-6_letter':0, 'words_up6_letter':0}}}
# Статистика по длинне слов ещё не дореализована!

try:
        a = SERVER
        b = USERNAME
        TALKERS_BOT_VERSION['JID'] = USERNAME.lower()+'@'+SERVER.lower()
        TALKERS_BOT_VERSION['VERSION'] = '73rev'
        TALKERS_BOT_VERSION['COMMENT'] = 'truncated supported!'
except:
        try:
                a = CONNECT_SERVER
                b = JID
                TALKERS_BOT_VERSION['JID'] = JID
                TALKERS_BOT_VERSION['VERSION'] = 'up73rev'
                TALKERS_BOT_VERSION['COMMENT'] = 'full supported!'
        except:
                TALKERS_BOT_VERSION['JID'] = ''
                TALKERS_BOT_VERSION['VERSION'] = 'default'
                TALKERS_BOT_VERSION['COMMENT'] = 'not supported!'
                print 'Unable to check bot version! Please, say me this om mail: gigabyte@ngs.ru or my room stalker@conference.jabbers.ru'

def talkers_load():
        # Функция служит для подгрузки уже созжанной БД или создания пустой БД
        global TALKERS_BD
        global TALKERS_FILE
        global TALKERS_CONF
        for room in GROUPCHATS:
                FILE = TALKERS_FILE.replace('%ROOM%', room)
                if check_file(room,'talkers.txt'):
                        try:
                                TALKERS_BD[room] = eval(read_file(FILE))
                                TALKERS_CONF[room] = {'COUNT':0}
                        except:
                                print 'Error #0 - I can not read file'
                else:
                        print 'Error #1 - I can not create file'
        register_message_handler(talkers_stat)
        if TALKERS_PASSIVE_TIMER:
                q = 'passive mode'
        else:
                q = 'normal mode'
        print 'Loaded '+str(len(TALKERS_BD))+' rooms in talkers base, bot version: '+TALKERS_BOT_VERSION['VERSION']+' - is '+TALKERS_BOT_VERSION['COMMENT']+'. Base loaded in '+q


def talkers_get_top(type, source, body, COUNT=10):
        global TALKERS_BD
        room = source[1] # получаем текущую комнату Get current room
        MAS = []
        if TALKERS_SORT_OF:
                OUT = u'Statistics\nTOP participants\nnumber, user, msg., words, words /me\n'
                MAKET = u'%NUM%. %NICK%\t%MSGS%\t%WORDS%\t%MES%'
                for PP in TALKERS_BD[room].keys():
                        MAS.append([ TALKERS_BD[room][PP]['messages'], TALKERS_BD[room][PP]['words'], TALKERS_BD[room][PP]['mes'], TALKERS_BD[room][PP]['nick'], PP])
                if len(MAS) == 0:
                        reply(type, source, u'database empty')
                        return
                MAS.sort()
                MAS.reverse()
                for i, OO in enumerate(MAS):
                        OUT += MAKET.replace('%NUM%', str(i+1)).replace('%NICK%', OO[3]).replace('%MSGS%', str(OO[0])).replace('%WORDS%', str(OO[1])).replace('%MES%', str(OO[2]))+'\n'
                        if i == COUNT-1:
                                break
        else:
                OUT = u'Statistics\nTOP participants\nnumber, user, words, posts., words /me, с/с\n'
                MAKET = u'%NUM%. %NICK%\t%WORDS%\t%MSGS%\t%MES%\t%SS%'
                for PP in TALKERS_BD[room].keys():
                        SS = round((TALKERS_BD[room][PP]['words'] * 1.0) / (TALKERS_BD[room][PP]['messages'] * 1.0), 1)
                        MAS.append([ TALKERS_BD[room][PP]['words'], TALKERS_BD[room][PP]['messages'], TALKERS_BD[room][PP]['mes'], TALKERS_BD[room][PP]['nick'], PP, SS ])
                if len(MAS) == 0:
                        reply(type, source, u'database empty')
                        return
                MAS.sort()
                MAS.reverse()
                for i, OO in enumerate(MAS):
                        OUT += MAKET.replace('%NUM%', str(i+1)).replace('%NICK%', OO[3]).replace('%MSGS%', str(OO[1])).replace('%WORDS%', str(OO[0])).replace('%MES%', str(OO[2])).replace('%SS%', str(OO[5]))+'\n'
                        if i == COUNT-1:
                                break
        reply(type, source, OUT)
                


def talkers_clear(type, source, body):
        global TALKERS_BD
        global T
        room = source[1] # получаем текущую комнату Get the current room
        jid = get_true_jid(source[1]+'/'+source[2]) # получаем жид
        if user_level(room+'/'+source[2], room)>=20:
                if not T.has_key(room):
                        T[room] = {'time':time.time(), 'jid':jid}
                        reply(type, source, u'Initialized to delete the database ('+str(len(TALKERS_BD[room]))+u' entries), run the command again to remove it!')
                        return
                else:
                        if time.time() - T[room]['time'] <= 60:
                                if jid == T[room]['jid']:
                                        del TALKERS_BD[room]
                                        TALKERS_BD[room] = {}
                                        del T[room]
                                        write_file(TALKERS_FILE.replace('%ROOM%', room), str(TALKERS_BD[room]))
                                        reply(type, source, u'The database is cleared, the action is recorded in the log')
                                        return
                                else:
                                        reply(type, source, u'Confirmation should be the same who initialized the removal!')
                                        return
                        else:
                                reply(type, source, u'Timeout 60 seconds!')
                                del T[room]
                                return
        else:
                reply(type, source, u'Few human!')
                return

def talkers_info(type, source, parameters):
        global TALKERS_BD
        OUT = u'Talkers v2.200 beta\n'
        OUT+= u'Config:\n'
        OUT+= u'TALKERS_SORT_OF (1-msg, 0-wrd): '+str(TALKERS_SORT_OF)+'\n'
        OUT+= u'TALKERS_PASSIVE_TIMER (0-off, 1-on): '+str(TALKERS_PASSIVE_TIMER)+'\n'
        OUT+= u'TALKERS_LOG_ON_LENGTH (0-off, 1-on): '+str(TALKERS_LOG_ON_LENGTH)+'\n'
        OUT+= u'TALKERS_LOG_PRIVATE (0-off, 1-on): '+str(TALKERS_LOG_PRIVATE)+'\n'
        OUT+= u'SAVE_COUNT (-1 - not save): '+str(SAVE_COUNT)+'\n'
        OUT+= u'Bot JID: '+TALKERS_BOT_VERSION['JID']+'\n'
        OUT+= u'Bot Version: '+TALKERS_BOT_VERSION['VERSION']+'\n'
        OUT+= u'Plugin is '+TALKERS_BOT_VERSION['COMMENT']
        reply(type, source, OUT)


def talkers_get(type, source, parameters):
        global TALKERS_BD
        room = source[1] # получаем текущую комнату Get the current room
        jid = get_true_jid(source[1]+'/'+source[2]) # получаем жид
        nick = source[2] # получаем ник obtain nickname

        OUT = u'Statistics\nUser, Msg., Words, /me, с/с\n%NICK%: %MESSAGES% %WORDS% %MES% %SS%'
        if not parameters:
                if TALKERS_BD[room].has_key(jid.lower()):
                        OUT = OUT.replace(u'%NICK%', TALKERS_BD[room][jid.lower()]['nick']).replace(u'%MESSAGES%', str(TALKERS_BD[room][jid.lower()][u'messages'])).replace(u'%WORDS%', str(TALKERS_BD[room][jid.lower()]['words'])).replace(u'%MES%', str(TALKERS_BD[room][jid.lower()]['mes'])).replace(u'%SS%', str( round((TALKERS_BD[room][jid.lower()]['words'] * 1.0) / (TALKERS_BD[room][jid.lower()][u'messages'] * 1.0), 1) ))
                        reply(type, source, OUT)
                else:
                        reply(type, source, u'Looks like you have no statistics')
        else:
                if parameters in ['info', 'clear', 'top']:
                        if parameters == 'top':
                                talkers_get_top(type, source, parameters)
                        elif parameters == 'clear':
                                talkers_clear(type, source, parameters)
                        elif parameters == 'info':
                                talkers_info(type, source, parameters)
                        else:
                                reply(type, source, u'Parameter identified as an internal command, but now it no')

                elif parameters in GROUPCHATS[room]:
                        if TALKERS_BD[room].has_key( get_true_jid(room+'/'+parameters).lower() ):
                                OUT = OUT.replace(u'%NICK%', TALKERS_BD[room][ get_true_jid(room+'/'+parameters).lower() ]['nick']).replace(u'%MESSAGES%', str(TALKERS_BD[room][get_true_jid(room+'/'+parameters).lower()][u'messages'])).replace(u'%WORDS%', str(TALKERS_BD[room][get_true_jid(room+'/'+parameters).lower()]['words'])).replace(u'%MES%', str(TALKERS_BD[room][get_true_jid(room+'/'+parameters).lower()]['mes'])).replace(u'%SS%', str( round((TALKERS_BD[room][get_true_jid(room+'/'+parameters).lower()]['words'] * 1.0) / (TALKERS_BD[room][get_true_jid(room+'/'+parameters).lower()][u'messages'] * 1.0), 1) ))
                                reply(type, source, OUT)
                        else:
                                reply(type, source, u'Like him there are no statistics')
                elif parameters.count('@') == 1:
                        if TALKERS_BD[room].has_key( parameters.lower() ):
                                OUT = OUT.replace(u'%NICK%', TALKERS_BD[room][ parameters.lower() ]['nick']).replace(u'%MESSAGES%', str(TALKERS_BD[room][parameters.lower()][u'messages'])).replace(u'%WORDS%', str(TALKERS_BD[room][parameters.lower()]['words'])).replace(u'%MES%', str(TALKERS_BD[room][parameters.lower()]['mes'])).replace(u'%SS%', str( round((TALKERS_BD[room][parameters.lower()]['words'] * 1.0) / (TALKERS_BD[room][parameters.lower()][u'messages'] * 1.0), 1) ))
                                reply(type, source, OUT)
                        else:
                                reply(type, source, u'Like him there are no statistics')
                else:
                        reply(type, source, u':-P, the parameter is not identified')


def talkers_stat(type, source, body):
        global TALKERS_BD
        global TALKERS_NOT_LOG
        global TALKERS_LOG_ON_LENGTH
        global TALKERS_CONF
        if not TALKERS_LOG_PRIVATE:
                if type == 'private':
                        return
        if body == '':
                return

        room = source[1] # получаем текущую комнату - Get the current room
        if not TALKERS_BD.has_key(room):
                return
        jid = get_true_jid(source[1]+'/'+source[2]) # получаем жид
        nick = source[2] # получаем ник
        jidbot = TALKERS_BOT_VERSION['JID'] # получаем реальный жид бота - Get a real JID bot
        nickbot = get_bot_nick(source[1]) # получаем ник бота в данной комнате - Obtain the nickname the bot in this room

        if (jid.lower() == jidbot.lower()) | (jid.lower() in TALKERS_NOT_LOG) | (jid.lower() == room.lower()) | (type == 'private'):
                return

        if not TALKERS_BD[room].has_key( jid.lower() ):
                TALKERS_BD[room][ jid.lower() ] = {'nick':nick, 'words':0, 'messages':0, 'mes':0, 'words_1_letter':0, 'words_2-3_letter':0, 'words_4-6_letter':0, 'words_up6_letter':0}

        
        TALKERS_BD[room][ jid.lower() ]['messages'] += 1
        if body.count('/me') > 0:
                TALKERS_BD[room][ jid.lower() ]['mes'] += 1
        WORDS = body.split(' ')
        TALKERS_BD[room][ jid.lower() ]['words'] += len( WORDS )

        # [BEGIN STATS OF LENGTH WORDS] Данный кусок считает статистику по длинне слов. Сейчас толком не реализовано. - This piece considers the statistics on long words. We have not really implemented.
        if TALKERS_LOG_ON_LENGTH:
                for W in WORDS:
                        if len(W) == 1:
                                TALKERS_BD[room][ jid.lower() ]['words_1_letter'] += 1
                        elif (len(W) > 1) & (len(W) < 4):
                                TALKERS_BD[room][ jid.lower() ]['words_2-3_letter'] += 1
                        elif (len(W) > 3) & (len(W) < 7):
                                TALKERS_BD[room][ jid.lower() ]['words_4-6_letter'] += 1      
                        elif (len(W) > 6):
                                TALKERS_BD[room][ jid.lower() ]['words_up6_letter'] += 1
        # [END STATS OF LENGTH WORDS]
        
        # [BEGIN SAVE STATS] Данный кусок сохраняет статистику по программе SAVE_COUNT - This piece keeps statistics on the program SAVE_COUNT
        if TALKERS_CONF[room]['COUNT'] >= SAVE_COUNT:
                write_file(TALKERS_FILE.replace('%ROOM%', room), str(TALKERS_BD[room]))
                TALKERS_CONF[room]['COUNT'] = 0
        else:
                TALKERS_CONF[room]['COUNT'] += 1
        # [END SAVE STATS]

if TALKERS_PASSIVE_TIMER:
        print 'This mode os not supported'
else:
        register_stage2_init(talkers_load)
register_command_handler(talkers_get, 'talkers', ['muc','all','new'], 0, 'Shows your statistics in this room.\ninfo - information about the plugin and config.\ntop - TOP10 chaters.\nclear - to clear database.', 'talkers [key/JID/nick]', ['talkers info', 'talkers Guy', 'talkers guy@jsmart.web.id'])

