from Global.Utils.db import post, get
from json import load
import datetime

class Adelanto:

    def __init__(self, params, load=True):
        self.id = None
        self.monto = None
        self.fecha = None
        self.estatus = None
        self.load(params) if load else self.create(params)

    @classmethod
    def validate_adelanto(cls, params):
        # Cambiar si hay mas empresas
        id_empleado = get('''SELECT id FROM empleados WHERE celular = %s''', (params["celular"],), False)[0]

        # obtenemos los ultimos dos adelantos para verificar que no se exceda el monto semanal maximo
        adelantos = get('''SELECT adelanto FROM empleados_adelantos WHERE empleado = %s ORDER BY adelanto DESC LIMIT 
        2''', (id_empleado,), True)
        # si no hay adelantos, entonces se autoriza en automatico
        if not adelantos:
            return 'autorizado'
        # si solo hay un adelanto, verificamos que sea menor a 1000 para autorizarlo
        elif len(adelantos) < 2:
            ultimo_monto = get('''SELECT monto FROM adelantos WHERE id = %s''', (adelantos[0][0],), False)[0]
            if ultimo_monto >= 1000:
                return 'rechazado'
            elif ultimo_monto + params["monto"] >= 1000:
                return 'rechazado'
            else:
                return 'autorizado'

        dates = get('''SELECT fecha FROM adelantos WHERE (id = %s) OR (id = %s)''', (adelantos[0][0], adelantos[1][0]), True)
        ultimo_periodo = Adelanto.obtener_periodo(dates[0][0])
        penultimo_periodo = Adelanto.obtener_periodo(dates[1][0])

        # si los periodos son iguales, se rechaza en automatico
        if ultimo_periodo == penultimo_periodo:
            return 'rechazado'
        else:
            ultimo_monto = get('''SELECT monto FROM adelantos WHERE id = %s''', (adelantos[0][0],), False)[0]
            if ultimo_monto >= 1000:
                return 'rechazado'
            else:
                print(params["monto"], ultimo_monto)
                # verificamos que el monto solicitado mas el ultimo monto no excedan la cantidad maxima
                if params["monto"] + ultimo_monto >= 1000:
                    return 'rechazado'
                else:
                    return 'autorizado'


    @classmethod
    def obtener_periodo(cls, date):
        siguiente_periodo = False
        num_semana = int(date.strftime('%U'))
        dia_semana = date.weekday()
        hora_dia = date.hour
        minutos_hora = date.minute

        # si es viernes, verificamos que sea antes de las 11:30, si no entonces se considera como el siguiente periodo
        if dia_semana > 4:
            siguiente_periodo = True
        elif dia_semana == 4:
            if hora_dia == 11 and minutos_hora >= 30:
                siguiente_periodo = True
            elif hora_dia > 11:
                siguiente_periodo = True

        # si es la ultima semana del año y se considera como siguiente periodo, entonces regresamos periodo 1
        if num_semana == 52 and siguiente_periodo:
            return 1
        elif num_semana != 52 and siguiente_periodo:

            return num_semana+1
        else:
            return num_semana

    @classmethod
    def exist(cls,adelanto):
        exist = get('''SELECT * FROM adelantos WHERE id = %s''', (adelanto,),False)
        if exist:
            return exist
        else:
            raise Exception('No hay adelantos con el id proporcionado')

    def create(self, params):
        self.monto = params["monto"]
        empleado = get('''SELECT id FROM empleados WHERE celular = %s''',(params["celular"],), False)[0]
        self.id = post('''INSERT INTO adelantos(monto,estatus_adelanto) VALUES (%s,'creado') RETURNING id''', (self.monto,), True)[0]
        post('''INSERT INTO empleados_adelantos(empleado,adelanto) VALUES (%s,%s)''', (empleado, self.id), False)

    def load(self, params):
        self.id = params["id"]
        if self.exist(self.id):
            self.monto, self.fecha, self.estatus = get('''SELECT monto,fecha,estatus_adelanto FROM adelantos WHERE id = 
            %s''', (self.id,), False)
            return self


    @classmethod
    def cancelar_solicitud(cls, params):
        adelanto = cls.exist(params["id"])
        if adelanto[3] == 'cancelado':
            raise Exception('La solicitud ya había sido cancelada')
        else:
            post('''UPDATE adelantos SET estatus_adelanto = 'cancelado' WHERE id = %s''', (adelanto[0],), False)
            return {"message":'Solicitud cancelada exitosamente'}

    @classmethod
    def obtener_adelantos(cls, params):
        monto = params["monto"]
        estatus_adelanto = params["estatus_adelanto"]
        solicitudes = []
        headers = ["Estatus", "Fecha", "Folio", "ID del usuario", "Monto", "Nombre", "RFC"]

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
            datos_empleado = get('''SELECT id, nombre, rfc FROM empleados WHERE id = %s''', (empleado,),False)
            solicitudes.append({'id_adelanto': registros_adelanto[i][0], 'monto': registros_adelanto[i][1],
                                'fecha': registros_adelanto[i][2].strftime("%d/%m/%Y"), 'estatus_adelanto': registros_adelanto[i][3],
                                'id_empleado': datos_empleado[0], 'nombre_empleado': datos_empleado[1], 'rfc': datos_empleado[2]})

        return {"DatosTabla": solicitudes, "DatosCsv": {"headers": headers, "data": solicitudes}}

    @classmethod
    def pagar_adelanto(cls, params):
        adelanto = cls.exist(params["id"])
        if not adelanto:
            raise Exception('No hay adelantos con el id proporcionado')
        else:
            post('''UPDATE adelantos SET estatus_adelanto = 'pagado' WHERE id = %s''', (adelanto[0],), False)
            return 'Adelanto pagado exitosamente'

