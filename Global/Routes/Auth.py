from flask import Blueprint
from Global.Controllers import Auth as a

GLOBAL_AUTH_BLUEPRINT = Blueprint('GLOBAL_AUTH_BLUEPRINT', __name__)


@GLOBAL_AUTH_BLUEPRINT.route('/login', methods=['POST'])
def login():
    return a.login()

@GLOBAL_AUTH_BLUEPRINT.route('/validate-session', methods=['GET'])
def validate_session():
    return a.validate_session()

@GLOBAL_AUTH_BLUEPRINT.route('/aceptar-tyc', methods=['POST'])
def aceptar_tyc():
    return a.aceptar_tyc()