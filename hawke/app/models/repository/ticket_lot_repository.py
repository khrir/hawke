from app.models.entities.ticket_lot import TicketLot
from sqlalchemy.exc import NoResultFound

class TicketLotRepository:
    def __init__(self, ConnectionHandler) -> None:
        self.__ConnectionHandler = ConnectionHandler

    def list(self):
        with self.__ConnectionHandler() as db:
            try:
                ticket_lots = db.session.query(TicketLot).all()
                rows = [ticket_lot.serialize() for ticket_lot in ticket_lots]
                return rows
            except NoResultFound:
                return []
        
    def select_by_id(self, ticket_lot_id):
        with self.__ConnectionHandler() as db:
            try:
                return db.session.query(TicketLot).filter(TicketLot.id == ticket_lot_id).first()
            except NoResultFound:
                return []

    def select_by_event_id(self, event_id):
        with self.__ConnectionHandler() as db:
            try:
                ticket_lots = db.session.query(TicketLot).filter(TicketLot.event_id == event_id).all()
                rows = [ticket_lot.serialize() for ticket_lot in ticket_lots]
                return rows
            except NoResultFound:
                return

    def insert(self, ticket_lot):
        with self.__ConnectionHandler() as db:
            try:
                db.session.add(ticket_lot)
                db.session.commit()
                return ticket_lot
            except Exception as e:
                db.session.rollback()
                raise e
        
    def update(self, ticket_lot):
        with self.__ConnectionHandler() as db:
            try:
                db.session.merge(ticket_lot)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
        
    def delete(self, ticket_lot):
        with self.__ConnectionHandler() as db:
            try:
                db.session.delete(ticket_lot)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e