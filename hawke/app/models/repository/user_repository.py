from app.models.entities.user import User
from sqlalchemy.exc import NoResultFound

class UserRepository:
    def __init__(self, ConnectionHandler) -> None:
        self.__ConnectionHandler = ConnectionHandler

    def list(self):
        with self.__ConnectionHandler() as db:
            try:
                users = db.session.query(User).all()
                rows = [user.serialize() for user in users]
                return rows
            except NoResultFound:
                return []
        
    def select_by_id(self, user_id):
        with self.__ConnectionHandler() as db:
            try:
                return db.session.query(User).filter(User.id == user_id).first()
            except NoResultFound:
                return []

    def select_by_email(self, email):
        with self.__ConnectionHandler() as db:
            try:
                user = db.session.query(User).filter(User.email == email).first()
                
                if user is not None:
                    return user.serialize()
                
                return user
            except NoResultFound:
                return []

    def insert_speaker(self, data):
        with self.__ConnectionHandler() as db:
            try:
                user = self.insert(data)
                return user
            except Exception as e:
                db.session.rollback()
                raise e

    def authenticate(self, email, password):
        with self.__ConnectionHandler() as db:
            try:
                user = db.session.query(User).filter(User.email == email, User.password == password).first()
                
                if user is not None:
                    return user.serialize()
                
                return user
            except NoResultFound:
                return []

    def insert(self, user):        
        with self.__ConnectionHandler() as db:
            try:
                db.session.add(user)
                db.session.commit()
                return user.serialize()
            except Exception as e:
                db.session.rollback()
                raise e

    def update(self, user):
        with self.__ConnectionHandler() as db:
            try:
                db.session.merge(user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
        
    def delete(self, user):
        with self.__ConnectionHandler() as db:
            try:
                db.session.delete(user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e