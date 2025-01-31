from app.models.entities.activity import Activity
from app.models.repository.activity_repository import ActivityRepository
from app.controllers.users_controller import UsersController
from infra.configs.connection import DBConnectionHandler

class ActivitiesController:
    def __init__(self):
        self.__activity_repository = ActivityRepository(DBConnectionHandler)
        self.__user_controller = UsersController()

    def list(self):
        return self.__activity_repository.list()

    def create(self, data):
        name = data.get('name')
        description = data.get('description')
        date = data.get('start_date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        price = data.get('price')
        event_id = data.get('event_id')

        speaker_email = data.get('speaker_email')
        speaker_id = self.__user_controller.validate_speaker(speaker_email).get('id')

        activity = dict(name=name, description=description, date=date, start_time=start_time, end_time=end_time, price=price, event_id=event_id, speaker_id=speaker_id)
        activity = self.__validate_activity(activity)
        _, err = self.__activity_repository.insert(activity)
        if err is not None:
            return {'success': False, 'errors': {'activity': {err}}}, 400
        
        return {'success': True}, 201
    
    def update(self, id, data):
        print(id)
        activity = self.__activity_repository.select_by_id(id)
        if activity is None:
            return {'success': False, 'errors': {'activity': 'Atividade não encontrada'}}, 404
        
        name = data.get('name')
        description = data.get('description')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        price = data.get('price')
        event_id = data.get('event_id')
        speaker_id = data.get('speaker_id')

        activity = dict(name=name, description=description, start_date=start_date, end_date=end_date, start_time=start_time, end_time=end_time, price=price, event_id=event_id, speaker_id=speaker_id)
        activity = self.__validate_activity(activity)
        _, err = self.__activity_repository.update(activity)
        if err is not None:
            return {'success': False, 'errors': {'activity': {err}}}, 400

        return {'success': True}, 200

    def list_by_event(self, event_id):
        activities = self.__activity_repository.select_event_activities(event_id)
        if activities is None:
            return {'success': False, 'errors': {'activities': 'Atividades não encontradas'}}, 404
        return {'success': True, 'activities': activities}, 200

    def __validate_activity(self, activity) -> Activity:
        if activity is None:
            return {'success': False, 'errors': {'activity': 'Atividade vazia'}}, 400
        
        if activity.get('name') is None or activity.get('name') == "" or not isinstance(activity.get('name'), str):
            return {'success': False, 'errors': {'name': 'Informe o nome da atividade'}}, 400

        if activity.get('start_date') is None or activity.get('date') == "" or not isinstance(activity.get('date'), str):
            return {'success': False, 'errors': {'start_date': 'Informe a data de início'}}, 400


        return Activity(name=activity.get('name'), description=activity.get('description'), start_date=activity.get('start_date'), end_date=activity.get('end_date'), start_time=activity.get('start_time'), end_time=activity.get('end_time'), price=activity.get('price'), event_id=activity.get('event_id'), speaker_id=activity.get('speaker_id'))