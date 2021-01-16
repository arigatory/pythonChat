import requests
import atexit

name = input('Введите имя: ')

requests.post('http://127.0.0.1:5000/send',
              json={'name': name, 'text': '/connect'}
              )


def exit_hadler(pers):
    requests.post('http://127.0.0.1:5000/send',
                  json={'name': name, 'text': '/disconnect'}
                  )


atexit.register(exit_hadler, name)
while True:
    text = input('Введите текст: ')
    requests.post('http://127.0.0.1:5000/send',
                  json={'name': name, 'text': text}
                  )
