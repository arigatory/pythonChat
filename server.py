import time
from datetime import datetime

from flask import Flask, request, abort

app = Flask(__name__)
db = [
    {
        'text': 'Привет',
        'time': time.time(),
        'name': 'Nick'
    },
    {
        'text': 'Привет, Nick',
        'time': time.time()+1,
        'name': 'Jane'
    }
]
users = []


@app.route("/")
def hello():
    return "Hello Ivan"


@app.route("/status")
def status():
    return {
        'status': True,
        'name': 'Skillbox messenger',
        'time': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        'total_messages': len(db),
        'total_users': len(users)
    }


@app.route("/send", methods=['POST'])
def send_message():
    if not isinstance(request.json, dict):
        return abort(400)

    name = request.json.get('name')
    text = request.json.get('text')
    if not isinstance(name, str) or not isinstance(text, str):
        return abort(400)
    if name == '' or text == '':
        return abort(400)
    message = {
        'text': text,
        'time': time.time(),
        'name': name
    }
    if text == '/connect':
        users.append(name)
    elif text == '/disconnect':
        users.remove(name)
    elif '/calc' in text:
        text = text.replace('/calc', '')
        try:
            result = eval(text)
            message['text'] = str(result)
            message['name'] = f'Выражение "{text}" вычислено для пользователя {name}'
            db.append(message)
        except Exception as e:
            print(e)
            message['text'] = 'Правильный формат, например, "/calc 3 + 5"'
            message['name'] = 'bot'
            db.append(message)
    else:
        db.append(message)
    return {'ok': True}


@app.route("/messages")
def get_messages():
    try:
        after = float(request.args['after'])
    except:
        return abort(400)

    res = []
    for message in db:
        if message['time'] > after:
            res.append(message)
    return {'messages': res[:100]}


app.run()
