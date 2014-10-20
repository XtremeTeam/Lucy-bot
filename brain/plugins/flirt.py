#===islucyplugin===
# -*- coding: utf-8 -*-

#   Lucy's Plugin
#   flirt_plugin.py
#   Coded by KiDo
#   best-rapper@qip.ru
#   best-rapper@jabber.org
#   konvict_massari@yahoo.com
#   www.facebook.com/KiDo.Konvict
#   www.twitter.com/KiDo3Konvict

def handler_flirt(type, source, parameters):
        flirts = [u'Hey I\'m looking for treasure, Can I look around your chest?',u'If being sexy was a crime, you\'d be guilty as charged!',u'Hi, I\'m an astronaut, and my next mission is to explore Uranus.',u'Is your name Summer? \'Cause you are as hot as heck.',u'You are a 9.999. Well, you\'d be a perfect 10 if you were with me.',u'If I could rearrange the alphabet, I\'d put U and I together.',u'Do you know what\'d look good on you? Me.',u'Your Daddy must have been a Baker, cos you got the nicest set of buns I\'ve ever saw.',u'I know a great way to burn off the calories in that cake you just ate.',u'Was your Father a mechanic? Then how did you get such a finely tuned body?',u'I\'m good at math, U+I=69',u'Help, somethings wrong with my eyes - I just can\'t take them off you.',u'Hey baby, you must be a light switch, coz every time I see you, you turn me on!',u'Do you have a Bandaid? Cos I just scraped my knee falling for you.',u'You gotta be tired \'cause you\'ve been running through my mind all day.',u'Do you have a map? \'Cause Honey, I just keep gettin\' lost in your eyes.',u'You\'re like a dictionary - you add meaning to my life!',u'I think I can die happy now, coz I\'ve just seen a piece of heaven',u'You are so beautiful that you give the sun a reason to shine.',u'Excuse me, can I borrow your phone number? I seem to have lost mine.',u'You\'ve made me so nervous that I\'ve totally forgotten forgotten my standard pick-up line.',u'Is your name Gillette? \'Cause you\'re the best a man can get.',u'It\'s not my fault I fell in love. You are the one that tripped me.',u'I\'ll give you a nickel if you tickle my pickle.',u'Was your father a thief? \'Cause someone stole the stars from the sky and put them in your eyes.',u'There\'s just one thing your eyes haven\'t told me yet....your phone number.\'You must be Jamaican, because Jamaican me crazy.']
        nick = random.choice(GROUPCHATS[source[1]].keys())
        flirt = random.choice(flirts)
        themsg = nick+': '+flirt
        msg(source[1], themsg)
register_command_handler(handler_flirt, 'flirt', ['flirt','en','all'], 0, 'Type flirt, so the bot will choose a pick up line, and flirt with a random user.')


