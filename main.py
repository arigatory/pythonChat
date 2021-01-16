import time

from flask import request

db = [
    {
        'text': 'Привет',
        'time': time.time(),
        'name': 'Nick'
    },
    {
        'text': 'Привет, Nick',
        'time': time.time(),
        'name': 'Jane'
    }
]


def print_message(message):
    print(message['time'], message['name'])
    print(message['text'])
    print()


def print_messages(db):
    for message in db:
        print_message(message)


def send_message(name, text):
    message = {
        'text': text,
        'time': time.time(),
        'name': name
    }
    db.append(message)


def get_messages(after):
    res = []
    for message in db:
        if message['time'] > after:
            res.append(message)
    return res


send_message('Nick', 'Привет')

messages = get_messages(0)
print_messages(messages)

send_message('Nick', 'Привет2')

messages = get_messages(messages[-1]['time'])
print_messages(messages)

messages = get_messages(messages[-1]['time'])
print_messages(messages)

