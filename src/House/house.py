#########################################################################
#									#
#	Written By: Akash Chandra					#
#									#
#########################################################################

'''
	Framework representing the structure of a house
	* Can be used to add/remove a room
	* Can be used to add/remove a device present in room
'''

# Every Room has a device and this class represents a single device
# The device can have on/off or levelled state
# It's all defined in this class
# don't import this function

class Device:
	def __init__(self, name, pin):
		self.name = name
		self.pin = pin
		self.level = 0

	def set_level(self, level):
		if self.level < 0:
			self.level = 0
		elif self.level > 100:
			self.level = 100
		else:
			self.level = level

	def on(self):
		self.level = 100	
	
	def off(self):
		self.level = 0
	

# Every House is composed of rooms present in them
# This class defines all the room behaviour and contains appliances array present in them
# We can add/remove devices present in a room
# don't import this function

class Room:
	def __init__(self, name):
		self.name = name
		self.device = list()
	
	def add_dev(self, name, pin):
		for i, j in enumerate(self.device):
			if j.name == name:
				return '{0} is already present'.format(name)
			if j.pin == pin:
				return '{0} is already present'.format(pin)

		self.device.append(Device(name, pin))
		return '{0} is added'.format(name)

	def rem_dev(self, name):
		for i, j in enumerate(self.device):
			if j.name == name:
				self.device.pop(i)
				return '{0} is removed'.format(name)

		return '{0} is not present'.format(name)

	def ls_dev(self):
		item = ''
		for i, j in enumerate(self.device):
			item += '{0}: {1}\n'.format(i+1, j.name)

		return item
	
	def ls_pin(self):
		item = ''
		for i in self.device:
			item += 'Pin {0}: Device {1}\n'.format(str(i.pin), i.name)

		return item



# Framework for a house
# A house has several rooms and these rooms have devices
# Use this function to import
# This function will be improved in the later version but for the testing sake it's now it what it is

class House:
	def __init__(self):
		self.room = list()
	
	def add_room(self, name):
		for i, j in enumerate(self.room):
			if j.name == name:
				return '{0} room already present'.format(name)

		self.room.append(Room(name))
		return '{0} room added'.format(name)
	
	def rem_room(self, name):
		for i, j in enumerate(self.room):
			if j.name == name:
				self.room.pop(i)
				return '{0} room is removed'.format(name)

		return '{0} room not present'.format(name)

	def ls_room(self):
		item = ''
		item_name = ''
		for i, j in enumerate(self.room):
			item_name = j.name
			item += '{0}: {1}\n'.format(i+1, j.name)

		return item
