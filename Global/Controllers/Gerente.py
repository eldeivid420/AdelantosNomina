from flask import request
from Global.Classes.Gerente import Gerente

def create_gerente():
    try:
        params = {'username': request.json.get('username'),
                  'nombre': request.json.get('nombre'),
                  'password': request.json.get('password')}
        gerente = Gerente(params, False)
        return {"message":f'El gerente: {gerente.nombre} se registró correctamente con el id: {gerente.id}'}, 200
    except Exception as e:
        return {'error': str(e)}, 400


def obtener_bancos():
    try:
        params = {'reverse': request.args.get('reverse')}
        return Gerente.obtener_bancos(params), 200
    except Exception as e:
        return {'error': str(e)}, 400


def generar_reporte():
    try:
        params = {"empresas": request.json.get('empresas'),
                  "bancos": request.json.get('bancos'),
                  "montos": request.json.get('montos'),
                  "fechas": request.json.get('fechas')}
        return Gerente.generar_reporte(params), 200
    except Exception as e:
        return {'error': str(e)}, 400
