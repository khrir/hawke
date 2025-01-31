from token_creator import TokenCreator
from dotenv import load_dotenv
import os

load_dotenv()

token_creator = TokenCreator (
    token_key=os.getenv('TOKEN_KEY'),
    exp_time=int(os.getenv('EXP_TIME')),
    refresh_time=int(os.getenv('REFRESH_TIME'))
)