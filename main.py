import os
import re

from prettytable import PrettyTable

from conf import Config
from library import Library
from builder import FabricDriverBuilder


class ConsoleInterface:
    def __init__(self):
        self.__db_filename = None
        self.__conf = None
        self.__lib = None
        self.__books = []
        self.__bases = []
        self.__driver = None
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

    def export_book(self):
        exp_books = []
        fields = ['Name', 'Author', 'Year', 'Genre', 'Publishing']
        for book in self.__books:
            exp_book = {}
            for i, field in enumerate(book[1:]):
                exp_book.update({fields[i]:field})
            exp_books.append(exp_book)
        self.__driver = FabricDriverBuilder.get_driver()
        if self.__driver is None:
            return
        self.__driver.write(exp_books,fields)

    def import_book(self):
        imp_books = []
        fields = ['Name', 'Author', 'Year', 'Genre', 'Publishing']
        bid = None
        self.__driver = FabricDriverBuilder.get_driver()
        if self.__driver is None:
            return
        for book in self.__driver.read(fields):
            imp_book = []
            for item in book.values():
                imp_book.append(item)
            imp_books.append(imp_book)
        for imp_book in imp_books:
            if isinstance(imp_book[2], str):
                year = int(imp_book[2]) if imp_book[2].isdigit() else None
            elif isinstance(imp_book[2], int):
                year =imp_book[2]
            else:
                year = None
            self.__lib.save_book(bid=bid,
                                 name=imp_book[0],
                                 author=imp_book[1],
                                 year=year,
                                 genre=imp_book[3],
                                 publishing=imp_book[4])

    def remove_book(self, bid):
        self.__lib.remove(bid)

    def get_lib_db_names(self):
        self.__bases = self.__conf.get_bases()

    def change_lib_db(self, db_filename):
        self.__conf.change_current_base(db_filename)
        self.__db_filename = self.__conf.read_conf()
        print(f'Connecting to {self.__db_filename}')
        self.__lib = Library(self.__db_filename)

    def add_lib_db(self, db_filename):
        if not db_filename.endswith('.db'):
            db_filename += '.db'
        self.__conf.add_base(db_filename)

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
        pretty_bases.field_names = ['DB ID', 'BD file name']
        for i, base in enumerate(self.__bases):
            pretty_bases.add_row([i + 1, base])
        print(pretty_bases)

    def book_menu(self):
        __book_menu_items = ['Export books', 'Change book', 'Remove book']
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
                choice = int(choice) - 1
                if choice == 0:
                    self.export_book()
                elif choice == 1:
                    self.change_book_menu()
                    break
                elif choice == 2:
                    self.remove_book_menu()
                    break
                elif choice == -1:
                    break
        self.__books = []

    def add_book_menu(self):
        while True:
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
            attributes = [name, author, year, genre, publishing]
            if len([attr for attr in attributes if attr is not None]):
                print(f'Name: {name}, '
                      f'Author: {author}, '
                      f'Year: {year}, '
                      f'Genre: {genre}, '
                      f'Publishing: {publishing}')
                answer = input(f'Insert {yes[0]} or {yes[1]} to continue or any key to try again: ')
                if answer in yes:
                    self.add_book(name=name, author=author, year=year, genre=genre, publishing=publishing)
                    break
            print('Some attribute must be not None')

    def change_book_menu(self):
        while True:
            bid = input('Please, enter BookID of book to modify or q to return: ')
            if bid.isdigit():
                bid = int(bid)
            elif bid == 'q':
                break
            else:
                print('Bad BookId, try again')
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
            attributes = [name, author, year, genre, publishing]
            if len([attr for attr in attributes if attr is not None]):
                print(f'BookID={bid}, '
                      f'Name: {name}, '
                      f'Author: {author}, '
                      f'Year: {year}, '
                      f'Genre: {genre}, '
                      f'Publishing: {publishing}')
                answer = input(f'Insert {yes[0]} or {yes[1]} to continue or any key to try again: ')
                if answer in yes:
                    self.change_book(bid, name=name, author=author, year=year, genre=genre, publishing=publishing)
                    break
            print('Some attribute must be not None')

    def remove_book_menu(self):
        while True:
            bid = input('Please, enter BookID of book to remove or q to return: ')
            if bid.isdigit():
                bid = int(bid)
                self.remove_book(bid)
                break
            elif bid == 'q':
                break
            else:
                print('Bad BookId, try again')
                continue

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
                choice = int(choice) - 1
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
                choice = int(choice) - 1
                if choice == -1:
                    print('Return to main menu\n')
                    break
                elif 0 <= choice < len(__options_menu_items):
                    print(__options_menu_items[choice])
                    if choice == 0:
                        self.add_lib_menu()
                    elif choice == 1:
                        self.change_lib_menu()
                    continue
                print(f'\nTry again it must be int from 1 to {__menu_len}\n')
            else:
                print(f'\nTry again it must be int from 1 to {__menu_len}\n')

    def change_lib_menu(self):
        self.__bases = self.__conf.get_bases()
        bases_count = len(self.__bases)
        while True:
            self.print_lib_db()
            choice = input('Enter DB ID or 0 to return: ')
            if choice.isdigit():
                choice = int(choice) - 1
                if choice == -1:
                    break
                elif 0 <= choice < bases_count:
                    self.change_lib_db(self.__bases[choice])
                    self.__bases = []
                    break
            print('Try again')

    def add_lib_menu(self):
        pattern = '[\w]+'
        while True:
            db_filename = input('Enter DB name or 0 to return: ')
            if db_filename.isdigit():
                db_filename = int(db_filename)
                if db_filename == 0:
                    return
            if re.match(pattern, db_filename) is None:
                print('Bad name, try again')
                continue
            self.add_lib_db(db_filename)
            break
        yes = ['y', 'yes']
        while True:
            answer = input(f'Insert {yes[0]}/{yes[1]} to connect to {db_filename}: ')
            if answer in yes:
                self.change_lib_menu()
                return

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
                choice = int(choice) - 1
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
                        self.add_book_menu()
                    elif choice == 3:
                        self.import_book()
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
