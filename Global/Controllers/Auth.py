from flask import request
from Global.Classes.Operador import Operador
from Global.Classes.Auth import Auth

def login():
    try:
        params = {'username': request.json.get('username'),
                  'password': request.json.get('password'),
                  'tipo_usuario': request.json.get('tipo_usuario')}
        try:
            if params['tipo_usuario'] == 'operador':
                usuario = Operador(params)
                print('VVVVVVVVVVVVVVV')
            else:
                usuario = False
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