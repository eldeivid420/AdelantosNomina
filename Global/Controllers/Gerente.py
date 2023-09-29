from flask import request
from Global.Classes.Gerente import Gerente

def create_gerente():
    try:
        params = {'username': request.json.get('username'),
                  'nombre': request.json.get('nombre'),
                  'password': request.json.get('password')}
        gerente = Gerente(params, False)
        return f'El gerente: {gerente.nombre} se registró correctamente con el id: {gerente.id}', 200
    except Exception as e:
        return {'error': str(e)}, 400


def obtener_bancos():
    try:
        params = {'reverse': request.args.get('reverse')}
        return Gerente.obtener_bancos(params)
    except Exception as e:
        return {'error': str(e)}, 400