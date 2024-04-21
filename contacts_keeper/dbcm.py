import mysql.connector


class UseDatabase:

    def __init__(self, config) -> None:
        self.configuration = config

    def __enter__(self):
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.conn.commit()
        self.conn.close()
        self.conn.close()
