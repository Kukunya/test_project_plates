

HOST = 'localhost'
PORT = '5432'
DATABASE = 'TestProjectDB'
USER = 'postgres'
PASSWORD = 'admin'


class FlaskConf:
    SECRET_KEY = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
