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

        self.id = get('''INSERT INTO tickets(empresa,tipo_usuario,tipo_ticket,asunto,descripcion,tipo_contacto,contacto)
        VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id''', (self.empresa, self.tipo_usuario, self.tipo_ticket,
                                                        self.asunto, self.descripcion, self.tipo_contacto, self.contacto), True)[0]

    def load(self, params):
        self.id = params["id"]
        self.empresa, self.tipo_usuario, self.tipo_ticket, self.asunto, self.descripcion, self.tipo_contacto, self.contacto = get(
            '''SELECT empresa,tipo_usuario,tipo_ticket,asunto,descripcion,tipo_contacto,contacto FROM tickets WHERE id = %s''', (self.id,), False)




