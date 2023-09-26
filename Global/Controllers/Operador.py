from flask import request
from Global.Classes.Operador import Operador

def create_operador():
    try:
        params = {'username': request.json.get('username'),
                  'nombre': request.json.get('nombre'),
                  'password': request.json.get('password')}
        operador = Operador(params, False)
        return f'El operador: {operador.nombre} se registró correctamente con el id: {operador.id}', 200
    except Exception as e:
        return {'error': str(e)}, 400
