import os

from prettytable import PrettyTable

from conf import Config
from library import Library


class ConsoleInterface:
    def __init__(self):
        self.__db_filename = None
        self.__conf = None
        self.__lib = None
        self.main_session()

    def print_books(self, books):
        pretty_books = PrettyTable()
        pretty_books.field_names = ['BookID', 'Name', 'Author', 'Year', 'Genre', 'Publishing']
        for book in books:
            pretty_books.add_row(book)
        print(pretty_books)

    def print_lib_db(self, bases):
        pretty_bases = PrettyTable()
        pretty_bases.field_names = ['N', 'BD file name']
        for i in range(bases):
            pretty_bases.add_row([i, bases[i]])
        print(pretty_bases)

    def get_all_books(self):
        books = self.__lib.search_book()
        self.print_books(books)
        return books

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
        self.print_books(books)
        return books

    def export_book(self):  # todo
        pass

    def import_book(self):  # todo
        pass

    def remove_book(self, bid):
        self.__lib.remove(bid)

    def get_lib_db_names(self):  # todo
        pass

    def change_lib_db(self):  # todo
        pass

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

    def book_menu(self, books):
        input()

    def options_menu(self):
        __options_menu_items = ['Add new DB', 'Change current DB']
        while True:
            for i in range(len(__options_menu_items)):
                print(f'{i+1}\t{__options_menu_items[i]}')
            choice = input(f'Please insert  number from 1 to {len(__options_menu_items)}'
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
                        self.add_lib_db()
                    elif choice == 1:
                        self.change_lib_db()
                    continue
                print(f'\nTry again it must be int from 1 to {len(__options_menu_items)}\n')
            else:
                print(f'\nTry again it must be int from 1 to {len(__options_menu_items)}\n')

    def menu(self):
        __main_menu_items = ['Get all books', 'Search book', 'Add new book', 'Options']
        while True:
            for i in range(len(__main_menu_items)):
                print(f'{i+1}\t{__main_menu_items[i]}')
            choice = input(f'Please insert  number from 1 to {len(__main_menu_items)}'
                           f' or 0 to exit program: ')
            if choice == '' or choice is None:
                continue
            elif choice.isdigit():
                choice = int(choice) -1
                if choice == -1:
                    print('Goodbye')
                    raise SystemExit
                elif 0 <= choice < len(__main_menu_items):
                    print(__main_menu_items[choice])
                    if choice == 0:
                        books = self.get_all_books()
                        self.book_menu(books)
                    elif choice == 1:
                        pass
                    elif choice == 2:
                        pass
                    elif choice == 3:
                        self.options_menu()
                    continue
                print(f'\nTry again it must be int from 1 to {len(__main_menu_items)}\n')
            else:
                print(f'\nTry again it must be int from 1 to {len(__main_menu_items)}\n')

    def main_session(self):
        print('Library v0.2')
        self.get_conf()
        self.menu()


if __name__ == '__main__':
    ConsoleInterface()
