#########################################################################
#									#
#	Written By: Akash Chandra					#
#									#
#########################################################################

'''
	This is the bot interface
	What it does is, it parses the command received over telegram messenger to this bot
	Sends the data to arduino over bluetooth and notifies the user about the change
'''

import House.house_loader as hl		# Contains backUpper and loader for house framework
import config

import Text.text as text		# Contains Text
import logging				# Used to log for errors

import telegram				# Telegram API library
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def bot():
	#	Initializing Bot
	updater = Updater(token='405173123:AAGRJuNTCgf3Fz0hfKKHxvc_fyJUlpzeC4Q')
	dispatcher = updater.dispatcher
	
	#	Logging
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

	#	Command Handlers
	dispatcher.add_handler(CommandHandler('start', start))
	dispatcher.add_handler(CommandHandler('help', help))

	#	Message Handlers
	dispatcher.add_handler(MessageHandler(Filters.text, msg_handler))
	
	#	error handler
	dispatcher.add_error_handler(error)

	#	polling starting point
	updater.start_polling()

	#	Ctrl+C handler
	updater.idle()


########	start
def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text=text.start_text)

########	help
def help(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text=text.help_text)

########	message handler
selected_room = None
def msg_handler(bot, update):
	global h
	global selected_room

	data = update.message.text.split(' ')

	if data[0] == 'add_room' or data[0] == 'ar' and len(data) == 2:
		bot.send_message(chat_id=update.message.chat_id, text=config.h.add_room(data[1]))
	elif data[0] == 'rem_room' or data[0] == 'rr' and len(data) == 2:
		bot.send_message(chat_id=update.message.chat_id, text=config.h.rem_room(data[1]))
	elif data[0] == 'ls_room' or data[0] == 'lr' and len(data) == 1:
		if config.h.ls_room() == '':
			bot.send_message(chat_id=update.message.chat_id, text='No rooms added/present')
		else:
			bot.send_message(chat_id=update.message.chat_id, text=config.h.ls_room())
	elif data[0] == 'select' or data[0] == 's' and len(data) == 2:
		for i in config.h.room:
			if i.name == data[1]:
				bot.send_message(chat_id=update.message.chat_id, text=i.name+' selected')
				selected_room = i
				break

		if selected_room == None:
			bot.send_message(chat_id=update.message.chat_id, text='No such room exists')
	elif data[0] == 'cur_room' or data[0] == 'cr' and len(data) == 1:
		if selected_room == None:
			bot.send_message(chat_id=update.message.chat_id, text='No Room selected currently')
		else:
			bot.send_message(chat_id=update.message.chat_id, text=selected_room.name)
	elif data[0] == 'save_settings' or data[0] == 'ss' :
		if len(data) == 2:
			hl.house_load('w', config.h, data[1])
			bot.send_message(chat_id=update.message.chat_id, text='Settings saved')
		elif len(data) == 1:
			hl.house_load('w', config.h)
			bot.send_message(chat_id=update.message.chat_id, text='Settings saved')			
		else:
			bot.send_message(chat_id=update.message.chat_id, text='Wrong number of arguments given')
	elif data[0] == 'load_settings' or data[0] == 'ls':
		if len(data) == 2:
			config.h = hl.house_load('r', config.h, data[1])
			bot.send_message(chat_id=update.message.chat_id, text='Settings loaded')
		elif len(data) == 1:
			config.h = hl.house_load('r', config.h)
			bot.send_message(chat_id=update.message.chat_id, text='Settings loaded')			
		else:
			bot.send_message(chat_id=update.message.chat_id, text='Wrong number of arguments given')
	else:
		if selected_room == None:
				bot.send_message(chat_id=update.message.chat_id, text='No Room selected currently')
		else:
			if data[0] == 'add_dev' or data[0] == 'ad' and len(data) == 3:
				bot.send_message(chat_id=update.message.chat_id, text=selected_room.add_dev(data[1], int(data[2])))
			elif data[0] == 'rem_dev' or data[0] == 'rd' and len(data) == 2:
				bot.send_message(chat_id=update.message.chat_id, text=selected_room.rem_dev(data[1]))
			elif data[0] == 'on' or data[0] == '1' and len(data) == 2:
				counter = 0
				for i in selected_room.device:
					if i.name == data[1]:
						i.on()
						config.msg_handler.send(i.get_data())
						bot.send_message(chat_id=update.message.chat_id, text=i.name+' is on')
						break
					else:
						counter += 1
					if counter == len(selected_room.device):
						bot.send_message(chat_id=update.message.chat_id, text='No such device exists')
			elif data[0] == 'off' or data[0] == '0' and len(data) == 2:
				counter = 0
				for i in selected_room.device:
					if i.name == data[1]:
						i.off()
						config.msg_handler.send(i.get_data())
						bot.send_message(chat_id=update.message.chat_id, text=i.name+' is off')
					else:
						counter += 1
					if counter == len(selected_room.device):
						bot.send_message(chat_id=update.message.chat_id, text='No such device exists')
			elif data[0] == 'set_lev' or data[0] == 'sl' and len(data) == 3:
				counter = 0
				for i in selected_room.device:
					if i.name == data[1]:
						i.set_level(int(data[2]))
						config.msg_handler.send(i.get_data())
						bot.send_message(chat_id=update.message.chat_id, text=i.name+' is set at '+str(i.level)+'%')
					else:
						counter += 1
					if counter == len(selected_room.device):
						bot.send_message(chat_id=update.message.chat_id, text='No such device exists')

			elif data[0] == 'ls_dev' or data[0] == 'ld' and len(data) == 1:
				if selected_room.ls_dev() == '':
					bot.send_message(chat_id=update.message.chat_id, text='No devices added/present')
				else:
					bot.send_message(chat_id=update.message.chat_id, text=selected_room.ls_dev())
			elif data[0] == 'ls_pin' or data[0] == 'lp' and len(data) == 1:
				if selected_room.ls_pin() == '':
					bot.send_message(chat_id=update.message.chat_id, text='No devices added/present')
				else:
					bot.send_message(chat_id=update.message.chat_id, text=selected_room.ls_pin())
			else:
				bot.send_message(chat_id=update.message.chat_id, text='Wrong input or argument count')

	
########	Error
def error(bot, update, error):
	logging.warn('Update:"%s" caused Error:"%s"'%(update, error))


