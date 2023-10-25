from flask import request
from Global.Classes.Operador import Operador
from Global.Classes.Gerente import Gerente
from Global.Classes.Auth import Auth
from Global.Classes.Empleado import Empleado


def login():
    try:
        params = {'username': request.json.get('username'),
                  'password': request.json.get('password')}
        try:
            role = Auth.obtain_role(params['username'])
            if role == 'operador':
                usuario = Operador(params)
                return {'token': usuario.web_token, 'empresa': usuario.empresa_nombre, 'tipo': 'operador', 'nombre': usuario.nombre, 'message': 'Login exitoso'}, 200
            elif role == 'gerente':
                usuario = Gerente(params)
                return {'token': usuario.web_token, 'empresa': usuario.empresa_nombre, 'tipo': 'gerente', 'nombre': usuario.nombre, 'message': 'Login exitoso'}, 200

        except Exception as e:
            return {'error': str(e)}, 400
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

def aceptar_tyc():
    try:
        params = {'id': request.json.get('id')}
        aceptado = Empleado.aceptar_tyc(params)
        return {'msg': aceptado}, 200
    except Exception as e:
        return {'error': str(e)}, 400
