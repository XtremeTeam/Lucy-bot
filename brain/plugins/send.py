#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  send_plugin.py

#  Initial Copyright Ac 2007 Als <Als@exploit.in>
#  Help Copyright Ac 2007 dimichxp <dimichxp@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

sendqueue={}


def handler_send_save(ltype, source, parameters):
   groupchat=source[1]
   if GROUPCHATS.has_key(groupchat):
      nicks = GROUPCHATS[groupchat].keys()
      args = parameters.split(' ')
      date=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
      fromnick=source[2]+u' Š¾Š. '+source[1]+u' Š2 '+date+u' (UTC) they asked me to send you the following message:\n\n'
      if len(args)>=2:
         nick = args[0]
         body = ' '.join(args[1:])
         if nick == 'botadmin':
            reply(ltype, source, u'I will send')
            msg(ADMINS[0], fromnick+body)
            return
         if get_bot_nick(groupchat) != nick:
            tojid = groupchat+'/'+nick
            if nick in nicks and GROUPCHATS[groupchat][nick]['ishere']==1:
               reply(ltype, source, u'Here')
            else:
               if not groupchat in sendqueue:
                  sendqueue[groupchat]=groupchat
                  sendqueue[groupchat]={}
               if not tojid in sendqueue[groupchat]:
                  sendqueue[groupchat][tojid] = tojid
                  sendqueue[groupchat][tojid] = []
               sendqueue[groupchat][tojid].append(fromnick+body)
               reply(ltype, source, u'I willl send')
               if check_file(groupchat,file='send.txt'):
                  sendfp='settings/'+groupchat+'/send.txt'
                  write_file(sendfp,str(sendqueue[groupchat]))
               else:
                  print 'send_plugin.py error'
                  pass

def handler_send_join(groupchat, nick, aff, role):
   tojid = groupchat+'/'+nick
   if groupchat in sendqueue:
      if sendqueue[groupchat].has_key(tojid) and sendqueue[groupchat][tojid]:
         for x in sendqueue[groupchat][tojid]:
            msg(tojid, x)
         sendqueue[groupchat][tojid] = []
         if check_file(groupchat,file='send.txt'):
            sendfp='settings/'+groupchat+'/send.txt'
            write_file(sendfp,str(sendqueue[groupchat]))
         else:
            print 'send.py error'
            pass
   else:
      pass
      
def get_send_cache(gch):
   sfc='settings/'+gch+'/send.txt'
   if not check_file(gch,'send.txt'):
      print 'error with caches in send.py'
      raise
   try:
      cache = eval(read_file(sfc))
      sendqueue[gch]={}
      sendqueue[gch]=cache
   except:
      pass   

register_join_handler(handler_send_join)
register_command_handler(handler_send_save, 'psay', ['muc','all'], 0, 'Remembers the message in base and transfers its specified person as soon as it will come into conference.', 'psay <To whom> <message>', ['psay Nick hello! Š.ŠŸŠ+ŠŸŠ?NS Nick666'])

register_stage1_init(get_send_cache)
