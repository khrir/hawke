from app.models.entities.activity import Activity
from sqlalchemy.exc import NoResultFound

class ActivityRepository:
    def __init__(self, ConnectionHandler) -> None:
        self.__ConnectionHandler = ConnectionHandler

    def list(self):
        with self.__ConnectionHandler() as db:
            try:
                activities = db.session.query(Activity).all()
                rows = [activity.serialize() for activity in activities]
                return rows
            except NoResultFound:
                return []
        
    def select_by_id(self, activity_id):
        with self.__ConnectionHandler() as db:
            try:
                activity = db.session.query(Activity).filter(Activity.id == activity_id).first()

                if activity is not None:
                    return activity.serialize()
                
                return activity
            except NoResultFound:
                return []
        
    def insert(self, activity):
        with self.__ConnectionHandler() as db:
            try:
                db.session.add(activity)
                db.session.commit()
                return activity, None
            except Exception as e:
                db.session.rollback()
                raise e
        
    def update(self, activity):
        with self.__ConnectionHandler() as db:
            try:
                db.session.merge(activity)
                db.session.commit()
                return activity, None
            except Exception as e:
                db.session.rollback()
                raise e
        
    def delete(self, activity):
        with self.__ConnectionHandler() as db:
            try:
                db.session.delete(activity)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
            
    def select_event_activities(self, event_id):
        with self.__ConnectionHandler() as db:
            try:
                activities = db.session.query(Activity).filter(Activity.event_id == event_id).all()
                if activities is not None:
                    rows = [activity.serialize() for activity in activities]
                    return rows
                return activities
            except NoResultFound:
                return []