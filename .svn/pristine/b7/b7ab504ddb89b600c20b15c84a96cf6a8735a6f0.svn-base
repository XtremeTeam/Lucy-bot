#===islucyplugin===
# -*- coding: utf8 -*-
#~#######################################################################
#~ Original Copyright (c) 2008 Burdakov Daniel <kreved@kreved.org>      #
#~ Modified Copyright (c) 2013 - 2014 x-team <xteam@xtreme.im>          #
#~ This file is part of FreQ-bot.                                       #
#~                                                                      #
#~ FreQ-bot is free software: you can redistribute it and/or modify     #
#~ it under the terms of the GNU General Public License as published by #
#~ the Free Software Foundation, either version 3 of the License, or    #
#~ (at your option) any later version.                                  #
#~                                                                      #
#~ FreQ-bot is distributed in the hope that it will be useful,          #
#~ but WITHOUT ANY WARRANTY; without even the implied warranty of       #
#~ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
#~ GNU General Public License for more details.                         #
#~                                                                      #
#~ You should have received a copy of the GNU General Public License    #
#~ along with FreQ-bot.  If not, see <http://www.gnu.org/licenses/>.    #
#~#######################################################################

def echo_handler(t, s, p):
 if p: s.msg(t, context_replace(p, t, s))
 else: s.syntax(t, 'echo')

def say_handler(t, s, p):
 if p: s.room.msg(context_replace(p, t, s))
 else: s.msg(t, '?')

def globmsg_handler(t, s, p):
 if p:
  for i in bot.g.values():
   if i.bot: i.msg(context_replace(p, 'groupchat', i.bot))
   else: i.msg(p)
  s.lmsg(t, 'globmsg_sent', len([i for i in bot.g.keys() if i]))
 else: s.msg(t, '?')

def handler_msg(t, s, p):
 p = p.strip()
 if p.count(' '):
  jid, p, text = p.partition(' ')
  if jid in bot.g.keys(): typ = 'groupchat'
  else: typ = 'chat'
  bot.wrapper.msg(typ, jid, text)
  s.lmsg(t, 'sent')
 else: s.syntax(t, 'msg')

register_command_handler(handler_msg, COMM_PREFIX+'msg', ['superadmin','muc','all','*'], 40, 'Join to a conference, if there is a password write that password right after the name of conference.', COMM_PREFIX+'join <conference> [pass=1234] [botnick]', [COMM_PREFIX+'join botzone@conference.jsmart.web.id', COMM_PREFIX+'join join botzone@conference.jsmart.web.id somebot', COMM_PREFIX+'join join botzone@conference.jsmart.web.id pass=1234 somebot'])
#register_command_handler(handler_admin_leave, COMM_PREFIX+'leave', ['admin','muc','all','*'], 20, 'Leave bot from the current or a specific conference.', COMM_PREFIX+'leave <conference> [reason]', [COMM_PREFIX+'leave botzone@conference.jsmart.web.id sleep', COMM_PREFIX+'leave sleep',COMM_PREFIX+'leave'])
#register_command_handler(handler_admin_msg, COMM_PREFIX+'message', ['admin','muc','all','*'], 40, 'Send message on behalf of bot to a certain JID.', COMM_PREFIX+'message <jid> <message>', [COMM_PREFIX+'message guy@jsmart.web.id how are you?'])
#register_command_handler(handler_admin_say, COMM_PREFIX+'say', ['admin','muc','all','*'], 20, 'Talk through bot.', COMM_PREFIX+'say <message>', [COMM_PREFIX+'say *HI* peoples'])
#register_command_handler(handler_admin_restart, COMM_PREFIX+'restart', ['superadmin','all','*'], 100, 'Restart bot.', COMM_PREFIX+'restart [reason]', [COMM_PREFIX+'restart',COMM_PREFIX+'restart refreshing!'])
#register_command_handler(handler_admin_exit, COMM_PREFIX+'halt', ['superadmin','all','*'], 100, 'Shutdown bot.', COMM_PREFIX+'halt [reason]', [COMM_PREFIX+'halt',COMM_PREFIX+'halt fixing bug!'])
