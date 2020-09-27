import os
import configparser


class Config:
    def __init__(self):
        self.__conf_dir = os.path.join('.', 'conf')
        self.__conf_file = os.path.join(self.__conf_dir, 'config.ini')
        self.__db_path = os.path.join('.', 'storage')
        self.__db_filename = None
        self.__bases = 'Databases'
        self.__path = 'Path'
        self.__conf_parser = configparser.ConfigParser()

    def create_new_conf(self, db_filename: str):
        if not os.path.exists(self.__conf_dir):
            os.mkdir(self.__conf_dir)
            os.mkdir(self.__db_path)
            self.__conf_parser.add_section(self.__path)
            self.__conf_parser.add_section(self.__bases)
            self.__conf_parser[self.__path] = {'db_path': self.__db_path}
            self.__conf_parser[self.__bases] = {db_filename: 'True'}
            with open(self.__conf_file, 'w') as conf_file:
                self.__conf_parser.write(conf_file)

    def read_conf(self):
        if not os.path.exists(self.__conf_dir):
            return -1
        else:
            self.__conf_parser.read(self.__conf_file)
            path = self.__conf_parser[self.__path]['db_path']
            for base in self.__conf_parser.items(self.__bases):
                if base[1] == 'True':
                    return os.path.join(path, base[0])

    def add_base(self, db_filename, key: bool = False):
        try:
            self.__conf_parser[self.__bases][db_filename] = str(key)
            with open(self.__conf_file, 'w') as conf_file:
                self.__conf_parser.write(conf_file)
        except KeyError:
            return

    def change_default_base(self, db_filename):
        for base in self.__conf_parser.items(self.__bases):
            if base[1] == 'True':
                self.__conf_parser.set(self.__bases, base[0], 'False')
        self.__conf_parser.set(self.__bases, db_filename, 'True')
        with open(self.__conf_file, 'w') as conf_file:
            self.__conf_parser.write(conf_file)

    def get_bases(self):
        bases = []
        for base in self.__conf_parser.items(self.__bases):
            bases.append(base[0])
        return bases
