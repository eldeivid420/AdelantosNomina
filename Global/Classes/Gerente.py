from Global.Utils.db import post, get
from json import load
import hashlib
import jwt
import os
import datetime

class Gerente:

    def __init__(self, params, load=True):
        self.id = None
        self.username = None
        self.password = None
        self.nombre = None
        self.creado_en = None
        self.editado_en = None
        self.web_token = None
        self.empresa = None
        self.empresa_nombre = None
        self.load(params) if load else self.create(params)

    @classmethod
    def exist(cls, params):
        exist = get('''SELECT * FROM operadores WHERE username = %s''',(params['username'],),False)
        if exist:
            return exist
        else:
            return False

    def create(self, params):
        if self.exist(params):
            raise Exception('El gerente ya habia sido registrado')
        else:
            self.nombre = params['nombre']
            self.username = params['username'].rstrip()
            self.empresa = params['empresa']
            h = hashlib.sha256(params['password'].encode('utf-8')).hexdigest()
            self.password = h
            self.id = post('''INSERT INTO gerentes (username,password,nombre,empresa) VALUES (%s,%s,%s,%s) RETURNING 
            id''',(self.username,self.password,self.nombre,self.empresa), True)[0]

    def load(self, params):
        exist = self.exist(params)
        if not exist:
            raise Exception('El usuario no está registrado')
        else:
            self.id = exist[0]
            self.nombre = exist[1]
            self.username = exist[2]
            self.password = exist[3]
            self.empresa = exist[4]
            self.creado_en = exist[5]
            self.editado_en = exist[6]
            h = hashlib.sha256(params['password'].encode('utf-8')).hexdigest()
            if exist[3] != h:
                raise Exception('Contraseña incorrecta')
            else:
                token = os.environ.get('JWT_TOKEN')
                timestamp = datetime.datetime.now()
                web_token = jwt.encode({
                    "id": self.id,
                    "timestamp": str(timestamp)
                },
                    token,
                    algorithm='HS256'
                )
                self.web_token = web_token
                empresa = get('''SELECT nombre FROM empresas WHERE id = %s''', (self.empresa,),False)[0]
                self.empresa_nombre = empresa
                return self

    @classmethod
    def obtener_bancos(cls, params):
        bancos = []
        if params["reverse"] == "true":
            registros = get('''SELECT * FROM bancos ORDER BY bancos DESC''', (), True)
        elif params["reverse"] == "false":
            registros = get('''SELECT * FROM bancos ORDER BY bancos ASC''', (), True)
        else:
            raise Exception('reverse sólo puede ser "true" o "false"')
        if not registros:
            raise Exception('No hay registros en la base de datos')

        for i in range(len(registros)):
            bancos.append({'id': registros[i][0], 'nombre': registros[i][1]})

        return bancos
