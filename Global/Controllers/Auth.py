from flask import request
from Global.Classes.Operador import Operador
from Global.Classes.Auth import Auth


def login():
    try:
        params = {'username': request.json.get('username'),
                  'password': request.json.get('password')}
        try:

            role = Auth.obtain_role(params['username'])
            if role == 'operador':
                usuario = Operador(params)
            elif role == 'gerente':
                pass

        except Exception as e:
            return {'error': str(e)}, 400
        return usuario.web_token, 200
    except Exception as e:
        return {'error': str(e)}, 400


def validate_session():
    try:
        headers = request.headers
        bearer = headers.get('Authorization')
        token = bearer.split()[1]
        return Auth.validar_token(token), 200
    except Exception as e:
        return {'error': str(e)}, 400
