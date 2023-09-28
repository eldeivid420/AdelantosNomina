from flask import Blueprint
from flask import request
from Global.Controllers import Adelanto as a
from twilio.twiml.messaging_response import MessagingResponse

GLOBAL_INCOMING_BLUEPRINT = Blueprint('GLOBAL_INCOMING_BLUEPRINT', __name__)


@GLOBAL_INCOMING_BLUEPRINT.route('', methods=['POST'])
def incoming():

    if request.form["Body"] == "Sí":
        return a.incoming()
    elif request.form["Body"] == "No":
        resp = MessagingResponse()
        resp.message("Gracias por usar nuestro servicio")
        return str(resp), 200

    if request.form["Body"] == 'Opcion 1':
        return a.opcion1()
    else:
        return a.incoming()
