import datetime
import asyncio
import time
import telegram.ext
import mysql.connector
import logging
import json
import pymysql.cursors
from datetime import timedelta
from telegram.ext import Updater , Job
import aiohttp 
from aiohttp import web
from aiogram import Bot , types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling

bot = Bot('TOKEN')
dBot = Dispatcher(bot)

db = pymysql.connect("ADRESSBD" , "USER" , "PASSWORD" , "DB")
cursor = db.cursor()
sql = "SELECT*FROM table"

now = datetime.datetime.now
chats_id = [USERID  ]




@dBot.message_handler(commands=['start'])
async def startMessage(message: types.Message):
    await bot.send_message(message.chat.id , "Hello")

@dBot.message_handler(commands=['verify'])
async def verifyMessage(message: types.Message):
    await msg(False, message.chat.id )
    print(message.chat.id)



@dBot.message_handler(content_types=["text"])
async def message_handler(message: types.Message):
    msg = ''
    s = message.text
    if len(s)<4:
        
        await bot.send_message(message.chat.id , "Введите больше информации")
    else:
        
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            name = row[1]
            if s in name:
                if row[2]=='':
                    msg =  row[1]+'\n'+'Номер отсутствует!'
                else:
                    msg =  row[1]+'\n'+' +996'+str(row[2])
                await bot.send_message(message.chat.id , msg)


async def handle(request):
    if request.method=="POST":
        text = "POSTOK "
    
        jsonResult = await request.text()   
        
        js = json.loads(jsonResult)

        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            if row[1] == js["name"]:
                sqlinsert = "UPDATE `DB`.`table` SET `FirstName` = '"+js["phone"]+"', `date` = '"+js["bdate"]+"' WHERE name = '"+js["name"]+"' ;"
            else:
                sqlinsert= "INSERT INTO `DB`.`table` (`Name`, `FirstName`, `date`) VALUES ('"+js["name"]+"', '"+js["phone"]+"', '"+js["bdate"]+"');"
        cursor.execute(sqlinsert)
        db.commit()
        print("POST")
        return web.Response(text=text)
    elif request.method=="GET":
        text= "OK"
        await msg(True)
        return web.Response(text=text)

    
     
async def msg( ver,chat_id = 0):
    
    cursor.execute(sql)
    result = cursor.fetchall()
    yDate = datetime.date.today()
    fDate = yDate + timedelta(days=1)
    a = fDate.strftime("%d.%m")
    b = yDate.strftime("%d.%m")
    mess = ''                  
    for row in result:  
     
        if a in row[3]:
            if row[2]==0:
                mess = row[1] + "\n " + 'Номер отсутствует \n'+ row[3]
            else:
                mess = row[1] + "\n " + row[3] + "\n +996 " + str(row[2])
                    
            if ver ==True:
                for id in chats_id:
                    await bot.send_message(id, "Завтра день рождение : " + mess)
            else:
                await bot.send_message(chat_id, "Завтра день рождение : " + mess)
        if b in row[3]:
            if row[2]==0:
                mess = row[1] + "\n " + 'Номер отсутствует \n'+ row[3]
            else:
                mess = row[1] + "\n " + row[3] + "\n +996 " + str(row[2])
                    
            if ver ==True:
                for id in chats_id:
                    await bot.send_message(id, "Сегодня день рождение : " + mess)
            else:
                await bot.send_message(chat_id, "Сегодня день рождение : " + mess)
    
async def startServ():
    server = web.Server(handle)
    runner = web.ServerRunner(server)
    await runner.setup()
    site = web.TCPSite(runner , 'localhost' , 8080)
    await site.start()
    print("STARTING SERVER")

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(startServ())
    loop.run_until_complete(start_polling(dBot , loop=loop , skip_updates=True))
except KeyboardInterrupt:
    pass
loop.close()

