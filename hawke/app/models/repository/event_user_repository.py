from sqlalchemy import text
from app.models.entities.event_user import EventUser
from sqlalchemy.exc import NoResultFound

class EventUserRepository:
    def __init__(self, ConnectionHandler) -> None:
        self.__ConnectionHandler = ConnectionHandler

    def list(self):
        with self.__ConnectionHandler() as db:
            try:
                event_users = db.session.query(EventUser).all()
                rows = [event_user.serialize() for event_user in event_users]
                return rows
            except NoResultFound:
                return []
        
    def select_by_id(self, event_user_id):
        with self.__ConnectionHandler() as db:
            try:
                return db.session.query(EventUser).filter(EventUser.id == event_user_id).first()
            except NoResultFound:
                return []
    
    def select_by_user_id(self, user_id):
        with self.__ConnectionHandler() as db:
            try:
                return db.session.query(EventUser).filter(EventUser.user_id == user_id).first()
            except NoResultFound:
                return []

    def select_by_email(self, email):
        with self.__ConnectionHandler() as db:
            try:
                user = db.session.query(EventUser).filter(EventUser.email == email).first()
                if user is not None:
                    return user.serialize()
                return user
            except NoResultFound:
                return []
        
    def insert(self, event_user):
        with self.__ConnectionHandler() as db:
            try:
                db.session.add(event_user)
                db.session.commit()
                return event_user.serialize()
            except Exception as e:
                db.session.rollback()
                raise e
        
    def update(self, event_user):
        with self.__ConnectionHandler() as db:
            try:
                db.session.merge(event_user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
        
    def delete(self, event_user):
        with self.__ConnectionHandler() as db:
            try:
                db.session.delete(event_user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
            
    def get_user_events(self, user_id):
        with self.__ConnectionHandler() as db:
            try:
                event_users = db.session.query(EventUser).filter(EventUser.user_id == user_id).all()
                rows = [event_user.serialize() for event_user in event_users]
                return rows
            except NoResultFound:
                return []
            
    def get_event_users(self, event_id):
        with self.__ConnectionHandler() as db:
            try:
                event_users = db.session.query(EventUser).filter(EventUser.event_id == event_id).all()
                rows = [event_user.serialize() for event_user in event_users]
                return rows
            except NoResultFound:
                return []
            
    # CRUD operations for the User entity with raw SQL
    def list_raw(self):
        with self.__ConnectionHandler() as db:
            try:
                users = db.session.execute('SELECT * FROM event_users').fetchall()
                rows = [dict(user) for user in users]
                return rows
            except NoResultFound:
                return []
    
    def select_by_id_raw(self, user_id):
        with self.__ConnectionHandler() as db:
            try:
                user = db.session.execute(f'SELECT * FROM event_users WHERE id = {user_id}').first()
                return dict(user)
            except NoResultFound:
                return []
            
    def insert_raw(self, event_user):
        with self.__ConnectionHandler() as db:
            try:
                db.session.execute(f"INSERT INTO event_users (event_id, user_id) VALUES ({event_user.event_id}, {event_user.user_id})")
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
    
    def update_raw(self, event_user):
        with self.__ConnectionHandler() as db:
            try:
                db.session.execute(f"UPDATE event_users SET event_id = {event_user.event_id}, user_id = {event_user.user_id} WHERE id = {event_user.id}")
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
    
    def delete_raw(self, event_user):
        with self.__ConnectionHandler() as db:
            try:
                db.session.execute(f"DELETE FROM event_users WHERE id = {event_user.id}")
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
    
    def get_user_events_raw(self, user_id):
        with self.__ConnectionHandler() as db:
            try:
                event_users = db.session.execute(f'SELECT * FROM event_users WHERE user_id = {user_id}').fetchall()
                rows = [dict(event_user) for event_user in event_users]
                return rows
            except NoResultFound:
                return []
            
    def get_subscriptions(self, event_id):
        with self.__ConnectionHandler() as db:
            try:
                sql = text("""
                    SELECT 
                        sub.id AS subscription_id, 
                        u.username AS username, 
                        u.email AS email 
                    FROM users u
                    LEFT JOIN event_users sub ON u.id = sub.user_id
                    WHERE sub.event_id = :event_id
                """)
                
                users = db.session.execute(sql, {"event_id": event_id}).fetchall()
                return [
                    {"subscription_id": row[0], "username": row[1], "email": row[2]}
                    for row in users
                ]
            except NoResultFound:
                return []