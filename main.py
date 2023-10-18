from twilio.rest import Client
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

#Backend config
load_dotenv()
application = Flask(__name__)
cors = CORS(application)

account_sid = os.environ.get('ACCOUNT_SID')
auth_token = os.environ.get('AUTH_TOKEN')
client = Client(account_sid, auth_token)


# Ruta de testing
@application.route("/api")
def hello_there():
    return "General Kenobi", 200

def enviar_mensaje(content_sid, celular, content_variables=None):
    client.messages.create(
        content_sid=content_sid,
        from_='whatsapp:+5215525392003',
        messaging_service_sid='MGf66cef393044e321c2b36af901e7bb8b',
        to='whatsapp:'+celular,
        content_variables=content_variables)

# Blueprints
from Global.Routes.Incoming import GLOBAL_INCOMING_BLUEPRINT
from Global.Routes.Auth import GLOBAL_AUTH_BLUEPRINT
from Global.Routes.Gerente import GLOBAL_GERENTE_BLUEPRINT
from Global.Routes.Operador import GLOBAL_OPERADOR_BLUEPRINT

application.register_blueprint(GLOBAL_INCOMING_BLUEPRINT, url_prefix='/api/incoming')
application.register_blueprint(GLOBAL_AUTH_BLUEPRINT, url_prefix='/api/auth')
application.register_blueprint(GLOBAL_GERENTE_BLUEPRINT, url_prefix='/api/gerente')
application.register_blueprint(GLOBAL_OPERADOR_BLUEPRINT, url_prefix='/api/operador')
print('\nLa aplicación está funcionando...')
print('\n\nNO cierre esta ventana.')
'''from Global.Routes.Inicio import GLOBAL_INICIO_BLUEPRINT
application.register_blueprint(GLOBAL_INICIO_BLUEPRINT, url_prefix='/inicio')'''


if __name__ == "__main__":
    application.run(host="0.0.0.0", debug=True, port = os.environ.get('FLASK_PORT'))
#print(message.sid)