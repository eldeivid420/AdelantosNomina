from Global.Classes.Empleado import Empleado
from flask import request
import json


def create_empleado():
    from main import enviar_mensaje
    try:
        params = {'nombre': request.json.get('nombre'),
                  'celular': request.json.get('celular'),
                  'direccion': request.json.get('direccion'),
                  'rfc': request.json.get('rfc'),
                  'correo': request.json.get('correo'),
                  'numero_cuenta': request.json.get('numero_cuenta'),
                  'banco': request.json.get('banco'),
                  'telefono_casa': request.json.get('telefono_casa')}
        empleado = Empleado(params, False)
        enviar_mensaje('HX0e1ea052cef82ac5bcb7131a9464b213', params["celular"],
                       content_variables=json.dumps({'1': empleado.nombre}))
        return f'El empleado: {empleado.nombre} se registró correctamente con el id: {empleado.id[0]}', 200
    except Exception as e:
        return {'error': str(e)}, 400


def obtener_empleados():
    """
    Controller for the route /obtener-empleados

    Method:
    * GET

    Parameters:
    * filtro: str - 'alfabetico' -> orders alphabetically; 'fecha' -> orders by date
    * reverse: str - 'true' -> descending order; 'false' -> ascending order

    Format:
    * QueryParams

    Returns:
    * An exception or a 200 status
    """
    try:
        params = {'filtro': request.args.get('filtro'),
                  'reverse': request.args.get('reverse')}
        return Empleado.obtener_empleados(params), 200
    except Exception as e:
        return {'error': str(e)}, 400


def detalles_empleado():
    try:
        params = {'id': request.args.get('id')}
        return Empleado.detalles_empleado(params), 200
    except Exception as e:
        return {'error': str(e)}, 400


def edit_empleado():
    try:
        params = {'id': request.json.get('id'),
                  'nombre': request.json.get('nombre'),
                  'celular': request.json.get('celular'),
                  'direccion': request.json.get('direccion'),
                  'rfc': request.json.get('rfc'),
                  'correo': request.json.get('correo'),
                  'numero_cuenta': request.json.get('numero_cuenta'),
                  'banco': request.json.get('banco'),
                  'telefono_casa': request.json.get('telefono_casa')}

        return {'msg': Empleado.edit_empleado(params)}, 200
    except Exception as e:
        return {'error': str(e)}, 400


def eliminar_empleado():
    try:
        params = {'id': request.json.get('id')}
        return {'msg': Empleado.eliminar_empleado(params)}, 200
    except Exception as e:
        return {'error': str(e)}, 400


def subir_empleados_bulk():
    try:
        empleados = 0
        errores = []
        from main import enviar_mensaje
        params = {"empleados": request.json.get('empleados')}
        for i in range(len(params["empleados"])):

            empleado = Empleado(params["empleados"][i], False, True)
            if empleado.error:
                errores.append({'a_nombre': empleado.nombre, 'b_celular': empleado.celular, 'c_direccion': empleado.direccion,
                                'd_rfc': empleado.rfc, 'e_correo': empleado.correo, 'f_numero_cuenta': empleado.numero_cuenta,
                                'g_banco': empleado.banco, 'h_telefono_casa': empleado.telefono_casa})
            else:
                enviar_mensaje('HX0e1ea052cef82ac5bcb7131a9464b213', params["empleados"][i]["celular"],
                               content_variables=json.dumps({'1': empleado.nombre}))
                empleados += 1
        if len(errores) == 0:
            return {'msg': f'Se registraron {empleados} empleados correctamente'}, 200
        else:
            headers = ['Nombre', 'Celular', 'Dirección', 'RFC', 'Correo', 'Número de Cuenta', 'Banco', 'Teléfono de Casa']
            return {'exitoso': f'Se registraron {empleados} empleados correctamente', 'errores': errores, 'headers': headers}, 200
    except Exception as e:
        return {'error': str(e)}, 400
