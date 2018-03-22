#! /usr/bin/python
from os import getcwd
from sys import path

path.append(getcwd()+'/House')
from house import House		# Contains house framework
import house_loader as hl		# Contains backUpper and loader for house framework

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

def web_interface():
	webui = Flask(__name__)
	bootstrap = Bootstrap(webui)

	@webui.route('/')
	def index():
		return render_template('index.html', room_list=room_list())

	@webui.route('/room/<room_name>', methods=['GET', 'POST'])
	def room_name(room_name):
		global h
		if request.method == 'POST':
			dev_to_ctrl = request.form['status'].split(' ')
			if dev_to_ctrl[0] == 'On':
				for i in h.room:
					if room_name.encode('ascii') == i.name:
						for j in i.device:
							if dev_to_ctrl[1] == j.name:
								j.level = 100 
								break

				return render_template('room.html', room_name=room_name, dev_list=dev_list(room_name), status='Device is turned On!')
			elif dev_to_ctrl[0] == 'Off':
				for i in h.room:
					if room_name.encode('ascii') == i.name:
						for j in i.device:
							if dev_to_ctrl[1] == j.name:
								j.level = 0
								break

				return render_template('room.html', room_name=room_name, dev_list=dev_list(room_name), status='Device is turned Off!')
		else:
			return render_template('room.html', room_name=room_name, dev_list=dev_list(room_name), status='')	
	
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
		global h
		method_type = method_type.encode('ascii')
		if request.method == 'POST':
			if 'add_room' == method_type:
				return render_template('msg.html', msg=h.add_room(request.form['room_name']))
			elif 'rem_room' == method_type:
				return render_template('msg.html', msg=h.rem_room(request.form['room_name']))
			elif 'add_dev' == method_type:
				return render_template('msg.html', msg='')
			elif 'rem_dev' == method_type:
				return render_template('msg.html', msg='')
			elif 'load' == method_type:	# There is one problem, a file if not saved before and asked to load is unhandled in this function, might be implemented later.
				filename = request.form['load']
				h = hl.house_load('r', h, filename)
				return render_template('msg.html', msg='BackUp loaded!')
			elif 'backup' == method_type:
				filename = request.form['backup']
				hl.house_load('w', h, filename)
				return render_template('msg.html', msg='BackUp done!')
			else:
				return 'Problem Occured!'
		else:
			return render_template('index.html')

	webui.run(debug=True, host='localhost', port=8080)


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

if __name__ == '__main__':
	h = House()
	h = hl.house_load('r', h)

	web_interface()
