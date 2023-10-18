from Global.Utils.db import post, get
from json import load


class Ticket:

    def __init__(self, params, load=True):

        self.id = None
        self.empresa = None
        self.tipo_usuario = None
        self.tipo_ticket = None
        self.asunto = None
        self.descripcion = None
        self.tipo_contacto = None
        self.contacto = None
        self.fecha = None
        self.load(params) if load else self.create(params)

    @classmethod
    def obtain_empresa(cls):
        pass

    def create(self, params):
        self.empresa = params["empresa"]
        self.tipo_usuario = params["tipo_usuario"]
        self.tipo_ticket = params["tipo_ticket"]
        self.asunto = params["asunto"]
        self.descripcion = params["descripcion"]
        self.tipo_contacto = params["tipo_contacto"]
        self.contacto = params["contacto"]

        self.id = post('''INSERT INTO tickets(tipo_usuario,tipo_ticket,asunto,descripcion,tipo_contacto,contacto)
        VALUES (%s,%s,%s,%s,%s,%s) RETURNING id''', (self.tipo_usuario, self.tipo_ticket,
                                                     self.asunto, self.descripcion, self.tipo_contacto, self.contacto),True)

    def load(self, params):
        self.id = params["id"]
        self.empresa, self.tipo_usuario, self.tipo_ticket, self.asunto, self.descripcion, self.tipo_contacto, self.contacto = get(
            '''SELECT empresa,tipo_usuario,tipo_ticket,asunto,descripcion,tipo_contacto,contacto FROM tickets WHERE id = %s''',
            (self.id,), False)

    @classmethod
    def obtener_tickets(cls, params):
        tipo_ticket = params["tipo_ticket"]
        tipo_usuario = params["tipo_usuario"]
        tickets = []
        headers = ["Asunto", "Contacto", "Descripción", "Fecha", "ID de ticket", "Forma de contacto", "Tipo de ticket",
                   "Tipo de usuario"]
        if tipo_ticket == 'todos' and tipo_usuario == 'todos':
            registros = get('''SELECT * FROM tickets ORDER BY fecha DESC''', (), True)
        elif tipo_ticket != 'todos' and tipo_usuario == 'todos':
            registros = get('''SELECT * FROM tickets WHERE tipo_ticket = %s ORDER BY fecha DESC''', (tipo_ticket,),
                            True)
        elif tipo_ticket == 'todos' and tipo_usuario != 'todos':
            registros = get('''SELECT * FROM tickets WHERE tipo_usuario = %s ORDER BY fecha DESC''', (tipo_usuario,),
                            True)
        elif tipo_ticket != 'todos' and tipo_usuario != 'todos':
            registros = get(
                '''SELECT * FROM tickets WHERE tipo_usuario = %s and tipo_ticket = %s ORDER BY fecha DESC''',
                (tipo_usuario, tipo_ticket), True)

        if not registros:
            raise Exception('No hay registros en la base de datos')

        for i in range(len(registros)):
            tickets.append({'id': registros[i][0], 'tipo_usuario': registros[i][1], 'tipo_ticket': registros[i][2],
                            'asunto': registros[i][3], 'descripcion': registros[i][4], 'tipo_contacto': registros[i][5],
                            'contacto': registros[i][6],'fecha': registros[i][7].strftime("%d/%m/%Y")})
        return {"DatosTabla": tickets, "DatosCsv": {"headers": headers, "data": tickets}}
