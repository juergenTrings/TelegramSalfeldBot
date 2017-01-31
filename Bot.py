#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from Salfeld import extension, status, stats, shutdown, sendmessage, lockpc, validate
from random import randint
import datetime

updater = Updater(token='')# Your token here
dispatcher = updater.dispatcher


def erfolg(bot, queryid):
    ant = ["Bin Fertig! Alles gut gelaufen.",
           "Ok work done!",
           "Jetzt habe Ich aber frei!",
           "Joap, das sollte es gewesen sein!",
           "alles gemacht!",
           "Fertig! Das macht 6,50€",
           "schon erledigt!",
           "rekordzeit! so schnell ging es noch nie!",
           "Alles nach deinem wunsch erledigt!"]
    bot.sendMessage(chat_id=queryid, text=ant[randint(0, len(ant)-1)])


def fehler(bot, queryid):
    ant = ["Irgendwas doofes ist gerade passiert!",
           "Ochh nee irgendwo ist ein Fehler aufgetreten!",
           "[*BIIEEP*] FEHLER, FEHLER, FEHLER [*BIIEEP*]",
           "Sorry aber die Elektronen sind gerade alle rausgefallen",
           "Hoppla da ging was schief",
           "da ging was schief oder haben wir wirklich das Jahr 1967 ???"]
    bot.sendMessage(chat_id=queryid, text=ant[randint(0, len(ant) - 1)])


def work(bot, queryid):
    ant = ["Bin dabei!",
           "wörk wörk wörk",
           "Ich sollte einer Gewerkschaft beitreten!",
           "Geht klar Chef!",
           "Wenn du das so willst!",
           "Ich wünschte ich könnte nein sagen!",
           "Warte kurz",
           "Du denkst aber auch das ich nichts anderes zu tun habe oder?",
           "OKII DOKI"]
    bot.sendMessage(chat_id=queryid, text=ant[randint(0, len(ant) - 1)])


def verung(bot, update, args):
    if args:
        try:
            zeit = int(args[0])
            work(bot, update.message.chat_id)
        except IndexError:
            zeit = False
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="Wie um alles in der Welt soll ich denn eine Verlängerung von Buchstaben setzten?")
    else:
        zeit = False
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Was soll den dieser Mist? soll Ich jetzt raten wie lange ich machen soll?")

    if zeit:
        print(zeit)
        check = extension(zeit)
        if check:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="Sehr gut {} Minuten Verlängerung wurden gesetzt!".format(zeit))
        else:
            fehler(bot, update.message.chat_id)


def statuscall(bot, update):
    work(bot, update.message.chat_id)
    data = status()
    if data[1]:
        computer = "eingeschalten"
    else:
        computer = "nicht eingeschalten"
    if data[0] == 0:
        verlangerung = "es ist keine Verlängerung gesetzt"
    else:
        verlangerung = "es ist eine Verlängerung von {} Minuten gesetzt".format(data[0])
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Ok. der Computer ist {} und {}".format(computer, verlangerung))


def statistik(bot, update):
    keyboard = [[InlineKeyboardButton("Heute", callback_data='0'),
                 InlineKeyboardButton("Gestern", callback_data='1')],

                [InlineKeyboardButton("Diese Woche", callback_data='2')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Joap, von wann willst du die Statisitken haben?', reply_markup=reply_markup)


def button(bot, update):
    opt = {0: 'Heute', 1: 'Gestern', 2: 'Diese Woche'}
    query = update.callback_query
    nr = int(query.data)
    bot.editMessageText(text=query.message.text, chat_id=query.message.chat_id, message_id=query.message.message_id)
    if nr <= 2:
        zeit = stats(nr)
        bot.sendMessage(text="{} war der Computer {} Stunden an".format(opt[nr], zeit), chat_id=query.message.chat_id)
    elif nr == 3 or nr == 4:
        if nr == 3:
            work(bot, query.message.chat_id)
            check = shutdown()
            if check:
                erfolg(bot, query.message.chat_id)
            else:
                fehler(bot, query.message.chat_id)
        else:
            bot.sendMessage(text="dann eben nicht!", chat_id=query.message.chat_id)
    elif 5 <= nr <= 7:
        if nr < 7:
            work(bot, query.message.chat_id)
            if nr == 5:
                now = datetime.datetime.now() + datetime.timedelta(days=1)
            else:
                now = datetime.date.today() + datetime.timedelta(weeks=1)
            success = lockpc(now.strftime('%Y-%m-%d %H:%M:%S'))
            if success:
                erfolg(bot, query.message.chat_id)

            else:
                fehler(bot, query.message.chat_id)
        else:
            bot.editMessageText(chat_id=query.message.chat_id, message_id=query.message.message_id,
                                text="Gut dann machen wir das so!\n"
                                     "Gib mir bitte ein Datum nach diesem Schema:\n"
                                     "/sperren JJ-MM-TT HH:MM:SS\n"
                                     "Beispiel: /sperren 2016-12-24 12:34:00")

    elif nr == 8:
        bot.sendMessage(text="dann eben nicht!", chat_id=query.message.chat_id)


def delverung(bot, update):
    work(bot, update.message.chat_id)
    verlangerung(0)
    erfolg(bot, update.message.chat_id)


def hilfe(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Alle Befehle:\n/verung - Verlängerung setzten\n"
                         "/status - zeigt pc status und alle Verlängerungen\n"
                         "/statistik - zeigt wie lange der PC benutz wurde\n"
                         "/delverung - löscht alle Verlängerungen\n"
                         "/shutdown - Computer Herunterfahren\n"
                         "/msg - Sendet eine Nachricht an den PC\n"
                         "/sperren - sperrt den Computer für eine def. Zeit\n"
                         "/delsperren - löscht alle Sperrungen")


def runter(bot, update):
    check = status()
    if check[1]:
        keyboard = [[InlineKeyboardButton("Ja", callback_data='3'),
                    InlineKeyboardButton("Neej", callback_data='4')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Bist du dir sicher?', reply_markup=reply_markup)
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Geht nicht weil der Computer nicht an ist!")


def msg(bot, update, args):
    work(bot, update.message.chat_id)
    response = sendmessage(args[0])
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=response)


def sperr(bot, update, args):
    if args:
        date = args[0]+args[1]
        if validate(date):
            work(bot, update.message.chat_id)
            if lockpc(date) == 1:
                erfolg(bot, update.message.chat_id)
            else:
                fehler(bot, update.message.chat_id)
        else:
            fehler(bot, update.message.chat_id)
            bot.sendMessage(chat_id=update.message.chat_id, text="Irgendwie kann dein Datum nicht stimmen!\n"
                                                                 "Es entspricht meiner meinung nach nicht diesem Muster:\n"
                                                                 "JJ-MM-TT HH:MM:SS")
    else:
        keyboard = [[InlineKeyboardButton("Morgen", callback_data='5'),
                     InlineKeyboardButton("Diese Woche", callback_data='6')],
                    [InlineKeyboardButton("Eigenes Datum", callback_data='7')],
                    [InlineKeyboardButton("Ich will doch nicht!", callback_data='8')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Bis wann soll ich den Computer Sperren ?', reply_markup=reply_markup)


def delsperr(bot,update):
    work(bot, update.message.chat_id)
    now = datetime.datetime.now()
    check = lockpc(now.strftime('%Y-%m-%d %H:%M:%S'))
    if check == 1:
        erfolg(bot, update.message.chat_id)
    else:
        fehler(bot, update.message.chat_id)

Verung_handler = CommandHandler('verung', verung, pass_args=True)
dispatcher.add_handler(Verung_handler)
Status_handler = CommandHandler('status', statuscall)
dispatcher.add_handler(Status_handler)
Statistik_handler = CommandHandler('statistik', statistik)
dispatcher.add_handler(Statistik_handler)
dispatcher.add_handler(CallbackQueryHandler(button))
delverung_handler = CommandHandler('delverung', delverung)
dispatcher.add_handler(delverung_handler)
help_handler = CommandHandler('help', hilfe)
dispatcher.add_handler(help_handler)
msg_handler = CommandHandler('msg', msg, pass_args=True)
dispatcher.add_handler(msg_handler)
Shutdown_handler = CommandHandler('shutdown', runter)
dispatcher.add_handler(Shutdown_handler)
sperren_handler = CommandHandler('sperren', sperr, pass_args=True)
dispatcher.add_handler(sperren_handler)
delsperren_handler = CommandHandler('delsperren', delsperr)
dispatcher.add_handler(delsperren_handler)

updater.start_polling()
