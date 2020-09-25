import os
import configparser


class Config:
    def __init__(
            self,
            conf_path: str = None,
            db_filename: str = None,
            db_path: str = None
    ):
        attributes = [conf_path, db_filename, db_path]

        for attrib in attributes:
            if not isinstance(attrib, (str, type(None))):
                raise TypeError(f'{attrib} must be str or None')

        if conf_path is None:
            if not os.path.exists(os.path.join('.', 'conf')):
                os.mkdir(os.path.join('.', 'conf'))
            self.__conf_path = os.path.join('.', 'conf', 'config.ini')
        else:
            if not os.path.exists(conf_path):
                os.mkdir(conf_path)
            self.__conf_path = conf_path

        if db_path is None:
            if not os.path.exists(os.path.join('.', 'storage')):
                os.mkdir(os.path.join('.', 'storage'))
            self.__db_path = os.path.join('.', 'storage')
        else:
            if not os.path.exists(db_path):
                os.mkdir(db_path)
            self.__db_path = db_path

        if db_filename is None:
            self.__db_filename = 'library.db'
        else:
            self.__db_filename = db_filename

        self.__conf_parser = configparser.ConfigParser()
        self.__bases = 'Databases'
        self.__path = 'Path'
        if not os.path.exists(self.__conf_path):
            self.create_new_conf(db_filename)
        else:
            self.__conf_parser.read(self.__conf_path)

    def create_new_conf(self, db_filename: str):
        self.__conf_parser[self.__path] = {'db_path': self.__db_path}
        self.__conf_parser[self.__bases] = {self.__db_filename: 'True'}

        with open(self.__conf_path, 'w') as conf_file:
            self.__conf_parser.write(conf_file)

    def read_conf(self):
        self.__conf_parser.read(self.__conf_path)
        path = self.__conf_parser[self.__path]['db_path']
        for base in self.__conf_parser.items(self.__bases):
            if base[1] == 'True':
                return os.path.join(path, base[0])

    def add_base(self, db_filename, key: bool = False):
        try:
            self.__conf_parser[self.__bases][db_filename] = str(key)
            with open(self.__conf_path, 'w') as conf_file:
                self.__conf_parser.write(conf_file)
        except KeyError:
            return

    def change_default_base(self, db_filename):
        for base in self.__conf_parser.items(self.__bases):
            if base[1] == 'True':
                self.__conf_parser.set(self.__bases, base[0], 'False')
        self.__conf_parser.set(self.__bases, db_filename, 'True')
        with open(self.__conf_path, 'w') as conf_file:
            self.__conf_parser.write(conf_file)

    def get_bases(self):
        bases = []
        for base in self.__conf_parser.items(self.__bases):
            bases.append(base[0])
        return bases
