from flask import Blueprint
from Global.Controllers import Empleado as e
from Global.Controllers import  Ticket as t

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