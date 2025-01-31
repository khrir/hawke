from app.models.entities.event_address import EventAddress as Address
from sqlalchemy.exc import NoResultFound

class EventAddressRepository:
    def __init__(self, ConnectionHandler) -> None:
        self.__ConnectionHandler = ConnectionHandler

    def list(self):
        with self.__ConnectionHandler() as db:
            try:
                addresses = db.session.query(Address).all()
                rows = [address.serialize() for address in addresses]
                return rows
            except NoResultFound:
                return []
    
    def select_by_id(self, id):
        with self.__ConnectionHandler() as db:
            try:
                address = db.session.query(Address).filter(Address.id == id).first()
                if address is not None:
                    return address.serialize()
                
                return address
            except NoResultFound:
                return []
        
    def insert(self, address):
        with self.__ConnectionHandler() as db:
            try:
                db.session.add(address)
                db.session.commit()
                return address, None
            except Exception as e:
                db.session.rollback()
                raise e
        
    def update(self, address):
        with self.__ConnectionHandler() as db:
            try:
                db.session.merge(address)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
        
    def delete(self, address):
        with self.__ConnectionHandler() as db:
            try:
                db.session.delete(address)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
             
    def get_event_addresses(self, event_id):
        with self.__ConnectionHandler() as db:
            try:
                addresses = db.session.query(Address).filter(Address.event_id == event_id).all()
                rows = [address.serialize() for address in addresses]
                return rows
            except NoResultFound:
                return []