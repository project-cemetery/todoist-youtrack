import json

from utils.apis import TodoistApi


def parse_parameters():
    with open("../parameters.json", 'r', encoding='utf-8') as parameters:
        return json.load(parameters)


# script
params = parse_parameters()

client = TodoistApi(**params['todoist'])

client.add_todo('QS-42', 'Text', priority=3)
