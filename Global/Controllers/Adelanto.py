from flask import request
from twilio.twiml.messaging_response import MessagingResponse


def incoming():
    from main import enviar_mensaje
    try:
        enviar_mensaje('HX78647419e48019069c44a880fdde31df')
        enviar_mensaje('HXbbfc4a72c7fac46712b686e317766799')
        return 200
    except Exception as e:
        return {'error': str(e)}, 400
