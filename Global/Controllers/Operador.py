from flask import request
from Global.Classes.Operador import Operador

def create_operador():
    try:
        params = {'username': request.json.get('username'),
                  'password': request.json.get('password'),
                  'nombre': request.json.get('nombre'),
                  'empresa': request.json.get('empresa')}
        operador = Operador(params, False)
        return f'El operador: {operador.nombre} se registró correctamente con el id: {operador.id[0]}', 200
    except Exception as e:
        return {'error': str(e)}, 400


def obtener_operadores():
    try:
        return Operador.obtener_operadores()
    except Exception as e:
        return {'error': str(e)}, 400


def buscar_operador():
    try:
        params = {'id': request.args.get('id')}
        return Operador.obtener_operador(params), 200
    except Exception as e:
        return {'error': str(e)}, 400

def editar_operador():
    try:
        params = {'id': request.json.get('id'),
                  'nombre': request.json.get('nombre'),
                  'username': request.json.get('username'),
                  'password': request.json.get('password'),
                  'empresa': request.json.get('empresa')}
        return Operador.editar_operador(params), 200
    except Exception as e:
        return {'error': str(e)}, 400


def eliminar_operador():
    try:
        params = {'id': request.json.get('id')}
        return Operador.eliminar_operador(params), 200
    except Exception as e:
        return {'error': str(e)}, 400