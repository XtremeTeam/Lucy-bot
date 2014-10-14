#===islucyplugin===
# -*- coding: utf-8 -*-
#  Lucy's Plugin
#  recoded by marcus. thanx my freinds for the idea :)
#  exclusive for http://jabberuk.dyndns.org

virus = [u'Net-gay ', u'tiny gay', u'Trojan.gay', u'097/Crown.B', u'911 gay ', u'Dropper.Win32 gaydom', u'Worm.Win32.lez/gay', u'Win32.HLLM.Graz.00', u'VBS.Redlof.a', u'gay fucker', u'Program.Hiddengay.origin', u'a very tiny gay', u'unknown', u'HUH']
act = [u'[sorry but there are so many i am turning gay', u'[cleared the room of gayness]',u'[removed]',u'[under carantine]']
lic = [u'[blacklist]', u'[whitelist]']

def handler_test_virus(type, source, parameters):

        reply(type,source,u'scanning room for Gayness...')

        time.sleep(random.randrange(0, 6))

        reply(type,source,u'...starting Anti gayness Security. Please wait...')

        time.sleep(random.randrange(0, 30))

        ocupants = []

        for i in GROUPCHATS[source[1]]:

                if GROUPCHATS[source[1]][i]['ishere'] == 1:

                        ocupants.append(i)

        if len(ocupants) > 10:

                count = random.randrange(0, 10)

        else:

                count = random.randrange(0, len(ocupants))

        if count == 0:

                res= u'room without viruses'

        else:

                res = u'WARNING detected '+str(count)+u' gays:'

                for vir in range(0, count):
                    oc=random.choice(ocupants)
                    vi=random.choice(virus)
                    ac=random.choice(act)
                    if ac == act[2]:
                        order_kick(source[1],oc,u'you will remove after your rejoined you will no longer be a gay')
                    if ac == act[3]:
                        order_visitor(source[1],oc,u'your gay bug will remove after your rejoin')
                    res += '\n'+oc+' ('+vi+') '+ac

        reply(type,source, res)
def handler_antivirus_update(type, source, parameters):
        lc=random.choice(lic)
        if lc == lic[1]:
                reply(type,source,u'Connecting to anti gay Update center...')
                time.sleep(random.randrange(0, 3))
                reply(type,source,u'starting update ================>100%')
                reply(type,source,u'update succesfully completed')
        if lc == lic[0]:
                reply(type,source,u'Connecting to  Update center...')
                time.sleep(random.randrange(0, 3))
                reply(type,source,u'you to gay to own a copy of anti gauness. your key have been banned. please buy licence key')

register_command_handler(handler_test_virus, COMM_PREFIX+'antigay', ['all'], 30, 'clean room from gay people‚', 'scan', ['scan'])
register_command_handler(handler_antivirus_update, COMM_PREFIX+'update', ['all'], 30, 'update for bot anti gayness datat base‚', 'av_update', ['av_update'])

