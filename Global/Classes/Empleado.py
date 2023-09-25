from Global.Utils.db import post, get
from json import load
class Empleado:
    def __init__(self, params, load=True):
        self.id = None
        self.nombre = None
        self.celular = None
        self.direccion = None
        self.rfc = None
        self.correo = None
        self.numero_cuenta = None
        self.banco = None
        self.telefono_casa = None
        self.empresa = None
        self.load(params) if load else self.create(params)

    @classmethod
    def exist(cls, params):
        rfc = params['rfc']
        celular = params['rfc']
        registro = get('''SELECT id FROM empleados WHERE rfc = %s and celular = %s''',(rfc,celular),False)
        if registro:
            raise Exception('El rfc o el celular ya existen en la base de datos')
        else:
            return False

    def create(self, params):
        self.nombre = params['nombre']
        self.celular = params['celular']
        self.direccion = params['direccion']
        self.rfc = params['rfc']
        self.correo = params['correo']
        self.numero_cuenta = params['numero_cuenta']
        self.banco = params['banco']
        self.telefono_casa = params['telefono_casa']
        self.empresa = params['empresa']

        # Si el usuario no existe, lo creamos
        if not self.exist(params):
            self.id = post('''INSERT INTO empleados (nombre,celular,direccion,rfc,correo,numero_cuenta,banco,
            telefono_casa,empresa) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id''',
                           (self.nombre, self.celular, self.direccion, self.rfc, self.correo, self.numero_cuenta,
                            self.banco, self.telefono_casa, self.empresa), False)

