import json

from utils.apis import TodoistApi, YouTrackApi
from utils.exceptions import ItemAlreadyExistsException


def parse_parameters():
    with open("../parameters.json", 'r', encoding='utf-8') as parameters:
        return json.load(parameters)


# script
params = parse_parameters()

todoistClient = TodoistApi(**params['todoist'])
youtrackClient = YouTrackApi(**params['youtrack'])

for task in youtrackClient.get_tasks():
    try:
        t = todoistClient.add_todo(task)
        print('Task was added: {}'.format(t))
    except ItemAlreadyExistsException as e:
        print(e)

print('\nAll done!')

