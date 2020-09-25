import os
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
            self.__connection.commit()



class Connect_sqlite:
    def __init__(self, database):
        if not isinstance(database, str):
            raise TypeError(f'{database} must be str')

        # if not os.path.exists(database):
        #     raise ValueError(f'{database} file not exists')

        self.__connection = DBConnection(database)

        with self.__connection as cursor:
            execute_msg = 'CREATE TABLE IF NOT EXISTS BOOKS(' \
                          'id integer PRIMARY KEY,' \
                          'name text,' \
                          'author text,' \
                          'year integer,' \
                          'genre text,' \
                          'publishing text)'
            cursor.execute(execute_msg)

    def write_to_db(self, bid, name, author, year, genre, publishing):
        book_info = [name, author, year, genre, publishing]

        if bid is None:
            # if year is not None:
            execute_msg = f'insert into books(id, name, author, year, genre, publishing)' \
                          f' values(null, ?, ?, ?, ?, ?)'
            with self.__connection as cursor:
                cursor.execute(execute_msg, book_info)
        else:
            execute_msg = f'update books set '
            key = False
            if name is not None:
                execute_msg += f'name = "{name}"'
                key = True
            if author is not None:
                if key:
                    execute_msg += f', author = "{author}"'
                else:
                    execute_msg += f' author = "{author}"'
                    key = True
            if year is not None:
                if key:
                    execute_msg += f', year ="{year}"'
                else:
                    execute_msg += f' year ="{year}"'
                    key = True
            if genre is not None:
                if key:
                    execute_msg += f', genre = "{genre}"'
                else:
                    execute_msg += f' genre = "{genre}"'
                    key = True
            if publishing is not None:
                if key:
                    execute_msg += f', publishing = "{publishing}"'
                else:
                    execute_msg += f' publishing = "{publishing}"'
            execute_msg += f' where id = "{bid}"'

            with self.__connection as cursor:
                print(execute_msg)
                cursor.execute(execute_msg)

    def find(self,
             bid=None,
             name=None,
             author=None,
             year=None,
             genre=None,
             publishing=None
             ):
        str_attributes = [name, author, year, genre, publishing]

        for attr in str_attributes:
            if not isinstance(attr, (str, type(None))):
                raise TypeError(f'{attr} must be str or None')

        if not isinstance(bid, (int, type(None))):
            raise TypeError(f'{bid} must be int or None')

        if bid is not None:
            execute_msg = f'Select * from books where id = "%{bid}%"'
        elif name is not None or \
                author is not None or \
                year is not None or \
                genre is not None or \
                publishing is not None:
            execute_msg = 'Select * from books where '
            key = False
            if name is not None:
                execute_msg += f'name like "%{name}%"'
                key = True
            if author is not None:
                if key:
                    execute_msg += f'and author like "%{author}%" '
                else:
                    execute_msg += f'author like "%{author}%" '
                    key = True
            if year is not None:
                if key:
                    execute_msg += f'and year like "%{year}%" '
                else:
                    execute_msg += f'year like "%{year}%" '
                    key = True
            if genre is not None:
                if key:
                    execute_msg += f'and genre like "%{genre}%" '
                else:
                    execute_msg += f'genre like "%{genre}%" '
                    key = True
            if publishing is not None:
                if key:
                    execute_msg += f'and publishing like "%{publishing}%"'
                else:
                    execute_msg += f'publishing like "%{publishing}%"'
        else:
            execute_msg = 'select * from books'

        with self.__connection as cursor:
            cursor.execute(execute_msg)
            return cursor.fetchall()

    def remove_item(self, bid):
        if not isinstance(bid, int):
            raise TypeError(f'{bid} must be int')
        execute_msg = f'delete from books where id = "%{bid}%"'
        with self.__connection as cursor:
            cursor.execute(execute_msg)

