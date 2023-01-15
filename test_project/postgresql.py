from configparser import ConfigParser
import psycopg2


class PostgreORM:

    def __init__(self):
        self.database_params = load_database_params(path_to_conf)
        self.connection = psycopg2.connect(
            dbname=self.database_params['database'], user=self.database_params['user'],
            password=self.database_params['password'], host=self.database_params['host']
        )
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self) -> None:
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS plates
                                (
                                    pk serial,
                                    id uuid DEFAULT uuid_generate_v4(),
                                    plate character varying(10),
                                    PRIMARY KEY (pk)
                                );""")

    def update_database(self, plate) -> None:
        self.cursor.execute(f"""INSERT INTO plates (plate) 
                                VALUES ('{plate}');""")
        self.connection.commit()

    def get_plates(self, columns: list, clauses=''):
        self.cursor.execute(f"""SELECT {', '.join(columns)} 
                                FROM plates 
                                {clauses};""")
        return self.cursor.fetchall()


def load_database_params(filename):
    conf = ConfigParser()
    conf.read(filename)
    connect_params = {
        key: value for key, value in conf.items("postgresql_connection_data")
    }
    return connect_params


path_to_conf = '../conf/database.ini'
PlatesViewer = PostgreORM()
