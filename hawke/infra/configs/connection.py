from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

db_dialect = os.environ.get("DB_DIALECT")
db_driver = os.environ.get("DB_DRIVER")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_database = os.environ.get("DB_DATABASE")

class DBConnectionHandler:
    def __init__(self):
        self.__connection_string = f"{db_dialect}+{db_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
        self.__engine = self.__create_engine()
        self.session = None

    def __create_engine(self):
        engine = create_engine(self.__connection_string)
        return engine
    
    def get_engine(self):
        return self.__engine
    
    def __enter__(self):
        self.session = sessionmaker(bind=self.__engine)()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        