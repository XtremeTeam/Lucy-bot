#===islucyplugin===
# -*- coding: utf-8 -*-

def handler_rejoinall(type, source, parameters):
#   print "rejoinall"
#   print type, source, parameters
#   print dir(parameters)

   if check_file(file='chatrooms.list'):
     lgcts = eval(read_file(GROUPCHAT_CACHE_FILE))
#     print GROUPCHATS.keys()
     for groupchat in lgcts: #GROUPCHATS:
       leave_groupchat(groupchat, u'leaving due to command rejoinall!')
          
       gc=lgcts[groupchat]  #GROUPCHATS[grc]
       join_groupchat(groupchat,gc["nick"],gc["passw"])
   else:
     print 'Error: unable to create chatrooms list file!'

def handler_changestatus(type, source, parameters):
   statusdict={u"xa":u"xa",u"dnd":u"dnd",u"online":u"online",u"away":u"away",u"chat":u"chat"}

   print source
   if check_file(file='statuses.list'):
     groupchatstatus = eval(read_file(GROUPCHAT_STATUS_CACHE_FILE))
     if parameters:      
       # если статус был записан в список уже то тогда его берем | if the status was recorded in the list, then bot will use it
       if groupchatstatus.has_key(source[1]):
         cstatus=groupchatstatus[source[1]]
       else: #иначе берем стандартные параметры по умолчанию | otherwise bot will use the standard default settings
         cstatus=["online",None]

       sts=parameters.split(' ')
       if statusdict.has_key(sts[0].lower()):
         cstatus[0]=statusdict[sts[0].lower()]
         if sts[1:]!= []:
           cstatus[1]=" ".join(sts[1:])
       else:
         cstatus[1]=parameters

       groupchatstatus[source[1]]=cstatus
     else:
       del groupchatstatus[source[1]]
     write_file(GROUPCHAT_STATUS_CACHE_FILE,str(groupchatstatus))
   else: 
     print 'Error: unable to create chatrooms status list file!'

   if check_file(file='chatrooms.list'):
     lgcts = eval(read_file(GROUPCHAT_CACHE_FILE))
     gc=lgcts[source[1]]
     join_groupchat(source[1],gc["nick"],gc["passw"])
   else:
     print 'Error: unable to create chatrooms list file!'

register_command_handler(handler_rejoinall, COMM_PREFIX+'rejoinall', ['admin','muc','all'], 100, 'Rejoin bot to conferences according to database.', COMM_PREFIX+'rejoinall', [COMM_PREFIX+'rejoinall'])

register_command_handler(handler_changestatus, COMM_PREFIX+'setstatus', ['muc','admin','all'],100, 'Change bot status in the current conference, if two parameters are not mentioned, bots will use the default status.', COMM_PREFIX+'setstatus[online|chat|away|xa|dnd] [message]', [COMM_PREFIX+'setstatus chat','setstatus dnd', COMM_PREFIX+'setstatus away meeting!!', COMM_PREFIX+'setstatus'])
