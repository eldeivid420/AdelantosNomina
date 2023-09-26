import os
import jwt
import datetime
class Auth:

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
            return f'Sesión válida'
