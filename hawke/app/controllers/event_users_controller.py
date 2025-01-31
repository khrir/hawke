from app.models.repository.event_repository import EventRepository
from app.models.entities.user import User
from app.models.repository.user_repository import UserRepository
from app.models.entities.event_user import EventUser
from app.models.repository.event_user_repository import EventUserRepository
from infra.configs.connection import DBConnectionHandler
from infra.observers.email_observer import EmailObserver
from infra.observers.log_observer import LogObserver

class EventUsersController:
    def __init__(self):
        self.__event_repository = EventRepository(DBConnectionHandler)
        self.__event_user_repository = EventUserRepository(DBConnectionHandler)
        self.__user_repository = UserRepository(DBConnectionHandler)
        self.__observers = [EmailObserver(), LogObserver()]

    def __notify_observers(self, data):
        for observer in self.__observers:
            observer.update(data)

    def create(self, data):
        event_id = data.get('event_id')
        name = data.get('username')
        email = data.get('email')

        event = self.__event_repository.select_by_id(event_id)
        if event is None:
            return {'success': False, 'errors': {'event': 'Evento não encontrado'}}, 404

        user = self.__user_repository.select_by_email(email)
        if user is None:
            user = self.__user_repository.insert(User(username=name, email=email, password='Mudar123@'))

        event_user = self.__event_user_repository.select_by_user_id(user.get('id'))
        if event_user is not None:
            return {'success': False, 'errors': {'event_user': 'Usuário já cadastrado no evento'}}, 400
        
        event_user = EventUser(event_id=event_id, user_id=user.get('id'))
        event_user = self.__event_user_repository.insert(event_user)
        if event_user is None:
            return {'success': False, 'errors': {'event_user': 'Erro ao cadastrar usuário no evento'}}

        self.__notify_observers({"event": event, "user": user})

        return {'success': True}, 201
    
    def get_subscriptions(self, event_id):
        subs = self.__event_user_repository.get_subscriptions(event_id)

        return subs