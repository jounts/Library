import json, csv


class IStructureDriver:
    def red(self, _):
        pass

    def write(self, d, _):
        pass


class JsonDriver(IStructureDriver):
    def __init__(self, filename):
        self.filename = filename

    def read(self, _):
        with open(self.filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def write(self, data, _):
        with open(self.filename, 'a', encoding='utf-8') as f:
            json.dump(data, f)
            f.flush()


class CSVDriver(IStructureDriver):
    def __init__(self, filename):
        self.filename = filename

    def read(self, field_names):
        with open(self.filename, 'r', newline='', encoding='utf-8') as f:
            r_lst = []
            reader = csv.DictReader(f, fieldnames=field_names)
            for row in reader:
                current_row = {}
                for field in field_names:
                    current_row.update({field:row[field]})
                r_lst.append(current_row)
            return r_lst

    def write(self, data, field_names):
        with open(self.filename, 'a', newline='', encoding='utf-8') as f:
            csv_writer = csv.DictWriter(f, fieldnames=field_names)
            for d in data:
                csv_writer.writerow(d)


if __name__ == '__main__':
    pass
