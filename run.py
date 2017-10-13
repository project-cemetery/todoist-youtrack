from src.apis import TodoistApi, YouTrackApi
from src.exceptions import ItemAlreadyExistsException
from src.parameters import parse_parameters


# script
params = parse_parameters("parameters.json")

todoistClient = TodoistApi(**params['todoist'])
youtrackClient = YouTrackApi(**params['youtrack'])

for task in youtrackClient.get_tasks():
    try:
        t = todoistClient.add_todo(task)
        print('Task was added: {}'.format(t))
    except ItemAlreadyExistsException as e:
        print(e)

print('\nAll done!')

