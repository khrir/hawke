from unittest import mock
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from app.models.entities.user import User
from app.models.repository.user_repository import UserRepository

class ConnectionHandlerMock:
    def __init__(self) -> None:
        self.session =  \
            UnifiedAlchemyMagicMock(
                data = [
                    (
                        [mock.call.query(User)],
                        [
                            User(id=1, username="Barthollomew", email="barth@hawke.com", password="abc123", cpf="12345678909", birthdate="2019-12-28", role_id=1),
                            User(id=2, username="Jorge", email="j@hawke.com", password="abc123", cpf="12345678909", birthdate="2019-12-28", role_id=1),
                            User(id=3, username="Roger", email="r@hawke.com", password="abc123", cpf="12345678909", birthdate="2019-12-28", role_id=1),
                        ],
                    )
                ]
            )

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

def test_select():
    user_repository = UserRepository(ConnectionHandlerMock)
    users = user_repository.select()

    assert isinstance(users, list)
    assert isinstance(users[0], User)

def test_insert():
    user_repository = UserRepository(ConnectionHandlerMock)
    user = User(id=4, username="Raimundo", email="r@hawke.com", password="abc123", cpf="12345678909", birthdate="2019-12-28", role_id=1)
    response = user_repository.insert(user)
    
    assert isinstance(response, User)
