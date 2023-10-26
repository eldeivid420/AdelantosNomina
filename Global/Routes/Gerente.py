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

@GLOBAL_GERENTE_BLUEPRINT.route('/detalles-empleado', methods=['GET'])
def detalles_empleado():
    return e.detalles_empleado()

@GLOBAL_GERENTE_BLUEPRINT.route('/obtener-bancos', methods=['GET'])
def obtener_bancos():
    return g.obtener_bancos()

@GLOBAL_GERENTE_BLUEPRINT.route('/crear-ticket', methods=['POST'])
def crear_ticket():
    return t.create_ticket()

@GLOBAL_GERENTE_BLUEPRINT.route('/obtener-tickets', methods=['GET'])
def obtener_tickets():
    return t.obtener_tickets()

@GLOBAL_GERENTE_BLUEPRINT.route('/crear-adelanto', methods=['POST'])
def crear_adelanto():
    return a.crear_adelanto()

@GLOBAL_GERENTE_BLUEPRINT.route('/obtener-adelantos', methods=['GET'])
def obtener_adelantos():
    return a.obtener_adelantos()

@GLOBAL_GERENTE_BLUEPRINT.route('/pagar-adelanto', methods=['POST'])
def pagar_adelanto():
    return a.pagar_adelanto()

@GLOBAL_GERENTE_BLUEPRINT.route('/obtener-operadores', methods=['GET'])
def obtener_operadores():
    return o.obtener_operadores()

@GLOBAL_GERENTE_BLUEPRINT.route('/crear-gerente', methods=['POST'])
def crear_gerente():
    return g.create_gerente()

@GLOBAL_GERENTE_BLUEPRINT.route('/buscar-operador', methods=['GET'])
def buscar_operador():
    return o.buscar_operador()

@GLOBAL_GERENTE_BLUEPRINT.route('/editar-operador', methods=['POST'])
def editar_operador():
    return o.editar_operador()

@GLOBAL_GERENTE_BLUEPRINT.route('/eliminar-operador', methods=['POST'])
def eliminar_operador():
    return o.eliminar_operador()

@GLOBAL_GERENTE_BLUEPRINT.route('/validar-adelanto', methods=['POST'])
def validar_adelanto():
    return a.validar_adelanto()

@GLOBAL_GERENTE_BLUEPRINT.route('/edit-empleado', methods=['POST'])
def edit_empleado():
    return e.edit_empleado()

@GLOBAL_GERENTE_BLUEPRINT.route('/generar-reporte', methods=['POST'])
def generar_reporte():
    return g.generar_reporte()

'''@GLOBAL_GERENTE_BLUEPRINT.route('/eliminar-empleado', methods=['POST'])
def eliminar_empleado():
    return e.eliminar_empleado()'''