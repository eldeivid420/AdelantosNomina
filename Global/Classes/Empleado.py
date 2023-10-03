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
        empresa = params['empresa']
        registro = get('''SELECT id FROM empleados WHERE rfc = %s and empresa = %s''', (rfc, empresa), False)
        if registro:
            raise Exception('El rfc o el celular ya existen en la base de datos')
        else:
            return False

    @classmethod
    def verify_phone(cls, phone):
        exist = get('''SELECT celular FROM empleados WHERE celular = %s''',(phone,),False)
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
            if registros[i][11]:
                registros[i][11] = registros[i][11].strftime("%d/%m/%Y")
            empleados.append({'id': registros[i][0], 'nombre': registros[i][1], 'celular': registros[i][2],
                              'direccion': registros[i][3], 'rfc': registros[i][4], 'correo': registros[i][5],
                              'numero_cuenta': registros[i][6], 'banco': banco, 'telefono_casa': registros[i][8],
                              'empresa': empresa, 'creado_en': registros[i][10].strftime("%d/%m/%Y"), 'editado_en': registros[i][11]})
        return empleados

    @classmethod
    def detalles_empleado(cls, params):
        empleado = get('''SELECT * FROM empleados WHERE id = %s''', (params["id"],),False)
        empresa = get('''SELECT nombre FROM empresas WHERE id = %s''',(empleado[9],),False)[0]
        banco = get('''SELECT nombre FROM bancos WHERE id = %s''', (empleado[7],),False)[0]
        return {'id': empleado[0], 'nombre': empleado[1], 'celular': empleado[2], 'direccion': empleado[3],
                'rfc': empleado[4], 'correo': empleado[5], 'numero_cuenta': empleado[6], 'banco': banco,
                'telefono_casa': empleado[8], 'empresa': empresa, 'creado_en': empleado[10], 'editado_en': empleado[11]}

    @classmethod
    def cancelar_ultimo_adelanto(cls, params):
        # revisar si se agregan mas empresas
        empleado = get('''SELECT id FROM empleados WHERE celular = %s''',(params["celular"],), False)
        adelanto = get('''SELECT adelanto FROM empleados_adelantos WHERE empleado = %s ORDER BY adelanto DESC''',(empleado,), False)[0]
        if not adelanto:
            return 'no registros'
        estatus = get('''SELECT estatus_adelanto FROM adelantos WHERE id = %s''', (adelanto,), False)[0]

        if estatus == 'cancelado':
            return 'cancelado'
        elif estatus == 'pagado':
            return 'pagado'
        elif estatus == 'creado':
            post('''UPDATE adelantos SET estatus_adelanto = 'cancelado' WHERE id = %s''', (adelanto,), False)
            return 'realizado'
        else:
            return False

