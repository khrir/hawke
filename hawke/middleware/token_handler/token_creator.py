from datetime import datetime, timedelta
import time, jwt

class TokenCreator:
    def __init__(self, token_key: str, exp_time: int, refresh_time: int):
        self.__TOKEN_KEY = token_key
        self.__EXP_TIME = exp_time
        self.__REFRESH_TIME = refresh_time

    def create(self, uid: int):
        return self.__encode(uid)
    
    def refresh(self, token: str):
        token_info = jwt.decode(token, key=self.__TOKEN_KEY, algorithms=['HS256'])
        token_uid = token_info['uid']
        exp_time = token_info['exp']

        if ((exp_time - time.time())/60) < self.__REFRESH_TIME:
            return self.__encode(token_uid)
        return token

    def __encode(self, uid: int):
        return jwt.encode({
            'uid': uid,
            'exp': datetime.now(datetime.UTC) + timedelta(minutes=self.__EXP_TIME),
        }, key=self.__TOKEN_KEY, algorithm='HS256')