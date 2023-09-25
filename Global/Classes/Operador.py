from Global.Utils.db import post, get
from json import load
import hashlib
import jwt
import os

class Operador:

    def __init__(self, params, load=True):
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
            raise Exception('El operador ya habia sido registrado')
        else:
            self.nombre = params['nombre']
            self.username = params['username'].rstrip()
            h = hashlib.sha256(params['passWORD'].encode('utf-8')).hexdigest()
            self.password = h
            self.id = post('''INSERT INTO operadores (username,password,nombre) VALUES (%s,%s,%s) RETURNING id''',(self.username,self.password,self.nombre), False)
        return f'El usuario: {self.username} se registró exitosamente con el id: {self.id}'

    def load(self, params):
        exist = self.exist(params)
        if not exist:
            raise Exception('El usuario no está registrado')
        else:
            self.username = params['username']
            h = hashlib.sha256(params['password'].encode('utf-8')).hexdigest()
            if exist[1] != h:
                raise Exception('Contraseña incorrecta')
            else:

                token = os.environ.get('JWT_TOKEN')
                web_token = jwt.encode({
                    "id": self.id
                },
                    token,
                    algorithm='HS256'
                )
                self.web_token = web_token
                return self


