from flask import request

def login():
    try:
        params = {'username': request.json.get('username'),
                  'password': request.json.get('password')}
        if params['username'] == 'operador':
            return