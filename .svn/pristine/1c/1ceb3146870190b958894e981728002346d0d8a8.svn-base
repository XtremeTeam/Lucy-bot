#===islucyplugin===
# /* coding: utf8 */
# Tron Bot Plugin
# © X-team

Langs = {   'en': u'English',
			'ja': u'Japanese.', 
			'ru': u'Russian', 
			'auto': u'Аuto', 
			'sq': u'Albanian', 
			'ar': u'Arabic', 
			'af': u'Afrikaans', 
			'be': u'Byelorussian', 
			'bg': u'Bulgarian', 
			'cy': u'Welsh', 
			'hu': u'Hungarian', 
			'vi': u'Vietnamese', 
			'gl': u'Galician', 
			'nl': u'Dutch', 
			'el': u'Greek', 
			'da': u'Danish', 
			'iw': u'Hebrew', 
			'yi': u'Yiddish', 
			'id': u'Indonesian', 
			'ga': u'Irish', 
			'is': u'Iceland', 
			'es': u'Spanish', 
			'it': u'Italian', 
			'ca': u'Catalan', 
			'zh-CN': u'Chinese', 
			'ko': u'Korean', 
			'lv': u'Latvian', 
			'lt': u'Lithuanian', 
			'mk': u'Macedonian', 
			'ms': u'Malay', 
			'mt': u'Maltese', 
			'de': u'German', 
			'no': u'Norway', 
			'fa': u'Persian', 
			'pl': u'Polish', 
			'pt': u'Portuguese', 
			'ro': u'Romanian', 
		 	'sr': u'Serbian', 
		 	'sk': u'Slovak', 
		 	'sl': u'Slovenian',
		 	'sw': u'Swahili', 
		 	'tl': u'Tagalog', 
		 	'th': u'Thai', 
		 	'tr': u'Turkish', 
		 	'uk': u'Ukrainian', 
		 	'fi': u'Finland', 
		 	'fr': u'French', 
		 	'hi': u'Hindi', 
		 	'hr': u'Croatian', 
		 	'cs': u'Czech', 
		 	'sv': u'Swedish', 
		 	'et': u'Estonian'}

from re import search
from urllib2 import quote, urlopen

uagent = "Opera/9.60 (J2ME/MIDP; Opera Mini/4.2.13337/724; U; ru)"

def uHTML(text):
	from HTMLParser import HTMLParser 
	text = text.replace("<br>", "\n").replace("</br>", "\n").replace("<br />", "\n")
	text = HTMLParser().unescape(text)
	del HTMLParser
	return text

def read_url(link, Browser = False):
	from urllib2 import Request
	req = Request(link)
	if Browser:
		req.add_header('User-agent', Browser)
	site = urlopen(req)
	data = site.read()
	del Request
	return data

def parse(code):
	match = search('class="t0">', code)
	end = code[match.end():]
	return end[:search("</div>", end).start()]

def gTrans(fLang, tLang, text):
	url = "http://translate.google.ru/m?hl=ru&sl=%(fLang)s&tl=%(tLang)s&ie=UTF-8&prev=_m&q=%(text)s"
	text = quote(text.encode('utf-8'))
	x = url % vars()
	try:
		time.sleep(0.2)
		return uHTML(parse(read_url(x, uagent)))
	except Exception, e:
		return "%s: %s" % (e.__class__.__name__, e.message)

def gAutoTrans(mType, source, text):
	if text:
		repl = gTrans("auto", "en", text).decode("utf-8")
		if text == repl:
			repl = u"Перевод %s => %s:\n%s" % ("auto", "en", gTrans("auto", "en", text).decode("utf-8"))
		else:
			repl = u"Перевод %s => %s:\n%s" % ("auto", "ru", repl)
	else:
		repl = u"Недостаточно параметров."
	reply(mType, source, repl)

def gTransHandler(mType, source, args):
	if args and len(args.split()) > 2:
		(fLang, tLang, text) = args.split(None, 2)
		reply(mType, source, u"Перевод %s => %s:\n%s" % (fLang, tLang, gTrans(fLang, tLang, text).decode("utf-8")))
	else:
		answer = u"\nДоступные языки:\n"
		for a, b in enumerate(sorted([x + u" — " + y for x, y in Langs.iteritems()])):
			answer += u"%i. %s.\n" % (a + 1, b)
		reply(mType, source, answer.encode("utf-8"))

register_command_handler(gTransHandler, 'tr', ['help','all'], 10, 'Переводчик.\nПеревод с одного языка на другой. Используется Google Translate.', 'перевод <исходный_язык> <нужный_язык> <текст>', ['перевод en ru hello world', 'перевод ru en привет, мир'])
register_command_handler(gAutoTrans, '!', ['help','all'], 10, 'Перевод с одного языка на другой с автоопределением. Используется Google Translate.', '! <текст>', ['! hello', '! привет'])