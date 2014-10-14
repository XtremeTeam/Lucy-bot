#===islucyplugin===
# -*- coding: utf-8 -*-

#  Lucy's Plugin
#  ext_plugin.py  v1.0

# Coded by Nikk  
# Exclusive for www.virtualtalk.org




import urllib2,re,urllib
from re import compile as re_compile
strip_tags = re_compile(r'<[^<>]+>')

def handler_ext(type, source, parameters):
	if parameters:
		try:
			req = urllib2.Request('http://www.file-extensions.org/' + parameters.encode('windows-1251')+'-file-extension')		
			r = urllib2.urlopen(req)
			target = r.read()
			od = re.search('description:</h3><p>',target)
			message = target[od.end():]
			message = message[:re.search('</p>',message).start()]
			message = decode(message)		
			message = u'Result for ' +'.\n' + unicode(message,'windows-1251')
                        reply(type, source, message)
			
		except:
			reply(type,source,u'nothing to find :(')
			return
	else:
		reply(type,source,u'enter title of extension')
	

def decode(text):
    return strip_tags.sub('', text.replace('<br />','').replace('<br>','')).replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('\t','').replace('||||:]','').replace('>[:\n','')

register_command_handler(handler_ext, COMM_PREFIX+'ext', ['all'], 0, 'find description of extention ', 'ext <word>', ['ext rar'])
