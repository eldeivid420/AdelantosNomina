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
        registro = get('''SELECT id FROM empleados WHERE rfc = %s and celular = %s''', (rfc, celular), False)
        if registro:
            raise Exception('El rfc o el celular ya existen en la base de datos')
        else:
            return False

    @classmethod
    def verify_phone(cls, phone):
        print(phone)
        exist = get('''SELECT celular FROM empleados WHERE celular = %s''',(phone,),False)
        print(exist)
        if not exist:
            return False
        else:
            return True

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
                            self.banco, self.telefono_casa, self.empresa), True)

    @classmethod
    def obtener_empleados(cls, params):
        empleados = []
        filtro = params['filtro']
        reverse = params['reverse']
        if filtro == 'alfabetico' and reverse == 'true':
            registros = get('''SELECT * FROM empleados ORDER BY nombre DESC''', (), True)
        elif filtro == 'alfabetico' and reverse == 'false':
            registros = get('''SELECT * FROM empleados ORDER BY nombre ASC''', (), True)
        elif filtro == 'fecha' and reverse == 'true':
            registros = get('''SELECT * FROM empleados ORDER BY creado_en DESC''', (), True)
        elif filtro == 'fecha' and reverse == 'false':
            registros = get('''SELECT * FROM empleados ORDER BY creado_en ASC''', (), True)
        else:
            raise Exception('Selecciona una opción de filtrado válida')

        if not registros:
            raise Exception('No hay registros en la base de datos')

        for i in range(len(registros)):
            banco = get('''SELECT nombre FROM bancos WHERE id = %s''', (registros[i][7],), False)[0]
            empresa = get('''SELECT nombre FROM empresas WHERE id = %s''', (registros[i][9],), False)[0]
            empleados.append({'id': registros[i][0], 'nombre': registros[i][1], 'celular': registros[i][2],
                              'direccion': registros[i][3], 'rfc': registros[i][4], 'correo': registros[i][5],
                              'numero_cuenta': registros[i][6], 'banco': banco, 'telefono_casa': registros[i][8],
                              'empresa': empresa, 'creado_en': registros[i][10], 'editado_en': registros[i][11]})
        return empleados