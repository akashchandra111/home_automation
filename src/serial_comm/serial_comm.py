import serial

class Communicator:
	def __init__(self, dev, baud_rate):
		self.serial = serial.Serial(dev, baudrate)
	
	def send(self, data):
		self.serial.write(data)
