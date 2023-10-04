import json

from flask import Blueprint
from flask import request
from Global.Controllers import Adelanto as a
from twilio.twiml.messaging_response import MessagingResponse

GLOBAL_INCOMING_BLUEPRINT = Blueprint('GLOBAL_INCOMING_BLUEPRINT', __name__)


@GLOBAL_INCOMING_BLUEPRINT.route('', methods=['POST'])
def incoming():
    from main import enviar_mensaje
    if request.form["Body"] == "Sí":
        return a.incoming()
    elif request.form["Body"] == "No":
        resp = MessagingResponse()
        resp.message("Gracias por usar nuestro servicio")
        return str(resp), 200

    if request.form["Body"][:8] == "Opcion 1":
        if request.form["Body"] != 'Opcion 1_1' and request.form["Body"] != 'Opcion 1_2':
            enviar_mensaje('HX9cbcc1cd286f6fd37600a34826b19589', request.form["From"][9:])
        return a.opcion1()
    elif request.form["Body"] == 'Opcion 2':
        return a.opcion2()
    elif request.form["Body"] == 'Opcion 3':
        return a.opcion3()
    else:
        print('asdasdsadasd')
        return a.incoming()
