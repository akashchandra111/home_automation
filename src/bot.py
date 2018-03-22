#! /usr/bin/python

#	Import
################################################	Common
import threading 

from os import getcwd
from sys import path
path.append(getcwd()+'/House')
path.append(getcwd()+'/Text')
from house import House		# Contains house framework
import house_loader as hl		# Contains backUpper and loader for house framework

################################################	Telegram
import text			# Contains Text
import logging				# Used to log for errors

import telegram				# Telegram API library
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

################################################	Web Interface
from flask import Flask
from flask import render_template
from flask import request
from flask_bootstrap import Bootstrap

########################################################################################################	Telegram Bot
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
		bot.send_message(chat_id=update.message.chat_id, text=h.add_room(data[1]))
	elif data[0] == 'rem_room' or data[0] == 'rr' and len(data) == 2:
		bot.send_message(chat_id=update.message.chat_id, text=h.rem_room(data[1]))
	elif data[0] == 'ls_room' or data[0] == 'lr' and len(data) == 1:
		if h.ls_room == '':
			bot.send_message(chat_id=update.message.chat_id, text='No rooms added/present')
		else:
			bot.send_message(chat_id=update.message.chat_id, text=h.ls_room())
	elif data[0] == 'select' or data[0] == 's' and len(data) == 2:
		for i in h.room:
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
			hl.house_load('w', h, data[1])
			bot.send_message(chat_id=update.message.chat_id, text='Settings saved')
		elif len(data) == 1:
			hl.house_load('w', h)
			bot.send_message(chat_id=update.message.chat_id, text='Settings saved')			
		else:
			bot.send_message(chat_id=update.message.chat_id, text='Wrong number of arguments given')
	elif data[0] == 'load_settings' or data[0] == 'ls':
		if len(data) == 2:
			h = hl.house_load('r', h, data[1])
			bot.send_message(chat_id=update.message.chat_id, text='Settings loaded')
		elif len(data) == 1:
			h = hl.house_load('r', h)
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
						bot.send_message(chat_id=update.message.chat_id, text=i.name+' is off')
					else:
						counter += 1
					if counter == len(selected_room.device):
						bot.send_message(chat_id=update.message.chat_id, text='No such device exists')
			elif data[0] == 'sel_lev' or data[0] == 'sl' and len(data) == 3:
				counter = 0
				for i in selected_room.device:
					if i.name == data[1]:
						i.set_level(int(data[2]))
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

########################################################################################################	Telegram Bot

########################################################################################################	Web Interface

def web_interface():
	webui = Flask(__name__)
	bootstrap = Bootstrap(webui)

	@webui.route('/')
	def index():
		return render_template('index.html', room_list=room_list())

	@webui.route('/room/<room_name>')
	def room_name(room_name):
		return render_template('room.html', room_name=room_name, dev_list=dev_list(room_name))	
	
	@webui.route('/add_room')
	def add_room():
		return render_template('add_room.html')
		
	@webui.route('/rem_room')
	def rem_room():
		return render_template('rem_room.html', room_list=room_list())
	
	@webui.route('/load_backup')
	def load_backup():
		return render_template('load_backup.html')
	
	@webui.route('/add_dev')
	def add_dev():
		return render_template('add_dev.html')
	
	@webui.route('/rem_dev')
	def rem_dev():
		return render_template('rem_dev.html', dev_list=dev_list())
	
	@webui.route('/msg/<method_type>', methods=['GET', 'POST'])
	def msg(method_type):
		method_type = method_type.encode('ascii')
		if request.method == 'POST':
			if 'add_room' == method_type:
				return render_template('msg.html', msg=h.add_room(request.form['room_name']))
			elif 'rem_room' == method_type:
				return render_template('msg.html', msg=h.rem_room(request.form['room_name']))
			elif 'add_dev' == method_type:
				return render_template('msg.html')
			elif 'rem_dev' == method_type:
				return render_template('msg.html')
			elif 'load' == method_type:
				return render_template('msg.html', msg=hl.house_load('w', request.form['load']))
			elif 'backup' == method_type:
				return render_template('msg.html', msg=hl.house_load('r', request.form['backup']))
			else:
				return 'Problem Occured!'
		else:
			return render_template('index.html')

	webui.run(debug=True, use_reloader=False, host='localhost', port=8080)


def room_list():
	room_list = list()
	for i in h.room:
		room_list.append(i.name)
	return room_list

def dev_list(room_name):
	dev_list = list()
	for i in h.room:
		if i.name == room_name:
			for j in i.device:
				dev_list.append(j.name)
	return dev_list

########################################################################################################	Web Interface

if __name__ == '__main__':
	# Defining the house object
	h = House()
	h = hl.house_load('r', h)

	# Defining 2 seperate processes for bot and web
	bot = threading.Thread(target=bot, args=())
	web_interface = threading.Thread(target=web_interface, args=())

	# Starting the processes individually
	bot.start()
	web_interface.start()

	# Join after work is complete, however not going to occur ever
	bot.join()
	web_interface.join()
