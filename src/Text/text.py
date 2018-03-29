start_text = '''
Telegram Bot to control home devices by giving commands
For more info see /help command
'''
help_text = '''
** Basic Commands **
/start: for starting with this bot
/help: to get this help text

# <>: Mandatory Arguments
# []: Optional Arguments

** Operational Commands **
add_room <Room Name>: To add a new room
rem_room <Room Name>: To remove a room
ls_room: To show all the current added rooms
select <Room Name>: To select a room for add/removing Device
cur_room: To show the currently selected room

-- These commands will work on room selection --
add_dev <Device Name> <Pin NO>: To add a device with specified pin
rem_dev: To remove a device
on <Device Name>: To switch on a device
off <Device Name>: To switch off a device
set_lev <Device Name> <value>: To set the device power level
ls_dev: To show all the devices present in room
ls_pin: To show the pin configuration of a selected room

** To save your settings **
save_settings [File Name]: To save your modified settings
load_settings [File Name]: To load your settings
'''

cheat_text = '''
ar:	add_room
rr:	rem_room
lr:	ls_room
s:	select
cr:	cur_room
ad:	add_dev
rd:	rem_dev
1:	on
0:	off
sl:	set_lev
ld:	ls_dev
lp:	ls_pin
ss:	save_settings
ls:	load_settings
'''
