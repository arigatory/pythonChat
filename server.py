import time
from datetime import datetime

from flask import Flask, request, abort
import random
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

not_sleep_advice = {
    'сделайте перерыв': 'Если вы клюёте носом на рабочем месте, встаньте и прогуляйтесь, например, до буфета. Не обязательно покупать булочку или полноценный обед, просто развейтесь.\nСкука часто приводит к сонливости. Не зря мы зеваем с назойливым собеседником и засыпаем во время унылого фильма. Поэтому разбавляем монотонную работу небольшими перерывами.',
    'съешьте яблоко': 'Взбодриться поможет и правильный перекус. Идеально подойдут:\nяблоки;\nшпинат;\nсложные углеводы (овсяная или гречневая каша, зелёная фасоль, кабачки);\nгорький шоколад;\nимбирь.\nВ борьбе с сонливостью специалисты также рекомендуют избегать перееданий и полностью исключить из рациона жирную пищу.',
    'вздремните': 'Дневной сон повышает работоспособность. Исследование Джорджтаунского университета показало: пока мы дремлем, левое полушарие мозга, отвечающее за память и логическое мышление, менее активно, то есть оно восстанавливается. Поэтому после дневного отдыха мы становимся активнее и легче усваиваем информацию. Дневной сон должен быть коротким. Специалисты считают: чтобы восстановиться, достаточно вздремнуть 15–20 минут. А если перед этим выпить чашку кофе, результат будет ещё лучше.',
    'включите свет': 'Повышенная сонливость обычно приходит вместе с сокращением светового дня. Солнечный свет, попадая на сетчатку, регулирует выработку мелатонина, то есть, по сути, выставляет наши биологические часы.\nПоэтому, чтобы взбодриться, откройте жалюзи или шторы. А если за окном темно, включите свет. Чем ярче, тем лучше.',
    'откройте окно': 'Мгновенно взбодриться поможет свежий воздух. Просто откройте окна и проветрите помещение. Нехватка кислорода — одна из причин сонливости. Если есть время и возможность, смело отправляйтесь на небольшую прогулку.',
    'умойтесь холодной водой': 'Снять усталость поможет и умывание холодной водой. Это стресс для организма, так что на некоторое время вы обретёте бодрость.',
    'выпейте чашечку кофе': 'Сотрудники Кардиффского университета доказали, что кофеин действительно повышает уровень активности человека.',
}


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
    elif '/sleep' in text:
            message['name'] = 'bot'
            key = random.choice(list(not_sleep_advice.keys()))
            description = not_sleep_advice[key]
            message['text'] = f'Чтобы не спать {key}\n\n ОПИСАНИЕ:\n{description}'
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
