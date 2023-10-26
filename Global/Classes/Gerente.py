from Global.Utils.db import post, get
from json import load
import hashlib
import jwt
import os
import datetime

class Gerente:

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
        exist = get('''SELECT * FROM gerentes WHERE username = %s''',(params['username'],),False)
        if exist:
            return exist
        else:
            return False

    def create(self, params):
        if self.exist(params):
            raise Exception('El gerente ya habia sido registrado')
        exist_operador = get('''SELECT id FROM operadores WHERE username = %s''',(params['username'],),False)
        if exist_operador:
            raise Exception('Ya existe ese usuario en la base de datos')
        else:
            self.nombre = params['nombre']
            self.username = params['username'].rstrip()
            self.empresa = 1
            h = hashlib.sha256(params['password'].encode('utf-8')).hexdigest()
            self.password = h
            self.id = post('''INSERT INTO gerentes (username,nombre,password,empresa) VALUES (%s,%s,%s,%s) RETURNING 
            id''',(self.username,self.nombre,self.password,self.empresa), True)[0]
            post('''INSERT INTO gerentes_empresas(gerente,empresa) VALUES (%s,%s)''', (self.id, self.empresa), False)

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
    def obtener_bancos(cls, params):
        bancos = []
        if params["reverse"] == "true":
            registros = get('''SELECT * FROM bancos ORDER BY bancos DESC''', (), True)
        elif params["reverse"] == "false":
            registros = get('''SELECT * FROM bancos ORDER BY bancos ASC''', (), True)
        else:
            raise Exception('reverse sólo puede ser "true" o "false"')
        if not registros:
            raise Exception('No hay registros en la base de datos')

        for i in range(len(registros)):
            bancos.append({'id': registros[i][0], 'nombre': registros[i][1]})

        return bancos

    @classmethod
    def generar_reporte(cls, params):
        headers = ["# Contrato", "Banco", "Comision Bancaria", "Empresa", "Fecha Deposito", "Fecha Solicitud",
                   "Gastos Adm. Interes", "IVA", "Nombre Empleado", "Numero Cuenta", "RFC", "Solicitado",
                   "Sub. Total", "Transferencia"]
        solicitudes = []
        primero = True
        query = '''select t3.nombre as nombre_empleado, t3.rfc, em.nombre as nombre_empresa, t3.id_adelanto, 
        t3.fecha, t3.fecha_pago,  t3.numero_cuenta, t3.nombre_banco, t3.monto from ( select t2.*, b.nombre as nombre_banco from ( select 
        t1.nombre, t1.rfc, t1.numero_cuenta, t1.banco, t1.empresa, a.id as id_adelanto, a.monto, a.fecha, a.fecha_pago from 
        adelantos a inner join (select e.id, e.nombre,e.rfc,e.numero_cuenta,e.banco,e.empresa, ea.adelanto from 
        empleados e inner join empleados_adelantos ea on e.id = ea.empleado) t1 on a.id = t1.adelanto) t2 inner join 
        bancos b on b.id = t2.banco) t3 inner join empresas em on em.id = t3.empresa '''

        if params["empresas"]:
            empresas = "','".join(params["empresas"])
            query += f"where em.nombre in ('{empresas}')"
            primero = False

        if params["montos"]:
            montos = ",".join(params["montos"])
            if primero:
                query += f"where t3.monto in ({montos})"
                primero = False
            elif not primero:
                query += f"and t3.monto in ({montos})"

        if params["bancos"]:
            bancos = "','".join(params["bancos"])
            if primero:
                query += f"where t3.nombre_banco in ('{bancos}')"
                primero = False
            elif not primero:
                query += f"and t3.nombre_banco in ('{bancos}')"

        if params["fechas"]:
            fecha_inicio = params["fechas"][0]
            fecha_fin = params["fechas"][1]
            if primero:
                query += f"where TO_CHAR(t3.fecha,'DD/MM/YYYY')  between '{fecha_inicio}' and '{fecha_fin}' "
            elif not primero:
                query += f"and TO_CHAR(t3.fecha,'DD/MM/YYYY')  between '{fecha_inicio}' and '{fecha_fin}' "

        query += f"order by t3.fecha desc"

        registro = get(query, (), True)
        print(registro)
        for i in range(len(registro)):
            comisiones = cls.calcular_comisiones(registro[i][8])
            solicitudes.append({"empleado": registro[i][0], "rfc": registro[i][1], "empresa": registro[i][2],
                                "id_adelanto": registro[i][3], "fecha": registro[i][4], "fecha_pago": registro[i][5],
                                "numero_cuenta": registro[i][6], "nombre_banco": registro[i][7],
                                "solicitado": f'${comisiones[0]}', "gastos_admin": comisiones[1],
                                "comision_bancaria": comisiones[2], "subtotal": comisiones[3], "iva": comisiones[4],
                                "transferencia": comisiones[5]})

        return {"DatosTabla": solicitudes, "DatosCsv": {"headers": headers, "data": solicitudes}}
    @classmethod
    def calcular_comisiones(cls, monto):
        solicitado = round(monto, 2)
        comision_bancaria = 5.80
        if solicitado == 1000.00:
            gastos_admin = 60.00
        elif solicitado == 500.00:
            gastos_admin = 40.00
        else:
            gastos_admin = 0.00
        subtotal = round(gastos_admin + comision_bancaria, 2)
        iva = round(subtotal*0.16, 2)
        transferecia = round(solicitado-(subtotal+iva),2)
        comisiones = [solicitado, gastos_admin, comision_bancaria, subtotal, iva, transferecia]
        return comisiones