from Global.Utils.db import post, get
from json import load
import hashlib
import jwt
import os
import datetime

class Gerente:

    def __init__(self):
        self.id = None
        self.username = None
        self.password = None
        self.nombre = None
        self.creado_en = None
        self.editado_en = None
        self.web_token = None
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
            h = hashlib.sha256(params['password'].encode('utf-8')).hexdigest()
            self.password = h
            self.id = post('''INSERT INTO gerentes (username,password,nombre) VALUES (%s,%s,%s) RETURNING id''',(self.username,self.password,self.nombre), False)

    def load(self, params):
        exist = self.exist(params)
        if not exist:
            raise Exception('El usuario no está registrado')
        else:
            self.id = exist[0]
            self.nombre = exist[1]
            self.username = exist[2]
            self.password = exist[3]
            self.creado_en = exist[4]
            self.editado_en = exist[5]
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
                return self