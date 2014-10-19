#===islucyplugin===
# -*- coding: utf-8 -*-

#   Lucy's Plugin
#   numbers_plugin.py
#   Coded by KiDo
#   best-rapper@qip.ru
#   best-rapper@jabber.org
#   konvict_massari@yahoo.com
#   www.facebook.com/KiDo.Konvict
#   www.twitter.com/KiDo3Konvict

JIDs = []
def handler_numbers(type, source, parameters):
        groupchat = source[1]
        if check_file(groupchat,'numbers.txt'):
                jid = get_true_jid(source)
                DBPATH = 'settings/'+groupchat+'/numbers.txt'
                numbersdb = eval(read_file(DBPATH))
                if parameters:
                        if len(parameters.strip().split()) == 1:
                                nick = source[2]
                                number = parameters.split()[0]
                                if not jid in numbersdb.keys():
                                        numbersdb[jid] = jid
                                        numbersdb[jid] = {}
                                        numbersdb[jid]['nick'] = nick
                                        numbersdb[jid]['number'] = number
                                        write_file(DBPATH, str(numbersdb))
                                        reply(type, source, u'OK, your number has been added.')
                                else:                        
                                        reply(type, source, u'You already gave me your number.')
                                
                        
                        else:
                                reply(type, source, u'Type help pnumber to learn how to use this command.')
                elif not parameters:
                        if jid in JIDs:
                                reply(type, source, u'You already asked for number, wait 24 hours, then you can ask for another one.')
                                time.sleep(86400)
                                JIDs.remove(jid)
                        else:
                                njid = random.choice(numbersdb.keys())
                                nick = numbersdb[njid]['nick']
                                number = numbersdb[njid]['number']
                                JIDs.append(jid)
                                reply('private', source, nick+u': '+number)
                
                

register_command_handler(handler_numbers, 'pnumber', ['numbers','en','all'], 10, 'Type pnumber to get a random phone number of a user who has entered his number before, or type pnumber your number, to add your number to the database.','pnumber |number',['pnumber','pnumber +17633017625'])
                        
