import os, time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Chat, ParseMode
from requests import post, get, delete
import prettytable as pt
import logging
import random as r
import time
from math import sqrt, gcd, log
from itertools import count, islice
from Classes.Database import *

def start(update, context):
    update.message.reply_text("Fala seu arrombado")

def register(update, context):
    global db
    user_id = str(update.message.from_user.id)
    existent_id = db.get('cod_usuario', 'usuario', 'cod_usuario = ' + user_id)
    text = ''
    if existent_id != []:
        text = 'Usuario ja registrado'
    else:
        user_name = update.message.from_user.first_name
        db.insert('usuario', 'cod_usuario, nome_usuario, capsulas', user_id + ", '" + user_name + "', 0")
        text = 'Usuario cadastrado com sucesso'
    update.message.reply_text(text)

def incr_cafe(update, context):
    global db
    user_id = str(update.message.from_user.id)
    user = db.get('cod_usuario', 'usuario', 'cod_usuario = ' + user_id)
    if user == []:
        update.message.reply_text('Usuario nao encontrado, cadastrando usuario')
        register(update, context)
        user = db.get('cod_usuario', 'usuario', 'cod_usuario = ' + user_id)
    db.update('usuario', 'capsulas=capsulas-1', 'cod_usuario = ' + user_id)
    update.message.reply_text("Manera no cafe, " + update.message.from_user.first_name)

def comprei_cafe(update, context):
    split_message = update.message.text.split(' ')
    capsulas = 0
    try:
        capsulas = int(split_message[1])
    except:
        update.message.reply_text('Aprende a usar o comando filho da puta')
        return
    global db
    user_id = str(update.message.from_user.id)
    user = db.get('cod_usuario', 'usuario', 'cod_usuario = ' + user_id)
    if user == []:
        update.message.reply_text('Usuario nao encontrado, cadastrando usuario')
        register(update, context)
        user = db.get('cod_usuario', 'usuario', 'cod_usuario = ' + user_id)
    db.update('usuario', 'capsulas=capsulas+' + str(capsulas), 'cod_usuario = ' + user_id)
    text = "Yay, o rico " + update.message.from_user.first_name + " acabou de abastecer o estoque de cafe"
    update.message.reply_text(text)

def lista_cafe(update, context):
    global db
    table = pt.PrettyTable(['Capsulas', 'Consumidor'])
    table.align['Capsulas'] = 'c'
    table.align['Consumidor'] = 'c'
    rows = db.get('capsulas, nome_usuario', 'usuario', 'cod_usuario != 0')
    for (capsulas, nome_usuario) in sorted(rows):
        table.add_row([str(capsulas), nome_usuario])
    update.message.reply_text(f'<pre>{table}</pre>', parse_mode=ParseMode.HTML)

def get_status():
    global db
    status = db.get('status', 'sala')
    return status[0][0]

def user_exists(update):
    global db
    user_id = str(update.message.from_user.id)
    user = db.get('cod_usuario', 'usuario', 'cod_usuario = ' + user_id)
    return user != []

def status_sala(update, context):
    if not user_exists(update):
        update.message.reply_text('Voce nao esta registrado')
        return
    if get_status() == 0:
        update.message.reply_text('A sala esta fechada')
    else:
        update.message.reply_text('A sala esta aberta')

def abre_sala(update,context):
    if not user_exists(update):
        update.message.reply_text('Voce nao esta registrado')
        return
    if get_status() == 1:
        update.message.reply_text('A sala ja esta aberta, cara')
    else:
        db.update('sala', 'status=1')
        update.message.reply_text('A sala foi aberta')

def fecha_sala(update,context):
    if not user_exists(update):
        update.message.reply_text('Voce nao esta registrado')
        return
    if get_status() == 0:
        update.message.reply_text('A sala ja esta fechada, cara')
    else:
        db.update('sala', 'status=0')
        update.message.reply_text('A sala foi fechada')

def error(update, context):
    update.message.reply_text('Update "%s" caused error "%s"', update, error)

def main():
    TOKEN = os.environ["TELEGRAM_TOKEN"]

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("registrar", register))
    dispatcher.add_handler(CommandHandler("tomei_cafe", incr_cafe))
    dispatcher.add_handler(CommandHandler("comprei_cafe", comprei_cafe))
    dispatcher.add_handler(CommandHandler("saldo_do_cafe", lista_cafe))
    # dispatcher.add_handler(CommandHandler("key_blame", comprei_cafe))
    # dispatcher.add_handler(CommandHandler("cade_a_chave", loc_chave))
    dispatcher.add_handler(CommandHandler("status_sala", status_sala))
    dispatcher.add_handler(CommandHandler("abri_a_sala", abre_sala))
    dispatcher.add_handler(CommandHandler("fechei_a_sala", fecha_sala))
    
    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    global db
    db = Database()
    main()
