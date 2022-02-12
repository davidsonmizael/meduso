from core import functions as fun
import time
from datetime import datetime
from core import Bot

bot = Bot('http://localhost:5000')

print("Startup")
bot.startUp()
while True:
	print("Sending heartbeat")
	bot.heartBeat()
	print("Looking for commands")
	cmds = bot.lookForCommands()
	for c in cmds:
		print("Doing command: " + c['type'])
		r = bot.doCommand(c['id'], c['type'], c['parameter'])
	time.sleep(20)