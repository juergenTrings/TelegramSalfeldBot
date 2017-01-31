#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import datetime
from datetime import timedelta
from requests_toolbelt.utils import dump


payload = {
           'language': 'de_DE',
           'username': '',#your username
           'password': ''}#yor password
User = 'Friedrich'


def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False


def posttosalfeld(url, data, withuser=True, debug=True):
    with requests.Session() as s:
        l = s.post('https://portal.salfeld.net/api/login/', json=payload)
        json = l.json()
        auth = {
            'X-sessionId': json['sessionID'],
            'X-pcId': json['pcId']
        }
        if withuser:
            response = s.post('https://portal.salfeld.net/api/{}/{}'.format(User, url), json=data, headers=auth)
        else:
            response = s.post('https://portal.salfeld.net/api/{}'.format(url), json=data, headers=auth)
        if debug:
            data = dump.dump_all(response)
            print(data.decode('utf-8'))
        return response.json()


def gettosalfeld(url, withuser=True, debug=True):
    with requests.Session() as s:
        l = s.post('https://portal.salfeld.net/api/login/', json=payload)
        json = l.json()
        auth = {
            'X-sessionId': json['sessionID'],
            'X-pcId': json['pcId']
        }
        if withuser:
            response = s.get('https://portal.salfeld.net/api/{}/{}'.format(User, url), headers=auth)
        else:
            response = s.get('https://portal.salfeld.net/api/{}'.format(url), headers=auth)
        if debug:
            data = dump.dump_all(response)
            print(data.decode('utf-8'))
        return response.json()


def extension(zeit):
    ext = {'msg': zeit}
    data = posttosalfeld('ccsettings/setextension', ext)
    if data == "SUCCESS":
        return True
    else:
        return False


def status():
    extensions = gettosalfeld('ccsettings/extension')
    isonline = gettosalfeld('sse/isonline', False)
    data = [extensions['extension'], isonline['success']]
    return data


def sendmessage(text):
    check = status()
    if not check[1]:
        return "Nicht möglich weil der PC nicht an ist :("
    else:
        msg = {'msg': text}
        json = posttosalfeld('sse/sendmsg', msg, False)
        if json['success']:
            return "Erledigt!"
        else:
            return "Irgend etwas doofes ist passiert! Vieleicht ist niemand Angemeldet..."


def stats(option):
    if option == 2:
        today = datetime.date.today()
        last_monday = today - datetime.timedelta(days=today.weekday())
    elif option == 1:
        today = datetime.date.today()
        last_monday = today - timedelta(1)
        today = last_monday
    else:
        today = datetime.date.today()
        last_monday = today
    response = gettosalfeld('ccusage/bydatesall/{}/{}/15'.format(last_monday, today))
    if not response['logs']:
        return 0
    else:
        return response['logs'][0]['Period']


def shutdown():
    check = gettosalfeld('sse/shutdown', False)
    return check['success']


def lockpc(datum):
    if validate(datum):
        sperre = {"lockDate": datum, "OneTimeLockLevel": 3}
        response = posttosalfeld('ccsettings', sperre)
        if response['message'] == "SUCCESS":
            return 1
        else:
            return 2

    else:
        return 0
