from app.models.entities.event import Event
from app.models.entities.user import User
from app.models.entities.event_address import EventAddress
from app.models.entities.activity import Activity
from datetime import datetime


class EventBuilder:
    def __init__(self):
        self._event_data = {
            'name': None,
            'description': None,
            'start_date': None,
            'end_date': None,
            'slug': None,
            'status': 1,
            'organizer_id': None,
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
        }
        self._address = None
        self._activities = []
        self._user = None

    def with_name(self, name: str) -> 'EventBuilder':
        self._event_data['name'] = name
        return self

    def with_description(self, description: str) -> 'EventBuilder':
        self._event_data['description'] = description
        return self

    def with_start_date(self, start_date: str) -> 'EventBuilder':
        self._event_data['start_date'] = start_date
        return self

    def with_end_date(self, end_date: str) -> 'EventBuilder':
        self._event_data['end_date'] = end_date
        return self

    def with_slug(self, slug: str) -> 'EventBuilder':
        self._event_data['slug'] = slug
        return self

    def with_status(self, status: int) -> 'EventBuilder':
        self._event_data['status'] = status
        return self

    def with_organizer_id(self, organizer_id: int) -> 'EventBuilder':
        self._event_data['organizer_id'] = organizer_id
        return self

    def with_address(self, address: EventAddress) -> 'EventBuilder':
        self._address = address
        return self

    def add_activity(self, activity: Activity) -> 'EventBuilder':
        self._activities.append(activity)
        return self

    def build(self, data: dict, additional, organizer_id: int) -> Event:
        id = data.get('id')
        name = additional.get('name')
        slug =  additional.get('slug')

        event = (
            EventBuilder()
            .with_name(name)
            .with_description(data.get('description'))
            .with_start_date(data.get('start_date'))
            .with_end_date(data.get('end_date'))
            .with_slug(slug)
            .with_status(1)
            .with_organizer_id(organizer_id)
        )

        # Configurar o endereço no Builder
        address_data = dict(
            zip_code=data.get('zip_code'),
            local=data.get('local'),
            neighborhood=data.get('neighborhood'),
            city=data.get('city'),
            state=data.get('state'),
            event_id=id
        )
        address = EventAddress(**address_data)
        event = event.with_address(address)

        # Configurar as atividades, se houverem
        # activities_data = data.get('activities', [])
        # for activity_data in activities_data:
        #     activity = Activity(
        #         name=activity_data['name'],
        #         start_time=activity_data['start_time'],
        #         end_time=activity_data['end_time'],
        #     )
        #     builder = builder.add_activity(activity)

        return event


# _, err = self.__address_repository.insert(address)
#         if err is not None:
#             return {'success': False, 'errors': {'address': {err}}}, 400