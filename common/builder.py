from abc import ABC, abstractmethod

from common.driver import JsonDriver, CSVDriver


class DriverBuilder(ABC):
    @abstractmethod
    def build(self):
        pass


class JSONBuilder(DriverBuilder):
    def build(self):
        while True:
            filename = input('Enter JSON filename or press [Enter] to quit: ')
            filename = filename.strip()
            if filename is None:
                break
            elif not filename.endswith('.json'):
                filename += '.json'
                return JsonDriver(filename)


class CSVBuilder(DriverBuilder):
    def build(self):
        while True:
            filename = input('Enter CSV filename or press [Enter] to quit: ')
            filename = filename.strip()
            if filename is None or filename == '':
                break
            elif not filename.endswith('.csv'):
                filename += '.csv'
                return CSVDriver(filename)


class FabricDriverBuilder():
    @staticmethod
    def get_driver():
        drivers = {
            1: JSONBuilder,
            2: CSVBuilder
        }
        for key, item in drivers.items():
            print(f'{key}:\t{item.__name__}')
        while True:
            driver_name = input('Enter Driver number or press [Enter] to quit: ')
            if driver_name is None or driver_name == '':
                return
            elif not driver_name.isdigit():
                print('Number must be int')
                continue
            else:
                driver_name = int(driver_name)
                break
        return drivers[driver_name]().build()


if __name__ == '__main__':
    pass
