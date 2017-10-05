import json

from utils.apis import TodoistApi, YouTrackApi


def parse_parameters():
    with open("../parameters.json", 'r', encoding='utf-8') as parameters:
        return json.load(parameters)


# script
params = parse_parameters()

todoistClient = TodoistApi(**params['todoist'])
youtrackClient = YouTrackApi(**params['youtrack'])

print(youtrackClient.get_tasks(20))


# todoistClient.add_todo('QS-42', 'Text', priority=3)
