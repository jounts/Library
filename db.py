import sqlite3


class DBConnection:
    def __init__(self, database):
        self.__connection = sqlite3.connect(database)
        self.__cursor = None

    def __enter__(self):
        self.__cursor = self.__connection.cursor()
        return self.__cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, Exception):
            self.__connection.rollback()
        else:
            self.__cursor.commit()
        self.__cursor.close()
