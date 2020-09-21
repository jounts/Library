
from conf import Config
from db import DBConnection
from library import Library

def main():
    # while True:
    #     database_file = input('Введите имя файла для БД Вашей библиотеки: ')
    #     if database_file is not None and database_file.endswith('.db'):
    #         return
    #     elif database_file is not None and not database_file.endswith('.db'):
    #         database_file += '.db'
    #         break
    #     else:
    #         print('Необходимо ввести имя файла')
    # conf = Config(database_file)
    # print(conf.read_conf())

    c = Config()
    print(c.read_conf())
    c.add_base('test')
    c.change_default_base('test')
    b = Config()
    print(b.read_conf())
    b.add_base('new_base.db')
    b.change_default_base('library.db')
    a = Config()
    print(a.read_conf())
    a.change_default_base('new_base.db')
    print(a.read_conf())
    bs = a.get_bases()
    print(bs)

    # file = os.path.join('.', 'conf', 'config.ini')
    # db = os.path.join('.', 'storage')
    # pars = configparser.ConfigParser()
    # with open(file, 'r') as f:
    #     pars.read_file(f)
    #     path = pars['Path'].values()
    #     for value in path:
    #         print(value)
