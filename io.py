import csv
import json
import yaml

from .formatting import *

def load_yaml_file(filename):
    try:
        with open(filename) as file:
            return yaml.load(file, Loader=yaml.FullLoader)
    except Exception:
        print_error('Could not read yaml file')
        raise

def write_yaml_file(data, filename):
    try:
        with open(filename, 'w') as file:
            yaml.dump(data, file)

    except Exception:
        print_error('Could not write yaml file: {}\n{}\n{}'.format(filename, data, e))
        raise

def _represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def get_input_map_from_csv(input_filename, has_header=True):
    input_map = {}

    with open(input_filename, 'rt') as csvfile:
        rows = csv.reader(csvfile, delimiter=',', quotechar='"')
        index = 0
        for row in rows:
            if has_header and index == 0:
                index = index + 1
                continue
            print(row)
            id_ = row[0] if _represents_int(row[0]) else row[1]
            name = row[1] if _represents_int(row[0]) and len(row) > 1 else row[0]

            if not _represents_int(id_):
                raise Exception('Bad RPM Id: {}'.format(id_))
            if not name:
                raise Exception('Bad Account Name: {}'.format(name))

            input_map[id_] = name

            index = index + 1

    # except Exception as e:
    #     print_error('Could not read input file: {}'.format(e))
    #     raise Exception('Trouble reading input file.')

    print_success('Account map: {}'.format(input_map))
    return input_map

def write_json_file(data, output_filename):
    try:
        with open(output_filename, 'w') as outfile:
            json.dump(data, outfile)
    except Exception as e:
        print_error('Error outputing file: {}.'.format(e))
        raise e

def read_json_file(filename):
    try:
        with open(filename) as json_file:
            return json.load(json_file)
    except Exception as e:
        print_error('Error reading json file: {}\n{}.'.format(filename,e))
        raise e
