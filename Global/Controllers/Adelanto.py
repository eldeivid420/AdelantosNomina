import json

from flask import request
from twilio.twiml.messaging_response import MessagingResponse
from Global.Classes.Empleado import Empleado
from Global.Classes.Adelanto import Adelanto


def incoming():
    from main import enviar_mensaje
    try:
        registrado = Empleado.verify_phone(request.form["From"][9:])
        if not registrado:
            enviar_mensaje('HX5f799704caf07549cb25ce94026c01ce')
            return 'Error', 200
        enviar_mensaje('HXbbfc4a72c7fac46712b686e317766799')
        return 'Success', 200
    except Exception as e:
        return {'error': str(e)}, 400


def opcion1():
    from main import enviar_mensaje
    resp = MessagingResponse()

    monto = request.form["ListTitle"]
    if monto == "Salir":
        resp.message("Gracias por usar nuestro servicio")
        return str(resp), 200

    if monto == 'MXN $1000':
        params = {'monto': 1000, 'celular': request.form["From"][9:]}
        adelanto = Adelanto(params, False)
        enviar_mensaje('HXa06a2deebab5fdeaa0f3cf71fe30b351', content_variables=json.dumps({'1': str(adelanto.monto)}))
        return 'Success', 200
    elif monto == 'MXN $500':
        params = {'monto': 500, 'celular': request.form["From"][9:]}
        adelanto = Adelanto(params, False)
        enviar_mensaje('HXa06a2deebab5fdeaa0f3cf71fe30b351', content_variables=json.dumps({'1': str(adelanto.monto)}))
        return 'Success', 200
    else:
        return 'success', 200


'''def crear_adelanto():
    try:
        params = {'monto': 1000, 'celular': '+5215526998823'}
        adelanto = Adelanto(params, False)
        return f'Adelanto con id {adelanto.id} creado'
    except Exception as e:
        return {'error': str(e)}, 400'''


def cancelar_solicitud():
    try:
        params = {'id': request.json.get('id')}
        return Adelanto.cancelar_solicitud(params), 200
    except Exception as e:
        return {'error': str(e)}, 400


def obtener_solicitudes():
    try:
        params = {'estatus_adelanto': request.args.get('estatus_adelanto'),
                  'monto': request.args.get('monto')}
        return Adelanto.obtener_solicitudes(params), 200
    except Exception as e:
        return {'error': str(e)}, 400
