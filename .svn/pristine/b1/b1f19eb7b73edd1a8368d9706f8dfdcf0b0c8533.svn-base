#===islucyplugin===
# -*- coding: utf-8 -*-

import re
import urllib2
class InvalidFormat:
	def __init__(self):
		pass

class RussianPostParser:
	def __init__(self):
		self.header = []
		self.result = []

		self.headers_count = 0
		
		self.BLOCK_STARTED = 0
		self.BLOCK_END = 1

	def process_header(self, elements):
		global header, headers_count
		if self.headers_count == 0:
			self.header = elements
			self.headers_count+=1
		elif self.headers_count == 1:
			self.header = self.header[0:2] + elements[0:2] + self.header[3:7] + elements[2:4] + self.header[8:]
			self.headers_count+=1

	def process_data(self, elements):
		if len(self.header) != len(elements):
			raise InvalidFormat()
		self.result.append(elements)

	def process_block(self, block_class, elements):
		if block_class.count('HEADER'):
			self.process_header(elements)
		else:
			self.process_data(elements)


	def Parse(self, data):
		block_class = ''
		state = None
		elems = []

		for x in [x.strip().replace('&nbsp;', '').decode('cp1251').encode('utf8') for x in data[data.index('<TABLE WIDTH="" CELLSPACING="1" CELLPADDING="2" BORDER="0" ALIGN="center">'):data.index('</TABLE>')].replace('\r','').split('\n')]:
			if not x: continue
			if x[0:4] == '<TR ':
				if state == self.BLOCK_STARTED:
					raise InvalidFormat()
				try:
					block_class = re.search('CLASS="([^"]*)"', x).group(1)
				except:
					raise InvalidFormat()
				state = self.BLOCK_STARTED
			elif x[0:4] == '<TD ':
				if state != self.BLOCK_STARTED:
					raise InvalidFormat()
				try:
					elems.append(re.match('<TD .*>(.*)</TD>', x).group(1))
				except:
					raise InvalidFormat()
			elif x[0:4] == '</TR':
				if state != self.BLOCK_STARTED:
					raise InvalidFormat()
				self.process_block(block_class, elems)
				state = self.BLOCK_END
				elems = []
	def filter(self, lst, columns):
		ret=[]
		for i in xrange(0, len(lst)):
			if not (i in columns): continue
			ret+=[lst[i]]
		return ret
	def Result(self, columns):
		return [self.filter(x, columns) for x in self.result]
	def Header(self, columns):
		return self.filter(self.header, columns)

def FormatTable(table):
	if not table: return []
	sizes = [max([len(x[i]) for x in table]) for i in xrange(0, len(table[0]))]
	return [[x[i]+'\t'*((sizes[i]-len(x[i]))/8+1) for i in xrange(0, len(x))] for x in table]
	
def DoSearch(tracknum):
	p = RussianPostParser()
	try:
		data = urllib2.urlopen('http://info.russianpost.ru/servlet/post_item?action=search&show_form=no&barCode='+tracknum).read()
		p.Parse(data)
	except:
		print 'shit happened...'
		raise
	ret=''
	for x in FormatTable([p.Header([0,1,5])]+p.Result([0,1,5])):
		ret+=reduce(lambda x,y:x+y, x)+'\n'
	return ret

def handler_post(type, source, parameters):
	if not parameters:
		reply(type,source,u'Track in studio')
		return
	reply(type, source, 'Result: \n'+DoSearch(parameters.strip()))

register_command_handler(handler_post, 'post', ['muc'], 0, 'Something shows.', 'post something', ['yes'])
