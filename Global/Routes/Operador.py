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


@GLOBAL_OPERADOR_BLUEPRINT.route('/cancelar-adelanto', methods=['POST'])
def cancelar_solicitud():
    return a.cancelar_solicitud()


@GLOBAL_OPERADOR_BLUEPRINT.route('/obtener-adelantos', methods=['GET'])
def obtener_adelantos():
    return a.obtener_adelantos()


@GLOBAL_OPERADOR_BLUEPRINT.route('/detalles-empleado', methods=['GET'])
def detalles_empleado():
    return e.detalles_empleado()


@GLOBAL_OPERADOR_BLUEPRINT.route('/subir-empleados-bulk', methods=['POST'])
def subir_empleados_bulk():
    return e.subir_empleados_bulk()
