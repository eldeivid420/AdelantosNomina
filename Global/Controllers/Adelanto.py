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
        #enviar_mensaje('HX78647419e48019069c44a880fdde31df')
        #body = request.form
        #print(body)
        return 'Success', 200
    except Exception as e:
        return {'error': str(e)}, 400

def opcion1():
    from main import enviar_mensaje
    resp = MessagingResponse()

    enviar_mensaje('HX2fb07aacfde5200a6d82fdfe73791764')
    monto = request.form["ListTitle"]
    if monto == "Salir":
        resp.message("Gracias por usar nuestro servicio")
        return str(resp), 200

    if monto == 'MXN $1000':
        params = {'monto': 1000, 'celular': request.form["from"][10:]}
        adelanto = Adelanto(params, False)
        enviar_mensaje('HXa06a2deebab5fdeaa0f3cf71fe30b351', content_variables=adelanto)
        return 'Success', 200

    elif monto == 'MXN $500':
        params = {'monto': 500, 'celular': request.form["from"][10:]}
        adelanto = Adelanto(params, False)
        enviar_mensaje('HXa06a2deebab5fdeaa0f3cf71fe30b351', content_variables=adelanto)
        return 'Success', 200

    else:
        enviar_mensaje('HX1cdac2268d5e6913f2e10ffd3e59a0e2')
