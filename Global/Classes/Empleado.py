from Global.Utils.db import post, get
from json import load
import json


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
        self.empresa = 1
        self.load(params) if load else self.create(params)

    @classmethod
    def exist(cls, params):
        rfc = params['rfc']
        empresa = 1
        celular = params['celular']
        correo = params['correo']
        registro = get('''SELECT id FROM empleados WHERE (rfc = %s and empresa = %s) OR 
        (celular = %s AND empresa = %s) OR (correo = %s AND empresa = %s)''', (rfc, empresa, celular,
                                                                               empresa, correo, empresa), False)
        if registro:
            raise Exception('El rfc, celular o correo ya existen en la base de datos')
        else:
            return False

    @classmethod
    def verify_phone(cls, phone):
        exist = get('''SELECT celular FROM empleados WHERE celular = %s''', (phone,), False)
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
        self.empresa = 1
        '''if not params["empresa"]:
            self.empresa = 1
        else:
            self.empresa = params['empresa']'''

        # Si el usuario no existe, lo creamos
        if not self.exist(params):
            self.id = post('''INSERT INTO empleados (nombre,celular,direccion,rfc,correo,numero_cuenta,banco,
            telefono_casa,empresa) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id''',
                           (self.nombre, self.celular, self.direccion, self.rfc, self.correo, self.numero_cuenta,
                            self.banco, self.telefono_casa, self.empresa), True)

    def load(self, params):
        self.id = params["id"]
        self.nombre, self.celular, self.direccion, self.rfc, self.correo, self.numero_cuenta, self.banco, self.telefono_casa = get(
            '''SELECT nombre,celular,direccion,rfc,correo,numero_cuenta,banco,telefono_casa FROM empleados WHERE id = 
            %s''', (self.id,), False)
        return self
    @classmethod
    def obtener_empleados(cls, params):
        empleados = []
        filtro = params['filtro']
        reverse = params['reverse']
        headers = ["Banco", "Celular", "Correo", "Creado en", "Dirección", "Editado en", "Empresa", "ID de empleado",
                   "Nombre", "Número de cuenta", "RFC", "Teléfono de casa"]
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
                editado_en = registros[i][11].strftime("%d/%m/%Y")
            else:
                editado_en = None
            empleados.append({'id': registros[i][0], 'nombre': registros[i][1], 'celular': registros[i][2],
                              'direccion': registros[i][3], 'rfc': registros[i][4], 'correo': registros[i][5],
                              'numero_cuenta': registros[i][6], 'banco': banco, 'telefono_casa': registros[i][8],
                              'empresa': empresa, 'creado_en': registros[i][10].strftime("%d/%m/%Y"),
                              'editado_en': editado_en})

        return {"DatosTabla": empleados, "DatosCsv": {"headers": headers, "data": empleados}}

    @classmethod
    def detalles_empleado(cls, params):
        empleado = get('''SELECT * FROM empleados WHERE id = %s''', (params["id"],), False)
        empresa = get('''SELECT nombre FROM empresas WHERE id = %s''', (empleado[9],), False)[0]
        banco = get('''SELECT nombre FROM bancos WHERE id = %s''', (empleado[7],), False)[0]
        return {'id': empleado[0], 'nombre': empleado[1], 'celular': empleado[2], 'direccion': empleado[3],
                'rfc': empleado[4], 'correo': empleado[5], 'numero_cuenta': empleado[6], 'banco': banco,
                'telefono_casa': empleado[8], 'empresa': empresa, 'creado_en': empleado[10], 'editado_en': empleado[11]}

    @classmethod
    def cancelar_ultimo_adelanto(cls, params):
        # revisar si se agregan mas empresas
        empleado = get('''SELECT id FROM empleados WHERE celular = %s''', (params["celular"],), False)
        adelanto = get('''SELECT adelanto FROM empleados_adelantos WHERE empleado = %s ORDER BY adelanto DESC''',
                       (empleado,), False)
        if not adelanto:
            return 'no registros'
        estatus = get('''SELECT estatus_adelanto FROM adelantos WHERE id = %s''', (adelanto[0],), False)[0]

        if estatus == 'cancelado':
            return 'cancelado'
        elif estatus == 'pagado':
            return 'pagado'
        elif estatus == 'creado':
            post('''UPDATE adelantos SET estatus_adelanto = 'cancelado' WHERE id = %s''', (adelanto,), False)
            return 'realizado'
        else:
            return False

    @classmethod
    def estatus_ultimo_adelanto(cls, params):
        # revisar si se agregan mas empresas
        empleado = get('''SELECT id FROM empleados WHERE celular = %s''', (params["celular"],), False)
        adelanto = get('''SELECT adelanto FROM empleados_adelantos WHERE empleado = %s ORDER BY adelanto DESC''',
                       (empleado[0],), False)
        if not adelanto:
            return 'no registros'
        estatus = get('''SELECT estatus_adelanto FROM adelantos WHERE id = %s''', (adelanto[0],), False)[0]

        if estatus == 'cancelado':
            return 'cancelado'
        elif estatus == 'pagado':
            return 'pagado'
        elif estatus == 'creado':
            return 'en espera a ser depositado'
        else:
            return False

    @classmethod
    def edit_empleado(cls, params):
        update_celular = False
        exist = get('''SELECT nombre FROM empleados WHERE id = %s''', (params["id"],), False)
        if not exist:
            raise Exception(f'No hay usuarios registrados con el id {params["id"]}')
        # actualizar si se agregan nuevas empresas
        empresa_actual = get('''SELECT empresa FROM empleados WHERE id = %s''', (params["id"],), False)[0]

        celular = get('''SELECT id FROM empleados WHERE (celular = %s AND empresa = %s)''',
                      (params["celular"], empresa_actual), False)
        if not celular:
            update_celular = True
        elif celular[0] == params["id"]:
            update_celular = False

        post('''UPDATE empleados SET nombre = %s, celular = %s, direccion = %s, rfc = %s, correo = %s, 
        numero_cuenta = %s, banco = %s, telefono_casa = %s, editado_en = NOW() WHERE id = %s''',
             (params["nombre"], params["celular"], params["direccion"], params["rfc"],
              params["correo"], params["numero_cuenta"], params["banco"], params["telefono_casa"], params["id"]), False)

        if update_celular:
            post('''UPDATE empleados SET celular = %s WHERE id = %s''', (params["celular"], params["id"]))
            from main import enviar_mensaje
            enviar_mensaje('HX0e1ea052cef82ac5bcb7131a9464b213', params["celular"],
                           content_variables=json.dumps({'1': str(exist[0])}))

        return 'Empleado editado exitosamente'

    @classmethod
    def eliminar_empleado(cls, params):
        exist = get('''SELECT nombre FROM empleados WHERE id = %s''', (params["id"],), False)
        if not exist:
            raise Exception(f'No hay usuarios registrados con el id {params["id"]}')
        post('''DELETE FROM empleados WHERE id = %s''', (params["id"],), False)
        post('''DELETE FROM empleados_adelantos WHERE empleado = %s''', (params["id"],), False)
        return 'Empleado eliminado exitosamente'

    @classmethod
    def obtener_id(cls, params):
        empleado_id = get('''SELECT id FROM empleados WHERE celular = %s''', (params["celular"],), False)[0]
        return empleado_id

    @classmethod
    def aceptar_tyc(cls, params):
        empleado_id = get('''SELECT id FROM empleados WHERE id = %s''', (params["id"],), False)
        if not empleado_id:
            raise Exception(f'No hay usuarios registrados con el id {params["id"]}')
        post('''UPDATE empleados SET terminos_aceptados = true WHERE id = %s''', (empleado_id[0],), False)
        return 'Terminos y condiciones aceptadas'

    @classmethod
    def check_tyc(cls, empleado):
        tyc = get('''SELECT terminos_aceptados FROM empleados WHERE id = %s''', (empleado,), False)[0]
        return tyc
