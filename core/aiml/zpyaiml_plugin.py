#$ neutron_plugin 01

import string
from string import *

def chat_pyaiml(type, source, body):
    reply = k.respond(body)
    smsg(type, source, reply)
    
def handler_pyaiml(type, source, body):
    if type == 'private':
		if not COMMANDS.has_key(string.split(body)[0]):
			chat_pyaiml(type, source, body)    

# Uncomment this if you want PyAIML support.
# Note: sessions are still not implemented.
#register_message_handler(handler_pyaiml)
