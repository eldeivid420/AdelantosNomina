from flask import Blueprint
from Global.Controllers import Auth as a

GLOBAL_AUTH_BLUEPRINT = Blueprint('GLOBAL_AUTH_BLUEPRINT', __name__)


@GLOBAL_AUTH_BLUEPRINT.route('/login', methods=['POST'])
def login():
    return a.login()