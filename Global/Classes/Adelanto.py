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

    @classmethod
    def exist(cls,adelanto):
        exist = get('''SELECT * FROM adelantos WHERE id = %s''', (adelanto,),False)
        if exist:
            return exist
        else:
            raise Exception('No hay adelantos con el id proporcionado')

    def create(self, params):
        self.monto = params["monto"]
        rfc = get('''SELECT rfc FROM empleados WHERE celular = %s''',(params["celular"],), False)[0]
        self.id = post('''INSERT INTO adelantos(monto,estatus_adelanto) VALUES (%s,'creado') RETURNING id''', (self.monto,), True)[0]
        post('''INSERT INTO empleados_adelantos(empleado,adelanto) VALUES (%s,%s)''', (rfc, self.id), False)

    def load(self):
        pass

    @classmethod
    def cancelar_solicitud(cls, params):
        adelanto = cls.exist(params["id"])
        if adelanto[3] == 'cancelado':
            raise Exception('La solicitud ya había sido cancelada')
        else:
            post('''UPDATE adelantos SET estatus_adelanto = 'cancelado' WHERE id = %s''', (adelanto[0],), False)
            return f'Solicitud cancelada exitosamente'

    @classmethod
    def obtener_solicitudes(cls, params):
        monto = params["monto"]
        estatus_adelanto = params["estatus_adelanto"]
        solicitudes = []

        if monto == 'todos' and estatus_adelanto == 'todos':
            registros_adelanto = get('''SELECT * FROM adelantos ORDER BY fecha DESC''', (), True)
        elif monto != 'todos' and estatus_adelanto == 'todos':
            registros_adelanto = get('''SELECT * FROM adelantos WHERE monto = %s ORDER BY fecha DESC''', (monto,), True)
        elif monto == 'todos' and estatus_adelanto != 'todos':
            registros_adelanto = get('''SELECT * FROM adelantos WHERE estatus_adelanto = %s ORDER BY fecha DESC''', (estatus_adelanto,), True)
        else:
            registros_adelanto = get('''SELECT * FROM adelantos WHERE estatus_adelanto = %s AND monto = %s ORDER BY fecha DESC''',
                                     (estatus_adelanto, monto), True)
        for i in range(len(registros_adelanto)):
            empleado = get('''SELECT empleado FROM empleados_adelantos WHERE adelanto = %s ''', (registros_adelanto[i][0],), False)[0]
            datos_empleado = get('''SELECT id, nombre FROM empleados WHERE rfc = %s''', (empleado,),False)

            solicitudes.append({'id_adelanto': registros_adelanto[i][0], 'monto': registros_adelanto[i][1],
                                'fecha': registros_adelanto[i][2].strftime("%d/%m/%Y"), 'estatus_adelanto': registros_adelanto[i][3],
                                'id_empleado': datos_empleado[0], 'nombre_empleado': datos_empleado[1]})

        return solicitudes
