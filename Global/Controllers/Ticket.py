from flask import request
from Global.Classes.Ticket import Ticket


def create_ticket():
    try:
        params = {'empresa': request.json.get('empresa'),
                  'tipo_usuario': request.json.get('tipo_usuario'),
                  'tipo_ticket': request.json.get('tipo_ticket'),
                  'asunto': request.json.get('asunto'),
                  'descripcion': request.json.get('descripcion'),
                  'tipo_contacto': request.json.get('tipo_contacto'),
                  'contacto': request.json.get('contacto')}
        ticket = Ticket(params,False)
        return f'Ticket creado con el id: {ticket.id[0]}', 200
    except Exception as e:
        return {'error': str(e)}, 400

def obtener_tickets():
    try:
        params = {'tipo_ticket': request.args.get('tipo_ticket'),
                  'tipo_usuario': request.args.get('tipo_usuario')}
        return Ticket.obtener_tickets(params), 200
    except Exception as e:
        return {'error': str(e)}, 400
