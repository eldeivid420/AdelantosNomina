from Global.Classes.Empleado import Empleado
from flask import request


def create_empleado():
    try:
        params = {'nombre': request.json.get('nombre'),
                  'celular': request.json.get('celular'),
                  'direccion': request.json.get('direccion'),
                  'rfc': request.json.get('rfc'),
                  'correo': request.json.get('correo'),
                  'numero_cuenta': request.json.get('numero_cuenta'),
                  'banco': request.json.get('banco'),
                  'telefono_casa': request.json.get('telefono_casa'),
                  'empresa': request.json.get('empresa')}
        empleado = Empleado(params, False)
        return f'El empleado: {empleado.nombre} se registró correctamente con el id: {empleado.id[0]}', 200
    except Exception as e:
        return {'error': str(e)}, 400


def obtener_empleados():
    try:
        params = {'filtro': request.args.get('filtro'),
                  'reverse': request.args.get('reverse')}
        return Empleado.obtener_empleados(params), 200
    except Exception as e:
        return {'error': str(e)}, 400
