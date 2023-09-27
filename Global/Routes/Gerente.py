from flask import Blueprint
from Global.Controllers import Operador as o
from Global.Controllers import Empleado as e

GLOBAL_GERENTE_BLUEPRINT = Blueprint('GLOBAL_GERENTE_BLUEPRINT', __name__)


@GLOBAL_GERENTE_BLUEPRINT.route('/create-operador', methods=['POST'])
def create_operador():
    return o.create_operador()

@GLOBAL_GERENTE_BLUEPRINT.route('/obtener-empleados', methods=['GET'])
def obtener_empleados():
    return e.obtener_empleados()