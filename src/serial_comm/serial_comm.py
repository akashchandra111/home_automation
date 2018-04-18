#########################################################################
#									#
#	Written By: Akash Chandra					#
#									#
#########################################################################

'''
	This file is responsible for the communication between arduino and the linux computer (RPi)
	the data is sent over bluetooth from raspberry to arduino
'''

from bluetooth import *

class Bserial:
	def __init__(self, hw_addr, port=1):
		self.socket = BluetoothSocket(RFCOMM)
		self.socket.connect((hw_addr, port))

	def send(self, data):
		self.socket.send(data)

	def kill(self):
		self.socket.close()
