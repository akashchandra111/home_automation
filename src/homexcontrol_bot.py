#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   THE SERVER BOT FOR CONTROLLING THE HOME APPLIANCES USING TELEGRAM OPEN SOURCE MESSENGER

#   COPYRIGHT: AKASH CHANDRA 2017

##################################################################################
##
##  Importing Section
##################################################################################
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

import logging

##################################################################################

#   Enable the logger
logging.basicConfig(format='%s(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

##################################################################################
##
##   This is the section to add all the static string pieces that this bot uses
##################################################################################

start_text="""
    Control your home with the help of this bot using any microcontroller like RaspberryPi.Simply make this bot a part of your group as a member,and give the commands or chat to it individually.
"""

help_text="""
    Help Section:
        /info-all: Get the overall information
        /select: Select a particular room
        /on: ON selected room device/s
        /off: OFF selected room device/s
        /info: Get info of the selected room
        /command: Give commands that are in development phase
"""


##################################################################################

##################################################################################
##
##  This section is for all the variables
##################################################################################

room_list = list()
device_list = dict()

selected_room = 0
selected_device = ''

queryhandlerresult = ''

addordel_button = [
    [InlineKeyboardButton("Add", callback_data='add')],
    [InlineKeyboardButton("Delete", callback_data='del')]
]

roomordev_button = [
     [InlineKeyboardButton("Room", callback_data='room')],
     [InlineKeyboardButton("Device", callback_data='device')]
]

##################################################################################

##################################################################################
##
##  This section is for function definition
##################################################################################

#   /start
def start(bot, update):
    update.message.reply_text(start_text)

#   /help
def help(bot, update):
    update.message.reply_text(help_text)

#   /roomordevice
def roomordev(bot, update):
    roomordev_reply_markup = InlineKeyboardMarkup(roomordev_button)
    update.message.reply_text("Choose Room/Device:", reply_markup=roomordev_reply_markup)

#   addordel
def addordel(bot, update):
    addordel_reply_markup = InlineKeyboardMarkup(addordel_button)
    if queryhandlerresult=="room":
        update.message.reply_text("Add/Delete Room/s:", reply_markup=addordel_reply_markup)
    elif queryhandlerresult=="device":
        update.message.reply_text("Add/Delete Device/s:", reply_markup=addordel_reply_markup)
    else:
        update.message.reply_text("Invalid Option! Try once again..")
        


#   /select
def select(bot, update, args):
    update.message.reply_text('Under Construction')
    #Under Construction


#   /info-all
def info_all(bot, update):
    update.message.reply_text('Under Construction')
    #Under Construction

#   /on
def on(bot, update):
    update.message.reply_text('Under Construction')
    #Under Construction

#   /off
def off(bot, update):
    update.message.reply_text('Under Construction')
    #Under Construction

#   /set_message
def set_message(bot, update):
    update.message.reply_text('Under Construction')
    #Under Construction

#   /schedule
def schedule(bot, update):
    update.message.reply_text('Under Construction')
    #Under Construction

#   /set_last_locn
def set_last_locn(bot, update):
    update.message.reply_text('Under Construction')
    #Under Construction

#   /extra
def command(bot, update):
    update.message.reply_text('Under Construction')
    #Under Construction

#   /info
def info(bot, update):
    update.message.reply_text('Under Construction')
    #Under Construction

#   Error
def error(bot, update, error):
    logger.warn('Update:"%s" caused Error:"%s"'%(update, error))

#   Button
def querydatahandler(bot, update):
    query = update.callback_query
    queryhandlerresult = query.data
    bot.edit_message_text(text="Choosed: %s" % query.data, chat_id=query.message.chat_id, message_id=query.message.message_id)
#    return query.data

##################################################################################

##################################################################################
##
##  Main Function
##################################################################################

def main():
    #   Enter your BOT token here.
    updater = Updater("Insert Token Here")
    
    #   Dispatcher
    dp = updater.dispatcher

    #   Commands-Answers in telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add_del", roomordev))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("info_all", info_all))
    dp.add_handler(CommandHandler("select", select))
    dp.add_handler(CommandHandler("on", on))
    dp.add_handler(CommandHandler("off", off))
    dp.add_handler(CommandHandler("set_message", set_message))
    dp.add_handler(CommandHandler("set_last_locn", set_last_locn))
    dp.add_handler(CommandHandler("schedule", schedule))
    dp.add_handler(CommandHandler("command", command))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CallbackQueryHandler(querydatahandler))

    #   Log errors
    dp.add_error_handler(error)

    #   Start Bot
    updater.start_polling()

    #   Run the bot until someone force stop it using ^C or any killing commands.
    updater.idle()

##################################################################################

##################################################################################
##
##  Starting Point
##################################################################################
if __name__ ==  '__main__':
    main()

#                               END
##################################################################################

