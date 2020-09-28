import os

from prettytable import PrettyTable

from conf import Config
from library import Library


class ConsoleInterface:
    def __init__(self):
        self.__db_filename = None
        self.__conf = None
        self.__lib = None
        self.__books = []
        self.__bases = []
        self.main_session()

    def search_book(self,
                    name: str = None,
                    author: str = None,
                    year: int = None,
                    genre: str = None,
                    publishing: str = None
                    ):
        books = self.__lib.search_book(name=name,
                                       author=author,
                                       year=year,
                                       genre=genre,
                                       publishing=publishing
                                       )
        return books

    def add_book(self,
                 name=None,
                 author=None,
                 year=None,
                 genre=None,
                 publishing=None):
        self.__lib.save_book(name=name, author=author, year=year, genre=genre, publishing=publishing)

    def change_book(self,
                    bid,
                    name=None,
                    author=None,
                    year=None,
                    genre=None,
                    publishing=None):
        self.__lib.save_book(bid=bid, name=name, author=author, year=year, genre=genre, publishing=publishing)

    def export_book(self):  # todo
        pass

    def import_book(self):  # todo
        pass

    def remove_book(self, bid):
        self.__lib.remove(bid)

    def get_lib_db_names(self):
        self.__bases = self.__conf.get_bases()

    def change_lib_db(self, db_filename):
        self.__conf.change_default_base(db_filename)
        self.__db_filename = self.__conf.read_conf()

    def add_lib_db(self):
        while True:
            db_filename = input('Insert DB file name '
                                'or press Enter to exit: ')
            if db_filename == '' or db_filename is None:
                return
            elif not db_filename.endswith('.db'):
                db_filename += '.db'
                break
        self.__conf.add_base(db_filename)
        yes = ['y', 'yes']
        answer = input(f'Insert {yes[0]} or {yes[1]} to connect to the {db_filename}: ')
        if answer in yes:
            self.__conf.change_default_base(db_filename)

    def get_conf(self):
        self.__conf = Config()
        db_filename = self.__conf.read_conf()
        if not os.path.exists(db_filename):
            print('First launch detected')
            print('Library needs to prepare DB file to continue')
            while True:
                db_filename = input('Please insert DB file name '
                                    'or press Enter for default (Library.db): ')
                if db_filename == '' or db_filename is None:
                    db_filename = 'Library.db'
                    self.__db_filename = db_filename
                    break
                elif not db_filename.endswith('.db'):
                    db_filename += '.db'
                    break
            self.__conf.create_new_conf(self.__db_filename)
            print(f'{self.__db_filename} created')
        else:
            self.__db_filename = db_filename
            print(f'Connecting to {self.__db_filename}')
        self.__lib = Library(self.__db_filename)

    def print_books(self):
        pretty_books = PrettyTable()
        pretty_books.field_names = ['BookID', 'Name', 'Author', 'Year', 'Genre', 'Publishing']
        for book in self.__books:
            pretty_books.add_row(book)
        print(pretty_books)

    def print_lib_db(self):
        pretty_bases = PrettyTable()
        pretty_bases.field_names = ['N', 'BD file name']
        for i, base in enumerate(self.__bases):
            pretty_bases.add_row([i, base])
        print(pretty_bases)

    def book_menu(self):
        __book_menu_items = ['Export books', 'Change book']
        __menu_len = len(__book_menu_items)
        self.print_books()
        while True:
            for i, menu_item in enumerate(__book_menu_items):
                print(f'{i + 1} - {menu_item} ', end='')
            print()
            choice = input(f'Please insert  number from 1 to {__menu_len}'
                           f' or 0 - return to main menu: ')
            if choice == '' or choice is None:
                continue
            elif choice.isdigit():
                try:
                    choice = int(choice) - 1
                except:
                    print('It must be int')
                    continue
                if choice == -1:
                    break
                if choice == 0:
                    for book in self.__books:
                        self.export_book(book)
                        break
                elif choice == 1:
                    self.change_book_menu()
                    break
        self.__books = []

    def change_book_menu(self):
        while True:
            bid = input('Please, enter BookID of book to modify: ')
            if bid.isdigit():
                try:
                    bid = int(bid)
                except:
                    print('It must be int')
                    continue

            name = input('insert an name of book: ')
            if name == '' or name is None:
                name = None

            author = input('insert an author of book: ')
            if author == '' or author is None:
                author = None

            while True:
                year = input('insert an year of book: ')
                if year == '' or year is None:
                    year = None
                    break
                elif year.isdigit():
                    year = int(year)
                    break
                else:
                    print('year must be int')

            genre = input('insert an genre of book : ')
            if genre == '' or genre is None:
                genre = None

            publishing = input('insert an publishing of book: ')
            if publishing == '' or publishing is None:
                publishing = None

            yes = ['y', 'yes']
            print()
            answer = input(f'Insert {yes[0]} or {yes[1]} to continue or any key to try again: ')
            if answer in yes:
                self.change_book(bid, name=name, author=author, year=year, genre=genre, publishing=publishing)
                break


    def get_all_books(self):
        self.__books = self.__lib.search_book()
        self.book_menu()

    def search_book_menu(self):
        __search_menu_items = ['by name', 'by author', 'by year', 'by genre', 'by publishing', 'by several items']
        __menu_len = len(__search_menu_items)
        name = author = year = genre = publishing = None
        while True:
            for i, menu_item in enumerate(__search_menu_items):
                print(f'{i + 1} - {menu_item} ', end='')
            print()
            choice = input(f'Please insert  number from 1 to {__menu_len}'
                           f' or 0 - return to main menu: ')
            if choice == '' or choice is None:
                continue
            elif choice.isdigit():
                try:
                    choice = int(choice) - 1
                except:
                    print('It must be int')
                    continue
                if choice == -1:
                    self.__books = []
                    print('Return to main menu\n')
                    break
                elif 0 <= choice < __menu_len:
                    print(__search_menu_items[choice])
                    if choice == 0:
                        name = input('insert an name of book: ')
                        if name == '' or name is None:
                            name = None
                        break
                    elif choice == 1:
                        author = input('insert an author of book: ')
                        if author == '' or author is None:
                            author = None
                        break
                    elif choice == 2:
                        while True:
                            year = input('insert an year of book: ')
                            if year == '' or year is None:
                                year = None
                                break
                            elif year.isdigit():
                                year = int(year)
                                break
                            else:
                                print('year must be int')
                        break
                    elif choice == 3:
                        genre = input('insert an genre of book : ')
                        if genre == '' or genre is None:
                            genre = None
                        break
                    elif choice == 4:
                        publishing = input('insert an publishing of book: ')
                        if publishing == '' or publishing is None:
                            publishing = None
                        break
                    elif choice == 5:
                        name = input('insert an name book'
                                     'or enter to pass: ')
                        if name == '' or name is None:
                            name = None
                        author = input('insert an author of book'
                                       'or enter to pass: ')
                        if author == '' or author is None:
                            author = None
                        while True:
                            year = input('insert an year of book'
                                         'or enter to pass: ')
                            if year == '' or year is None:
                                year = None
                                break
                            elif year.isdigit():
                                year = int(year)
                                break
                            else:
                                print('year must be int')
                        genre = input('insert an genre of book'
                                      'or enter to pass: ')
                        if genre == '' or genre is None:
                            genre = None
                        publishing = input('insert an publishing of book'
                                           'or enter to pass: ')
                        if publishing == '' or publishing is None:
                            publishing = None
                        break
                    continue
                print(f'\nTry again it must be int from 1 to {__menu_len}\n')
            else:
                print(f'\nTry again it must be int from 1 to {__menu_len}\n')

        self.__books = self.search_book(name, author, year, genre, publishing)
        self.book_menu()

    def options_menu(self):
        __options_menu_items = ['Add new DB', 'Change current DB']
        __menu_len = len(__options_menu_items)
        while True:
            for i in range(__menu_len):
                print(f'{i + 1}\t{__options_menu_items[i]}')
            choice = input(f'Please insert  number from 1 to {__menu_len}'
                           f' or 0 - return to main menu: ')
            if choice == '' or choice is None:
                continue
            elif choice.isdigit():
                try:
                    choice = int(choice) - 1
                except:
                    print('It must be int')
                    continue
                if choice == -1:
                    print('Return to main menu\n')
                    break
                elif 0 <= choice < len(__options_menu_items):
                    print(__options_menu_items[choice])
                    if choice == 0:
                        self.add_lib_db()
                    elif choice == 1:
                        self.change_lib_db()
                    continue
                print(f'\nTry again it must be int from 1 to {__menu_len}\n')
            else:
                print(f'\nTry again it must be int from 1 to {__menu_len}\n')

    def menu(self):
        __main_menu_items = ['Get all books', 'Search book', 'Add new book', 'Import books', 'Options']
        __menu_len = len(__main_menu_items)
        while True:
            for i in range(len(__main_menu_items)):
                print(f'{i + 1}\t{__main_menu_items[i]}')
            choice = input(f'Please insert  number from 1 to {__menu_len}'
                           f' or 0 to exit program: ')
            if choice == '' or choice is None:
                continue
            elif choice.isdigit():
                try:
                    choice = int(choice) - 1
                except:
                    print('It must be int')
                    continue
                if choice == -1:
                    print('Goodbye')
                    raise SystemExit
                elif 0 <= choice < len(__main_menu_items):
                    print(__main_menu_items[choice])
                    if choice == 0:
                        self.get_all_books()
                    elif choice == 1:
                        self.search_book_menu()
                    elif choice == 2:
                        pass
                    elif choice == 3:
                        pass
                    elif choice == 4:
                        self.options_menu()
                    continue
                print(f'\nTry again it must be int from 1 to {__menu_len}\n')
            else:
                print(f'\nTry again it must be int from 1 to {__menu_len}\n')

    def main_session(self):
        print('Library v0.2')
        self.get_conf()
        self.menu()


if __name__ == '__main__':
    ConsoleInterface()
