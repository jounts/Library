
from conf import Config
from db import DBConnection
from library import Library

def main():

    conf = Config()
    print(conf.read_conf())
    my_lyb = Library(conf.read_conf())
    # my_lyb.save_book(name='test_name_book', author='test_author')
    for book in my_lyb.find_book():
        print(book)
    my_lyb.save_book(2, year=1861, genre='классика')
    for book in my_lyb.find_book(author='Толст', genre='ас'):
        print(book)

    # print(b.read_conf())
    # b.add_base('new_base.db')
    # b.change_default_base('library.db')
    # a = Config()
    # print(a.read_conf())
    # a.change_default_base('new_base.db')
    # print(a.read_conf())
    # bs = a.get_bases()
    # print(bs)

    # file = os.path.join('.', 'conf', 'config.ini')
    # db = os.path.join('.', 'storage')
    # pars = configparser.ConfigParser()
    # with open(file, 'r') as f:
    #     pars.read_file(f)
    #     path = pars['Path'].values()
    #     for value in path:
    #         print(value)

if __name__ == '__main__':
    main()
