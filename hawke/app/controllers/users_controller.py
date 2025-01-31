from app.models.entities.user import User
from app.models.repository.user_repository import UserRepository
from infra.configs.connection import DBConnectionHandler

class UsersController:
    def __init__(self):
        self.__user_repository = UserRepository(DBConnectionHandler)

    def list(self):
        return self.__user_repository.list()
    
    def validate_speaker(self, email):
        user = self.select_by_email(email)
        if user is None:
            username = 'Speaker ' + email.split('@')[0]
            password = 'Mudar123@'
            
            speaker = User(username=username, email=email, password=password)
            user = self.insert_speaker(speaker)
        
        return user

    def select_by_email(self, email):
        user = self.__user_repository.select_by_email(email)
        return user
    
    def insert_speaker(self, data):
        user = self.__user_repository.insert_speaker(data)
        return user
    
    def create(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')

        user = dict(username=username, email=email, password=password, password_confirmation=password_confirmation)
        user = self.__validate_user(user)
        
        self.__user_repository.insert(user)

        return {'success': True}, 201 
    
    def login(self, data):
        email = data.get('email')
        password = data.get('password')

        user = self.__user_repository.authenticate(email, password)
        if user is None:
            return {'success': False, 'errors': 'Credenciais incorretas.'}, 401

        return {'user': user, 'success': True}, 200

    def update(self, data):
        username = data.get('username') | None
        email = data.get('email') | None
        password = data.get('password') | None

        user = {'username': username, 'email': email, 'password': password}
        res, err = self.__user_repository.update(user)
        if err is not None:
            return {'success': False, 'errors': {'user': {err}}}, res

        return {'success': True}, res

    def delete(self, user_id):
        user = self.__user_repository.select_by_id(user_id)

        if user is None:
            return {'success': False, 'errors': {'user': 'Usuário não encontrado'}}, 404
        
        res, err = self.__user_repository.delete(user)
        if err is not None:
            return {'success': False, 'errors': {'user': {err}}}, res

        return {'success': True}, res

    def __validate_user(self, user) -> User:
        if user is None:
            return {'success': False, 'errors': {'username': 'Usuário vazio'}}, 400
        
        if user.get('username') is None or user.get('username') == "" or not isinstance(user.get('username'), str):
            return {'success': False, 'errors': {'username': 'Informe o nome completo'}}, 400

        if user.get('email') is None or user.get('email') == "" or not isinstance(user.get('email'), str):
            return {'success': False, 'errors': {'email': 'Informe o email'}}, 400

        if self.select_by_email(user.get('email')) is not None:
            return {'success': False, 'errors': {'email': 'Email já cadastrado'}}, 400

        if user.get('password') is None or user.get('password') == "" or not isinstance(user.get('password'), str):
            return {'success': False, 'errors': {'password': 'Informe a senha'}}, 400

        if user.get('password_confirmation') is None or user.get('password_confirmation') == "" or not isinstance(user.get('password_confirmation'), str):
            return {'success': False, 'errors': {'password_confirmation': 'Confirme a senha'}}, 400
        
        if user.get('password') != user.get('password_confirmation'):
            return {'success': False, 'errors': {'password': 'As senhas não conferem'}}, 400
        
        return User(username=user.get('username'), email=user.get('email'), password=user.get('password'))