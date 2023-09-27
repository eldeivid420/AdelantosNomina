from flask import Blueprint
from Global.Controllers import Empleado as e

GLOBAL_OPERADOR_BLUEPRINT = Blueprint('GLOBAL_OPERADOR_BLUEPRINT', __name__)


@GLOBAL_OPERADOR_BLUEPRINT.route('/create-empleado', methods=['POST'])
def create_empleado():
    return e.create_empleado()

@GLOBAL_OPERADOR_BLUEPRINT.route('/obtener-empleados', methods=['GET'])
def obtener_empleados():
    return e.obtener_empleados()