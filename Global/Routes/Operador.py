from flask import Blueprint
from Global.Controllers import Empleado as e
from Global.Controllers import  Ticket as t
from Global.Controllers import Adelanto as a

GLOBAL_OPERADOR_BLUEPRINT = Blueprint('GLOBAL_OPERADOR_BLUEPRINT', __name__)


@GLOBAL_OPERADOR_BLUEPRINT.route('/create-empleado', methods=['POST'])
def create_empleado():
    return e.create_empleado()

@GLOBAL_OPERADOR_BLUEPRINT.route('/obtener-empleados', methods=['GET'])
def obtener_empleados():
    return e.obtener_empleados()

@GLOBAL_OPERADOR_BLUEPRINT.route('/crear-ticket', methods=['POST'])
def crear_ticket():
    return t.create_ticket()

@GLOBAL_OPERADOR_BLUEPRINT.route('/cancelar-solicitud', methods=['POST'])
def cancelar_solicitud():
    return a.cancelar_solicitud()

@GLOBAL_OPERADOR_BLUEPRINT.route('/obtener-solicitudes', methods=['GET'])
def obtener_solicitudes():
    return a.obtener_solicitudes()