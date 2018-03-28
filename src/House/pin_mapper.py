def pin_mapper(house_obj):
	pin_dict = dict()
	for i in house_obj.room:
		if i == None:
			return 'No room exists'
		else:
			for j in i.device:
				if j == None:
					return 'No devices exist'
				else:
					pin_dict[j.pin] = j.level
	return pin_dict
