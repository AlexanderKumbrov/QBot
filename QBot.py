import datetime
import asyncio
import time
import telegram.ext
import mysql.connector
import pymysql.cursors
from datetime import timedelta
from telegram.ext import Updater , Job
from aiohttp import web
from aiogram import Bot , types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling

bot = Bot('API_TOKEN')
dBot = Dispatcher(bot)

db = pymysql.connect("NAMESERV" , "USER" , "PASS" , "NAMEDB")
cursor = db.cursor()
sql = "SELECT*FROM NAMETABLE"

now = datetime.datetime.now
chats_id = [USERID  ]




@dBot.message_handler(commands=['start'])
async def startMessage(message: types.Message):
   await bot.send_message(message.chat.id , "Hi!")


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
   
@dBot.message_handler(commands=['verify'])
async def verifyMessage(message:types.message):
    await msg(False, message.chat.id )


async def handle(request):
    if request.method=="POST":
        text = "POSTOK "
        print("POST")
        return web.Response(text=text)
    elif request.method=="GET":
        text= "OK"
    await msg(True)
    return web.Response(text=text)

def printmsg():
    print("message ")
    
     
async def msg( ver,chat_id = 0):
    
    cursor.execute(sql)
    result = cursor.fetchall()
    yDate = datetime.date.today()
    fDate = yDate + timedelta(days=1)
    a = fDate.strftime("%d.%m")
    b = yDate.strftime("%d.%m")
    mess = ''
    for row in result:  
        # print(str(number))
            
        # print(b)
           
        if a in row[3]:
            if row[2]==0:
                mess = row[1] + "\n " + 'Номер отсутствует \n'+ row[3]
            else:
                mess = row[1] + "\n " + row[3] + "\n +996 " + str(row[2])
                    
            if ver ==True:
                for id in chats_id:
                    await bot.send_message(id, "MESSAGE : " + mess)
            else:
                await bot.send_message(chat_id, "MESSAGE : " + mess)
        if b in row[3]:
            if row[2]==0:
                mess = row[1] + "\n " + 'MESSAGE \n'+ row[3]
            else:
                mess = row[1] + "\n " + row[3] + "\n +996 " + str(row[2])
                    
            if ver ==True:
                for id in chats_id:
                    await bot.send_message(id, "MESSAGE : " + mess)
            else:
                await bot.send_message(chat_id, "MESSAGE : " + mess)
    
async def startServ():
    server = web.Server(handle)
    runner = web.ServerRunner(server)
    await runner.setup()
    site = web.TCPSite(runner , '0.0.0.0' , 8080)
    await site.start()
    print("STARTING SERVER")

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(startServ())
    loop.run_until_complete(start_polling(dBot , loop=loop , skip_updates=True))
except KeyboardInterrupt:
    pass
loop.close()

    


