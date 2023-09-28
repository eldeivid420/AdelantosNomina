from Global.Utils.db import post, get
from json import load

class Adelanto:

    def __init__(self, params, load=True):
        self.id = None
        self.monto = None
        self.fecha = None
        self.estatus = None
        self.load(params) if load else self.create(params)

    @classmethod
    def validate_adelanto(cls,empleado):
        pass

    def create(self, params):
        print(params)
        self.monto = params["monto"]
        rfc = get('''SELECT rfc FROM empleados WHERE celular = %s''',(params["celular"],), False)[0]
        self.id = post('''INSERT INTO adelantos(monto,estatus_adelanto) VALUES (%s,'creado') RETURNING id''', (self.monto,), True)[0]
        post('''INSERT INTO empleados_adelantos(empleado,adelanto) VALUES (%s,%s)''', (rfc, self.id), False)

    def load(self):
        pass