from flask import Blueprint
from Global.Controllers import Adelanto as a

GLOBAL_INCOMING_BLUEPRINT = Blueprint('GLOBAL_INCOMING_BLUEPRINT', __name__)


@GLOBAL_INCOMING_BLUEPRINT.route('', methods=['POST'])
def incoming():
    return a.incoming()
