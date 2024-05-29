import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = str(os.environ.get('SECRET_KEY'))
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_FILE_DIR = './.flask_session/'
    SESSION_TYPE = 'filesystem'