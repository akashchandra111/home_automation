# This file intention is to load/backup the house in memory in case of failure/shutdown
# It is used to retain the structure
# It uses an instance of House() to work and copies/write the whole data from the 'filename' to/from the House() object

#########################################################################
#									#
#	Written By: Akash Chandra					#
#									#
#########################################################################

import json
from os import getcwd

def house_load(mode, house_obj, filename='home.bak'):
	json_data = ''

	if mode == 'w':
		room_data = dict()
		dev_data = list()
		pin_data = dict()

		file = open(getcwd()+'/House/'+filename, mode)
		
		for i in house_obj.room:
			for j in i.device:
				pin_data[j.name] = j.pin
				dev_data.append(pin_data)
				pin_data = dict()
			room_data[i.name] = dev_data
			dev_data = list()
			
		json_data = json.dumps(room_data)
		file.write(json_data)
		file.close()
		print('BackUp Done!')

	elif mode == 'r':
		file = open(getcwd()+'/House/'+filename, mode)
		json_data = json.loads(file.readline())
		
		counter1 = 0
		counter2 = 0
		
		for i in json_data:
			house_obj.add_room(i)
			for j in json_data[i]:
				for k in j:
					house_obj.room[counter1].add_dev(k, None)
					house_obj.room[counter1].device[counter2].pin = j[k]
				counter2 +=1
			counter1 += 1
			counter2 = 0

		file.close()
		print('BackUp Loaded!')
		return house_obj

	else:
		print('Wrong Input Passed!')
