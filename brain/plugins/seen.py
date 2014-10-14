#--bot
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  seen_plugin.py       

#  Initial Copyright © 2010 Tuarisa <Tuarisa@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.


seen_stats = {}


def handler_leave(groupchat, nick, aff, jid):
#       msg(groupchat, u'blabla')
        jid=get_true_jid(groupchat+'/'+nick)
        seen_stats[jid]=[time.gmtime(), 1, nick]
#       seen_stats[nick[leave]]=1       
#       msg(groupchat, seen_stats[nick][time])
        
        
def handler_join(groupchat, nick, aff, jid):
#       msg(groupchat, u'blabla')
        jid=get_true_jid(groupchat+'/'+nick)
        seen_stats[jid]=[time.gmtime(), 0, nick]
#       seen_stats[nick[leave]]=0       
#       msg(groupchat, seen_stats[nick[leave]])
        

def handler_seen(type, source, parameters):

        nicks = GROUPCHATS[source[1]].keys()
        if not parameters:
                reply(type, source, u'hmmm?')  
                return
                
        if not parameters.count('@'):
        
                nick=parameters
                truejid=get_true_jid(source[1]+'/'+nick)
                if not nick in nicks:
                        
                        reply(type, source, u'who?')
                        return
        else:
                truejid=parameters
                jids=seen_stats.keys()

                if not truejid in jids:
                        reply(type, source, u'was he here?')
                        return
        time_now = time.mktime(time.gmtime())
        time_diff = time_now - time.mktime(seen_stats[truejid][0])
        if seen_stats[truejid][1]==0:
                reply(type, source, u'<' + parameters+u'> he was here ' +  timeElapsed(time_diff) +  u' ago with nickname <'+ seen_stats[truejid][2] +u'>')
                return
                                
        else:
                reply(type, source, u'<' + parameters+u'> was there ' +  timeElapsed(time_diff) + u' ago with nickname <'+seen_stats[truejid][2]+u'>')
                return

                        
         
        


register_leave_handler(handler_leave)
        
register_join_handler(handler_join)

register_command_handler(handler_seen, 'seen', ['info', 'all'], 10, 'to get info of a person that was last online', 'seen <nick>', ['seen bob'])
