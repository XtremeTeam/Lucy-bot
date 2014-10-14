#===islucyplugin===
# -*- coding: utf-8 -*-

def change_bot_status(gch, status, show):
        prs=xmpp.protocol.Presence(gch+'/'+get_bot_nick(gch))
        if status:
                prs.setStatus(status)
        if show:
                prs.setShow(show)
        JCON.send(prs)

def status_change_tmp(type, source, parameters):
        if not parameters:
                reply(type, source, u'did you forget to write something?')
                return
        
        WAR_STMSG = u'attention!\n'+parameters
        WAR_STATUS = 'dnd'

        OLD_STATUS = {}
        for GCH in GROUPCHATS.keys():
                BOTNICK = get_bot_nick(GCH)
                if BOTNICK in GROUPCHATS[GCH]:
                        OLD_STATUS[GCH] = {'status':GROUPCHATS[GCH][BOTNICK]['status'], 'stmsg':GROUPCHATS[GCH][BOTNICK]['stmsg']}
                        change_bot_status(GCH, WAR_STMSG, WAR_STATUS)
        reply(type, source, u'Status changed %s conf, wait 30 seconds and il be back!' % (str(len(OLD_STATUS))))
        time.sleep(30)
        for GCH in OLD_STATUS.keys():
                change_bot_status(GCH, OLD_STATUS[GCH]['stmsg'], OLD_STATUS[GCH]['status'])
        reply(type, source, u'Status in the same position!')

register_command_handler(status_change_tmp, COMM_PREFIX+'gstatus', ['admin','all'], 100, 'Global change of status with the notice for 30 seconds', 'gstatus [notice]', ['gstatus Hello'])
