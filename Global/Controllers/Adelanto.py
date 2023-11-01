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
            enviar_mensaje('HX5f799704caf07549cb25ce94026c01ce', request.form["From"][9:])
            return 'Error', 200

        params = {'celular': request.form["From"][9:]}
        empleado = Empleado.obtener_id(params)
        tyc = Empleado.check_tyc(empleado)
        if not tyc:
            enviar_mensaje('HX952867a59c360f0c3a3ad9b1ec118f06', request.form["From"][9:],
                           content_variables=json.dumps({'1': str(empleado)}))
            return 'Error', 200
        elif tyc:
            enviar_mensaje('HXb37aad21bf9a99f68ab2a9c105caaf26', request.form["From"][9:])
            return 'Success', 200

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
        valido = Adelanto.validate_adelanto(params)
        if valido == 'autorizado':
            enviar_mensaje('HXd9dce63775be2c311a1d89920b4806dc', request.form["From"][9:],
                           content_variables=json.dumps({'1': str(1000), '2': str(60), '3': str(10.53), '4': str(923.67)}))
        elif valido == 'rechazado':
            enviar_mensaje('HX8d026a1612ec6b339e46410d50a1a2be', request.form["From"][9:])
        return 'Success', 200

    elif monto == 'MXN $500':
        params = {'monto': 500, 'celular': request.form["From"][9:]}
        valido = Adelanto.validate_adelanto(params)
        if valido == 'autorizado':
            enviar_mensaje('HX7058906d8b763f6ffaa7e1c5560f5e89', request.form["From"][9:],
                           content_variables=json.dumps(
                               {'1': str(500), '2': str(40), '3': str(7.33), '4': str(446.87)}))
        elif valido == 'rechazado':
            enviar_mensaje('HX8d026a1612ec6b339e46410d50a1a2be', request.form["From"][9:])
        return 'Success', 200

    elif request.form["Body"] == 'Opcion 1_a1000':
        params = {'monto': 1000, 'celular': request.form["From"][9:]}
        adelanto = Adelanto(params, False)
        enviar_mensaje('HXa06a2deebab5fdeaa0f3cf71fe30b351', request.form["From"][9:],
                       content_variables=json.dumps({'1': str(adelanto.monto)}))
        return 'Success', 200

    elif request.form["Body"] == 'Opcion 1_a500':
        params = {'monto': 500, 'celular': request.form["From"][9:]}
        adelanto = Adelanto(params, False)
        enviar_mensaje('HXfd4772b02d108fa58ff9be5a8cbb96a5', request.form["From"][9:],
                       content_variables=json.dumps({'1': str(adelanto.monto)}))
        return 'Success', 200
    elif request.form["Body"] == 'Opcion 1_n':
        enviar_mensaje('HXfd4772b02d108fa58ff9be5a8cbb96a5', request.form["From"][9:])
        return 'Success', 200
    else:
        return 'Success', 200

def opcion2():
    from main import enviar_mensaje
    resp = MessagingResponse()

    opcion = request.form["ListTitle"]
    if opcion == "Salir":
        resp.message("Gracias por usar nuestro servicio")
        return str(resp), 200

    if opcion == "Cancelar un adelanto":
        params = {'celular': request.form["From"][9:]}
        cancelacion = Empleado.cancelar_ultimo_adelanto(params)

        if cancelacion == 'no registros':
            enviar_mensaje('HX5e4518fa767840cff123d755e771401a', request.form["From"][9:])
            return 'success', 200
        elif cancelacion == 'pagado':
            enviar_mensaje('HX33104d9a38f633d1c95c8aec6158b937', request.form["From"][9:])
            return 'success', 200
        elif cancelacion == 'cancelado':
            enviar_mensaje('HXabb17014142d102191eb425fce0393d4', request.form["From"][9:])
            return 'success', 200
        elif cancelacion == 'realizado':
            enviar_mensaje('HX9d62716fffb5f94fd537c54c82fe9c17', request.form["From"][9:])
            return 'success', 200

    else:
        return 'success', 200

def opcion3():
    from main import enviar_mensaje
    resp = MessagingResponse()

    opcion = request.form["ListTitle"]
    if opcion == "Salir":
        resp.message("Gracias por usar nuestro servicio")
        return str(resp), 200

    if opcion == 'Cómo va mi adelanto?':
        params = {'celular': request.form["From"][9:]}
        estatus = Empleado.estatus_ultimo_adelanto(params)
        if estatus == 'no registros':
            enviar_mensaje('HX5e4518fa767840cff123d755e771401a', request.form["From"][9:])
            return 'success', 200
        else:
            enviar_mensaje('HXd9104b00e485d371833bd1970e5d2fd7', request.form["From"][9:], content_variables=json.dumps({'1': estatus}))
            return 'success', 200
    else:
        return 'success', 200


def opcion4():
    from main import enviar_mensaje
    resp = MessagingResponse()

    opcion = request.form["ListTitle"]
    if opcion == "Salir":
        resp.message("Gracias por usar nuestro servicio")
        return str(resp), 200

    if opcion == 'Términos y condiciones':
        params = {'celular': request.form["From"][9:]}
        empleado = Empleado.obtener_id(params)
        enviar_mensaje('HX80196b9f0ea386aa268b8d61bb4f7636', request.form["From"][9:],
                       content_variables=json.dumps({'1': str(empleado)}))
        return 'success', 200
    else:
        return 'success', 200




def crear_adelanto():
    try:
        params = {'monto': request.json.get('monto'), 'celular': request.json.get('celular')}
        adelanto = Adelanto(params, False)
        return f'Adelanto con id {adelanto.id} creado'
    except Exception as e:
        return {'error': str(e)}, 400


def cancelar_solicitud():
    try:
        params = {'id': request.json.get('id')}
        return Adelanto.cancelar_solicitud(params), 200
    except Exception as e:
        return {'error': str(e)}, 400


def obtener_adelantos():
    try:
        params = {'estatus_adelanto': request.args.get('estatus_adelanto'),
                  'monto': request.args.get('monto')}
        return Adelanto.obtener_adelantos(params), 200
    except Exception as e:
        return {'error': str(e)}, 400


def pagar_adelanto():
    try:
        params = {'id': request.json.get('id')}
        celular = Adelanto.get_celular_adelanto(params)
        if celular:
            from main import enviar_mensaje
            enviar_mensaje('HX80196b9f0ea386aa268b8d61bb4f7636', celular)
            return {"message": Adelanto.pagar_adelanto(params)}, 200
    except Exception as e:
        return {'error': str(e)}, 400


def validar_adelanto():
    try:
        params = {'celular': request.json.get('celular'),
                  'monto': request.json.get('monto')}
        return {"message": Adelanto.validate_adelanto(params)}, 200
    except Exception as e:
        return {'error': str(e)}, 400