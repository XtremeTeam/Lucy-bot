#===islucyplugin===
# -*- coding: utf-8 -*-

#Imported from isida by quality(quality@botaq.net)
#Official conference - botaq@conference.jabber.ru
#Thanks to Disabler - http://isida.googlecode.com/

def youtube(type, source, text):
	text = text.lower()
	text = text.encode('utf-8')
	text = text.replace('\\x','%')
	text = text.replace(' ','%20')
	link = 'http://www.youtube.com/results?search_type=&search_query='+text+'&aq=f'
	f = urllib.urlopen(link)
	tube = f.read()
	f.close()
	tube = tube.split('video-title video-title-results')
	tube = tube.split('video-run-time')

	tmass = []
	ltube = len(tube)
	smsg = u'found: '+str(ltube-1)
	if ltube > 4: ltube=4
	for i in range(1,ltube):

		msg = tube[i].decode('utf')
		idx = msg.index('>')
		imsg = msg[idx+1:]
		idx = imsg.index('<')
		mtime = imsg[:idx]

		idx = msg.index('/watch?v=')
		imsg = msg[idx:]
		idx = imsg.index('\"')
		imsg = imsg[:idx]
		murl = 'http://www.youtube.com'+imsg

		idx = msg.index('title=\"')
		imsg = msg[idx+7:]
		idx = imsg.index('\"')
		imsg = imsg[:idx]
		imsg = rss_replace(imsg)
		msg = murl +'\t'+ imsg +' ('+ mtime +')'
		tmass.append(msg)
	
	msg = smsg + '\n'
	for i in tmass: msg += i + '\n'
	msg = msg[:-1]
	reply(type, source, msg)
	
	


	
register_command_handler (youtube, COMM_PREFIX+'youtube', ['all', 'all', 'info'], 10, 'Search for YouTube', 'YouTube <word>', ['YouTube anime'])
