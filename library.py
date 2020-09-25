import os

from db import DBConnection


class Book:
    def __init__(
            self,
            bid: int = None,
            name: str = None,
            author: str = None,
            year: int = None,
            genre: str = None,
            publishing: str = None
    ):

        str_attributes = [name, author, genre, publishing]
        int_attributes = [bid, year]

        for attrib in str_attributes:
            if not isinstance(attrib, (str, type(None))):
                raise TypeError(f'{attrib} must be str or None')

        for attrib in int_attributes:
            if not isinstance(attrib, (int, type(None))):
                raise TypeError(f'{attrib} must be int or None')
        self.__bid = bid
        self.__name = name
        self.__author = author
        self.__year = year
        self.__genre = genre
        self.__publishing = publishing

    @property
    def bid(self):
        return self.__bid

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f'{value} must be str')
        self.__name = value

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f'{value} must be str')
        self.__author = value

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f'{value} must be int')
        self.__year = value

    @property
    def genre(self):
        return self.__genre

    @genre.setter
    def genre(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f'{value} must be str')
        self.__genre = value

    @property
    def publishing(self):
        return self.__publishing

    @publishing.setter
    def publishing(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f'{value} must be str')
        self.__publishing = value

    def get_book(self) -> object:
        return [self.bid, self.name, self.author, self.year, self.genre, self.publishing]

    def __repr__(self):
        return f'{self.bid}\t{self.name}\t{self.author}\t{self.year}\t{self.genre}\t{self.publishing}'


class Library:
    def __init__(self, database):
        if not isinstance(database, str):
            raise TypeError(f'{database} must be str')

        if not os.path.exists(database):
            raise ValueError(f'{database} file not exists')

        self.__con = DBConnection(database)

        with self.__con as cursor:
            execute_msg = 'CREATE TABLE IF NOT EXISTS BOOKS(' \
                          'id integer PRIMARY KEY,' \
                          'name text,' \
                          'author text,' \
                          'year integer,' \
                          'genre text,' \
                          'publishing text)'
            cursor.execute(execute_msg)

    def save_book(self, book: Book):
        if book.bid is None:
            execute_msg = f'insert into books(id, name, author, year, genre, publishing)' \
                          f'values ' \
                          f'    (' \
                          f'        "%null%",' \
                          f'        "%{book.name}%",' \
                          f'        "%{book.author}%",' \
                          f'        "%{book.year}%",' \
                          f'        "%{book.genre}%",' \
                          f'        "%{book.publishing}%"' \
                          f'    )'
        else:
            execute_msg = f'update books' \
                          f'    set name = "%{book.name}%",' \
                          f'    author = "%{book.author}%",' \
                          f'    year ="%{book.year}%",' \
                          f'    genre = "%{book.genre}%",' \
                          f'    publishing = "%{book.publishing}%"' \
                          f'where id = "%{book.bid}%"'
        with self.__con as cursor:
            cursor.execute(execute_msg)

    def find_book(self,
                  bid: int = None,
                  name: str = None,
                  author: str = None,
                  year: int = None,
                  genre: str = None,
                  publishing: str = None):
        if bid is not None:
            execute_msg = f'Select * from books where id = "%{bid}%"'
        elif name is not None:
            execute_msg = f'Select * from books where name like "%{name}%"'
        elif author is not None:
            execute_msg = f'Select * from books where author like "%{author}%"'
        elif year is not None:
            execute_msg = f'Select * from books where year like "%{year}%"'
        elif genre is not None:
            execute_msg = f'Select * from books where genre like "%{genre}%"'
        elif publishing is not None:
            execute_msg = f'Select * from books where publishing like "%{publishing}%"'
        else:
            execute_msg = 'select * from books'

        with self.__con as cursor:
            cursor.execute(execute_msg)
            books = cursor.fetchall()
            ans = []
            for book in books:
                ans.append(Book(
                    int(book[0]) if book[0] is not None else book[0],
                    str(book[1]) if book[1] is not None else book[1],
                    str(book[2]) if book[2] is not None else book[2],
                    int(book[3]) if book[3] is not None else book[3],
                    str(book[4]) if book[4] is not None else book[4],
                    str(book[5]) if book[5] is not None else book[5]).get_book())
            return ans

    def remove(self, book):
        execute_msg = f'delete from books where id = "%{book.bid}%"'
        with self.__con as cursor:
            cursor.execute(execute_msg)


if __name__ == '__main__':
    pass
