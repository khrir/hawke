from app.models.entities.event import Event
from sqlalchemy.exc import NoResultFound

class EventRepository:
    def __init__(self, ConnectionHandler) -> None:
        self.__ConnectionHandler = ConnectionHandler

    def list(self):
        with self.__ConnectionHandler() as db:
            try:
                events = db.session.query(Event).all()
                rows = [event.serialize() for event in events]
                return rows
            except NoResultFound:
                return []

    def get_organizer_events(self, organizer_id):
        with self.__ConnectionHandler() as db:
            try:
                events = db.session.query(Event).filter(Event.organizer_id == organizer_id).all()
                rows = [event.serialize() for event in events]
                return rows
            except NoResultFound:
                return []

    def select_by_id(self, event_id):
        with self.__ConnectionHandler() as db:
            try:
                event = db.session.query(Event).filter(Event.id == event_id).first()

                if event is not None:
                    return event.serialize()
                
                return event
            except NoResultFound:
                return []
            
    def select_by_slug(self, slug):
        with self.__ConnectionHandler() as db:
            try:
                event = db.session.query(Event).filter(Event.slug == slug).first()
                return event
            except NoResultFound:
                return
        
    def insert(self, event):
        with self.__ConnectionHandler() as db:
            try:
                db.session.add(event)
                db.session.commit()
                return event, None
            except Exception as e:
                db.session.rollback()
                raise e
        
    def update(self, event):
        with self.__ConnectionHandler() as db:
            try:
                db.session.merge(event)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
        
    def delete(self, event):
        with self.__ConnectionHandler() as db:
            try:
                db.session.delete(event)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

    def get_next_id(self):
        with self.__ConnectionHandler() as db:
            try:
                last_event = db.session.query(Event).order_by(Event.id.desc()).first()
                if last_event is None:
                    return 1
                return last_event.id + 1
            except NoResultFound:
                return 1