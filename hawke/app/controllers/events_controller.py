from app.models.entities.event import Event
from app.models.entities.event_address import EventAddress as Address
from app.models.repository.event_repository import EventRepository
from app.models.repository.event_address_repository import EventAddressRepository as AddressRepository
from infra.configs.connection import DBConnectionHandler

class EventsController:
    def __init__(self):
        self.__event_repository = EventRepository(DBConnectionHandler)
        self.__address_repository = AddressRepository(DBConnectionHandler)

    def list(self):
        return self.__event_repository.list()
    
    def list_organizer_events(self, organizer_id):
        return self.__event_repository.get_organizer_events(organizer_id)
    
    def list_event_activities(self, event_id):
        return self.__event_repository.select_event_activities(event_id)

    def select(self, id):
        event = self.__event_repository.select_by_id(id)
        if event is None:
            return {'success': False, 'errors': {'event': 'Evento não encontrado'}}, 404
        return {'success': True, 'event': event}, 200
    
    def create(self, data, organizer_id):
        id = self.__event_repository.get_next_id()
        name = data.get('name')
        slug = self.__generate_slug(name, id)

        event = dict(name=name, description=data.get('description'), start_date=data.get('start_date'), end_date=data.get('end_date'), slug=slug, organizer_id=organizer_id)
        event = self.__validate_event(event)
        _, err = self.__event_repository.insert(event)
        if err is not None:
            return {'success': False, 'errors': {'event': {err}}}, 400
        
        address = dict(zip_code=data.get('zip_code'), local=data.get('local'), neighborhood=data.get('neighborhood'), city=data.get('city'), state=data.get('state'), event_id=id)
        address = self.__validate_address(address)
        _, err = self.__address_repository.insert(address)
        if err is not None:
            return {'success': False, 'errors': {'address': {err}}}, 400
        
        return {'success': True}, 201
    
    def update(self, id, data):
        event = self.__event_repository.select_by_id(id)
        if event is None:
            return {'success': False, 'errors': {'event': 'Evento não encontrado'}}, 404
        
        name = data.get('name')
        slug = self.__generate_slug(name, id)

        event = dict(name=name, description=data.get('description'), start_date=data.get('start_date'), end_date=data.get('end_date'), slug=slug)
        event = self.__validate_event(event)
        _, err = self.__event_repository.update(event)
        if err is not None:
            return {'success': False, 'errors': {'event': {err}}}, 400
        
        address = dict(zip_code=data.get('zip_code'), local=data.get('local'), neighborhood=data.get('neighborhood'), city=data.get('city'), state=data.get('state'), event_id=id)
        address = self.__validate_address(address)
        _, err = self.__address_repository.update(address)
        if err is not None:
            return {'success': False, 'errors': {'address': {err}}}, 400
        
        return {'success': True}, 200

    def select_by_slug(self, slug):
        event = self.__event_repository.select_by_slug(slug)
        if event is None:
            return {'success': False, 'errors': {'event': 'Evento não encontrado'}}, 404
        return {'success': True, 'event': event.serialize_full()}, 200
    
    def __generate_slug(self, title, id) -> str | None:
        slug = title.lower().replace(' ', '-')

        res = self.__event_repository.select_by_slug(slug)
        if res is not None:
            slug = f"{slug}-{id}"

        return slug
    
    def __validate_address(self, address) -> Address:
        if address is None:
            return {'success': False, 'errors': {'address': 'Endereço vazio'}}, 400
        
        if address.get('zip_code') is None or address.get('zip_code') == "" or not isinstance(address.get('zip_code'), str):
            return {'success': False, 'errors': {'cep': 'Informe o CEP'}}, 400

        if address.get('local') is None or address.get('local') == "" or not isinstance(address.get('local'), str):
            return {'success': False, 'errors': {'local': 'Informe o local'}}, 400

        if address.get('neighborhood') is None or address.get('neighborhood') == "" or not isinstance(address.get('neighborhood'), str):
            return {'success': False, 'errors': {'neighborhood': 'Informe o bairro'}}, 400

        if address.get('city') is None or address.get('city') == "" or not isinstance(address.get('city'), str):
            return {'success': False, 'errors': {'city': 'Informe a cidade'}}, 400

        if address.get('state') is None or address.get('state') == "" or not isinstance(address.get('state'), str):
            return {'success': False, 'errors': {'state': 'Informe o estado'}}, 400

        return Address(zip_code=address.get('zip_code'), local=address.get('local'), neighborhood=address.get('neighborhood'), city=address.get('city'), state=address.get('state'), event_id=address.get('event_id'))

    def __validate_event(self, event) -> Event:
        if event is None:
            return {'success': False, 'errors': {'event': 'Evento vazio'}}, 400
        
        if event.get('name') is None or event.get('name') == "" or not isinstance(event.get('name'), str):
            return {'success': False, 'errors': {'name': 'Informe o nome do evento'}}, 400

        if event.get('description') is None or event.get('description') == "" or not isinstance(event.get('description'), str):
            return {'success': False, 'errors': {'description': 'Informe a descrição do evento'}}, 400

        if event.get('start_date') is None or event.get('start_date') == "" or not isinstance(event.get('start_date'), str):
            return {'success': False, 'errors': {'start_date': 'Informe a data de início do evento'}}, 400

        if event.get('end_date') is None or event.get('end_date') == "" or not isinstance(event.get('end_date'), str):
            return {'success': False, 'errors': {'end_date': 'Informe a data de término do evento'}}, 400

        return Event(name=event.get('name'), description=event.get('description'), start_date=event.get('start_date'), end_date=event.get('end_date'), slug=event.get('slug'), organizer_id=event.get('organizer_id'))