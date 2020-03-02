#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import telebot
import datetime
from datetime import timedelta
from threading import Thread
import time
import schedule
import telegram.ext
from telegram.ext import Updater, Job
 

bot = telebot.TeleBot('TOKEN')

now = datetime.datetime.now
chats_id = [chats_id]


@bot.message_handler(commands=['start'])
def startMessage(message):
    bot.send_message(message.chat.id , "Hi!")

@bot.message_handler(commands=['verify'])

def verify_messages(message):
    msg(False ,message.chat.id )

@bot.message_handler(content_types=["text"])
def message_handler(message):
    msg = ''
    s = message.text
    if len(s)<4:
        
        bot.send_message(message.chat.id , "Введите больше информации")
    else:
        fileHandle = open(r'', 'r' ,encoding="utf-8")
        for line in fileHandle:
            fields = line.split('|')
            if s in fields[0]:
                if fields[1]=='':
                    msg =  fields[0]+'\n'+'Номер отсутствует!'
                else:
                    msg =  fields[0]+'\n'+' +996'+fields[1]
                bot.send_message(message.chat.id , msg)

        fileHandle.close()
        if msg == '':
            msg = 'Не найдено !'
            bot.send_message(message.chat.id , msg)


def msg(shed , chat_id = 0):
    
    date = datetime.date.today()
    fDate = date + timedelta(days=1)
    mess = ''
    a = fDate.strftime("%d.%m")
    fileHandler = open(r'', 'r' ,encoding="utf-8")
    for line in fileHandler:
        fields = line.split("|")
        if a in fields[2]:
            if fields[1]=='':
                mess = fields[0] + "\n " + fields[2] + '\n Отсутствует номер'
            else:
                mess = fields[0] + "\n " + fields[2] + "\n +996 " + fields[1]
            if shed ==True:
                for id in chats_id:
                    print(id)
                    bot.send_message(id, "Завтра день рождение : " + mess)
            else:
                bot.send_message(chat_id, "Завтра день рождение : " + mess)
    fileHandler.close()



def execute_me():
    schedule.every().day.at("10:00").do(msg , True)
    while True:
        schedule.run_pending()
        time.sleep(0)

thread1 = Thread(target=execute_me)
thread1.start()

bot.polling(none_stop=True, interval=0)