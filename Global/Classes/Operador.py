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
            post('''INSERT INTO operadores_empresas (operador,empresa) VALUES (%s,%s)''',(self.id, self.empresa), False)

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

    @classmethod
    def obtener_operador(cls, params):
        # modificar si se agregan empresas
        registro = get('''SELECT * FROM operadores WHERE id = %s''', (params["id"],), False)
        if not registro:
            raise Exception('No hay usuarios registrados con ese id')
        empresa = get('''SELECT nombre FROM empresas WHERE id = %s''', (registro[4],), False)[0]
        if registro[6]:
            registro[6] = registro[6].strftime("%d/%m/%Y")
        return {'id': registro[0], 'nombre': registro[1], 'username': registro[2], 'empresa': empresa,
                'creado_en': registro[5].strftime("%d/%m/%Y"), 'editado_en': registro[6]}

    @classmethod
    def obtener_operadores(cls):
        operadores = []
        registros = get('''SELECT * FROM operadores''',(), True)
        print(registros)
        for i in range(len(registros)):
            empresa = get('''SELECT nombre FROM empresas WHERE id = %s''', (registros[i][0],), False)
            print(empresa)
            operadores.append({'id': registros[i][0], 'username': registros[i][1], 'empresa': empresa[i]})
        return operadores

    @classmethod
    def editar_operador(cls, params):
        editado = False
        exist = get('''SELECT username FROM operadores WHERE id = %s''',(params["id"],), False)
        if not exist:
            raise Exception('No hay usuarios registrados con ese id')

        if params["password"]:
            h = hashlib.sha256(params['password'].encode('utf-8')).hexdigest()
            post('''UPDATE operadores SET password = %s WHERE id = %s''', (h, params["id"]), False)
            editado = True
        if params["nombre"]:
            post('''UPDATE operadores SET nombre = %s WHERE id = %s''', (params["nombre"], params["id"]), False)
            editado = True

        if params["empresa"]:
            post('''UPDATE operadores SET empresa = %s WHERE id = %s''', (params["empresa"], params["id"]), False)
            editado = True

        if params["username"]:
            post('''UPDATE operadores SET username = %s WHERE id = %s''', (params["username"], params["id"]), False)
            editado = True

        if editado:
            post('''UPDATE operadores SET editado_en = NOW() WHERE id = %s''',(params["id"],), False)

        return 'Usuario actualizado exitosamente'

    @classmethod
    def eliminar_operador(cls, params):
        exist = get('''SELECT username FROM operadores WHERE id = %s''',(params["id"],), False)
        if not exist:
            raise Exception('No hay usuarios registrados con ese id')
        post('''DELETE FROM operadores WHERE id = %s''', (params["id"],), False)
        post('''DELETE FROM operadores_empresas WHERE operador = %s''', (params["id"],), False)
        return 'Operador eliminado exitosamente'
