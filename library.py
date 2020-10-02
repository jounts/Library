from db import Connect_sqlite


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

        for attr in str_attributes:
            if not isinstance(attr, (str, type(None))):
                raise TypeError(f'{attr} must be str or None')

        for attr in int_attributes:
            if not isinstance(attr, (int, type(None))):
                raise TypeError(f'{attr} must be int or None')

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
        self.__con = Connect_sqlite(database)

    def save_book(self,
                  bid: int = None,
                  name: str = None,
                  author: str = None,
                  year: int = None,
                  genre: str = None,
                  publishing: str = None
                  ):

        book = Book(bid, name, author, year, genre, publishing)
        self.__con.write_to_db(
            book.bid,
            book.name,
            book.author,
            book.year,
            book.genre,
            book.publishing
        )

    def search_book(self,
                    bid=None,
                    name=None,
                    author=None,
                    year=None,
                    genre=None,
                    publishing=None):
        books = self.__con.find(bid, name, author, year, genre, publishing)
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

    def remove(self, bid):
        self.__con.remove_item(bid)


if __name__ == '__main__':
    pass
