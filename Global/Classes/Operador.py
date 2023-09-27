from Global.Utils.db import post, get
from json import load
import hashlib
import jwt
import os
import datetime


class Operador:

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
            raise Exception('El operador ya habia sido registrado')
        else:
            self.nombre = params['nombre']
            self.username = params['username'].rstrip()
            self.empresa = params['empresa']
            h = hashlib.sha256(params['password'].encode('utf-8')).hexdigest()
            self.password = h
            self.id = post('''INSERT INTO operadores (username,password,nombre,empresa) VALUES (%s,%s,%s,
            %s) RETURNING id''',(self.username,self.password,self.nombre,self.empresa), True)

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
                    "username": self.username,
                    "timestamp": str(timestamp)
                },
                    token,
                    algorithm='HS256'
                )
                self.web_token = web_token
                empresa = get('''SELECT nombre FROM empresas WHERE id = %s''', (self.empresa,),False)[0]
                self.empresa_nombre = empresa
                return self
