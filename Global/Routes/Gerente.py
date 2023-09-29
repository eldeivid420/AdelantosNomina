from flask import Blueprint
from Global.Controllers import Operador as o
from Global.Controllers import Empleado as e
from Global.Controllers import Gerente as g
from Global.Controllers import Ticket as t
from Global.Controllers import Adelanto as a

GLOBAL_GERENTE_BLUEPRINT = Blueprint('GLOBAL_GERENTE_BLUEPRINT', __name__)


@GLOBAL_GERENTE_BLUEPRINT.route('/create-operador', methods=['POST'])
def create_operador():
    return o.create_operador()

@GLOBAL_GERENTE_BLUEPRINT.route('/obtener-empleados', methods=['GET'])
def obtener_empleados():
    return e.obtener_empleados()

@GLOBAL_GERENTE_BLUEPRINT.route('/obtener-bancos', methods=['GET'])
def obtener_bancos():
    return g.obtener_bancos()

@GLOBAL_GERENTE_BLUEPRINT.route('/crear-ticket', methods=['POST'])
def crear_ticket():
    return t.create_ticket()

@GLOBAL_GERENTE_BLUEPRINT.route('/obtener-tickets', methods=['GET'])
def obtener_tickets():
    return t.obtener_tickets()

'''@GLOBAL_GERENTE_BLUEPRINT.route('/crear-adelanto', methods=['POST'])
def crear_adelanto():
    return a.crear_adelanto()'''

@GLOBAL_GERENTE_BLUEPRINT.route('/obtener-solicitudes', methods=['GET'])
def obtener_solicitudes():
    return a.obtener_solicitudes()
