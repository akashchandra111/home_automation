from bluetooth import *

class Bserial:
	def __init__(self, hw_addr, port=1):
		self.socket = BluetoothSocket(RFCOMM)
		self.socket.connect((hw_addr, port))

	def send(self, data):
		self.socket.send(data)

	def kill(self):
		self.socket.close()
