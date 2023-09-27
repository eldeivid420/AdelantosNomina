import os
import jwt
import datetime
from Global.Utils.db import post, get
from Global.Classes.Operador import Operador
class Auth:

    @classmethod
    def obtain_role(cls, username):
        operador = get('''SELECT id FROM operadores WHERE username = %s''', (username,), False)
        if operador:
            return 'operador'
        if not operador:
            gerente = get('''SELECT id FROM gerentes WHERE username = %s''', (username,), False)
            if not gerente:
                raise Exception(f'No existe el ususario en la base de datos')
            else:
                return 'gerente'

    @classmethod
    def generate_token(cls,user):
        token = os.environ.get('JWT_TOKEN')
        timestamp = datetime.datetime.now()
        web_token = jwt.encode({
            "id": user[0],
            "username": user[2],
            "timestamp": str(timestamp)
        },
            token,
            algorithm='HS256'
        )
        return web_token

    @classmethod
    def validar_token(cls,token):
        token_desencriptado = jwt.decode(token, os.environ.get('JWT_TOKEN'), 'HS256')
        hora_actual = datetime.datetime.now()
        hora_actual = hora_actual.strftime("%d/%m/%Y")
        #pendiente funcion que calcule diferencia de tiempos en minutos
        hora_token = datetime.datetime.strptime(token_desencriptado['timestamp'][:10], "%Y-%m-%d")
        hora_token = hora_token.strftime("%d/%m/%Y")
        if hora_token != hora_actual:
            raise Exception('Token expirado')
        else:
            rol = cls.obtain_role(token_desencriptado["username"])
            params = {'username': token_desencriptado["username"]}
            mensaje = 'Sesión válida'
            if rol == "operador":
                operador = Operador.exist(params)
                empresa = get('''SELECT nombre FROM empresas WHERE id = %s''', (operador[4],), False)[0]
                return {'nombre': operador[1], 'empresa': empresa, 'tipo': 'operador', 'message': mensaje}
