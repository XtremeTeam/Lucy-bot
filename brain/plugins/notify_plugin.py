#===istalismanplugin===
# -*- coding: utf-8 -*-

#   Talisman Plugin
#   notify_plugin.py
#   Coded by KiDo
#   best-rapper@qip.ru
#   best-rapper@jabber.org
#   konvict_massari@yahoo.com
#   www.facebook.com/KiDo.Konvict
#   www.twitter.com/KiDo3Konvict

ToBeNotifieden = []

def handler_notifyen(type, source, parameters):
        global ToBeNotifieden
        nick = source[2]
        groupchat = source[1]
        if parameters == '1':
                reply(type, source, u'OK, now you will be notified.')
                nicks = GROUPCHATS[groupchat].keys()
                if nick in nicks:
                        ToBeNotifieden.append(nick)
        elif parameters == '0':
                ToBeNotifieden.remove(nick)
                reply(type, source, u'OK, you will not be notified anymore.')
                        
                
def atjoin_notify(groupchat, nick, aff, role):
        global ToBeNotifieden
        for i in range(0,len(ToBeNotifieden)):
                if ToBeNotifieden[i] in GROUPCHATS[groupchat].keys():
                        if get_true_jid(groupchat+'/'+ToBeNotifieden[i]) in ADMINS:
                                jid = get_true_jid(groupchat+'/'+nick)
                                message = jid + ' has joined: ' + groupchat + ' as ' + nick
                                to = groupchat+u'/'+ToBeNotifieden[i]
                                msg(to, message)
                                return
                        else:
                                message = nick + ' has joined: ' + groupchat
                                to = groupchat+u'/'+ToBeNotifieden[i]
                                msg(to, message)
                                return

                
        
register_command_handler(handler_notifyen, COMM_PREFIX+'notify', ['notify','en','all'], 10, 'Avril will send you a private message notifying you with the name of the user who joined the room immediately.\nYou can type 1 to be notified, or 0 to cancel.', 'notify <parameters 1|0>', ['notify 1'])
register_join_handler(atjoin_notify)
