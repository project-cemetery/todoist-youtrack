import json


def parse_parameters(parameters_file_name):
    with open(parameters_file_name, 'r', encoding='utf-8') as parameters:
        return json.load(parameters)
