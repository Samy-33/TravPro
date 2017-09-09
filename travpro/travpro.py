import argparse
import os
from helpers import ConfigData
from config import FILE_TYPES

import operator

class TravPro:

    def __init__(self, path):
        self.path = path
        self.counter = {}
        self.data = self.generate_ext_dict()

    def generate_ext_dict(self):

        data = dict()

        for language, extensions in FILE_TYPES.items():

            for ext in extensions:
                data[ext] = language

        self.counter['unknown'] = 0

        return data

    def travel(self):
        for root, subdirs, files in os.walk(self.path):
            for f in files:
                extension = f.split('.')[-1]
                try:
                    if self.data[extension] in self.counter.keys():
                        self.counter[self.data[extension]] += 1
                    else:
                        self.counter[self.data[extension]] = 1

                except KeyError as e:

                    self.counter['unknown'] += 1

                except Exception as e:
                    print('Unknown error ' + str(e))
                    exit()



    def number_of_lines(self, file_path):
        #TODO: Add this functionality. Count percentage of code on the basis of # of lines in a file
        pass

    def print_results(self):

        from terminaltables import AsciiTable

        self.counter = sorted(self.counter.items(), key = operator.itemgetter(1), reverse=True)

        sm = sum(fs for name, fs in self.counter)

        table_data = [['Language', 'Total Files', 'Percentage']]

        table_data += [[key, value, str(round((float(value)*100)/sm, 2))+' %'] \
                        for key, value in self.counter]

        table = AsciiTable(table_data)
        print(table.table)

    @staticmethod
    def add_file_type(language_string):

        try:
            language = language_string.split(':')[0].strip()
            extensions = language_string.split(':')[-1]
            extensions = extensions.lstrip('[').rstrip(']').split(',')
            extensions = tuple(ex.strip() for ex in extensions)

            FILE_TYPES[language] = extensions

            data = ConfigData(FILE_TYPES)

            formatted_data = data.__str__()

            with open('config.py', 'w') as f:
                f.write(formatted_data)

            print(f'Successfully Added ==> {language_string}')

        except Exception as e:
            print(str(e) + '\nfile types in format Python:[py,pyc,pwc]')
            exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--path', type=str, help='path of the project')
    parser.add_argument('-a', '--add-file-type', type=str, help='file types in'
                                                                'format Python:[py,pyc,pwc]')
    args = parser.parse_args()

    if args.add_file_type:
        TravPro.add_file_type(args.add_file_type)
        exit(0)

    if not args.path:
        parser.print_help()
        # print(parser)
        exit(0)
    else:
        trav = TravPro(args.path)
        trav.travel()
        trav.print_results()
