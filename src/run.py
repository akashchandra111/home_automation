#! /usr/bin/python

from interface.webui import web_interface
from interface.bot import	bot 

import threading

if __name__ == '__main__':

	# Defining 2 seperate processes for bot and web
	bot = threading.Thread(target=bot, args=())
	web_interface = threading.Thread(target=web_interface, args=())

	# Starting the processes individually
	bot.start()
	web_interface.start()

	# Join after work is complete, however not going to occur ever
	bot.join()
	web_interface.join()
