DEBUG = True

USERNAME = 'root'
PASSWORD = 'A123456b!'
SERVER = 'localhost'
DB = 'gerenciamento_contas'

SQLALCHEMY_DATABASE_URI = f'mysql://{USERNAME}:{PASSWORD}@{SERVER}/{DB}'
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY="gerenciamento_contas"