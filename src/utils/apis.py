from youtrack import Connection, TokenAuth
import todoist

from .exceptions import *
from .models import Task


class YouTrackApi:
    def _authorize(self, token, url, email):
        api = Connection(url, TokenAuth(token))
        if api.get_me()['email'] != email:
            raise BadCredentialsException(email, token)

        self._api = api

    def __init__(self, auth_token, tracker_url, user_email):
        self._authorize(auth_token, tracker_url, user_email)

    def get_tasks(self, count=10):
        filter_query = 'for:me state:Open, {In Progress}'
        issues = self._api.get_issues([filter_query], [], count)

        return [Task(i['id'], i['summary']) for i in issues]


class TodoistApi:
    def _authorize(self, email, key):
        api = todoist.api.TodoistAPI(key)
        api.sync()

        if not api.state['user'].get('email', False):
            raise BadCredentialsException(email, api_key)

        self._api = api

    def _configure_target_project(self, project_name):
        for project in self._api.state['projects']:
            if project['name'] == project_name:
                break
        else:
            raise ProjectNotFoundException(target_project_name)

        self._target_project = project

    def _configure_label(self, label):
        label = self._api.labels.add(label)
        self._api.commit()

        self._label_id = label['id']

    def __init__(self, user_email, api_key, project_name, label):
        self._authorize(user_email, api_key)
        self._configure_target_project(project_name)
        self._configure_label(label)

    def add_todo(self, task):
        self._api.sync()

        if task.key in [x['content'].split(' – ')[0]
                   for x in self._api.state['items']
                   if self._label_id in x['labels'] and not x['checked']
                   ]:
            raise ItemAlreadyExistsException(task.key)

        item = self._api.items.add(
            "{0} – {1}".format(task.key, task.title),
            self._target_project['id'],
            priority=task.priority,
            labels=[self._label_id]
        )

        if task.comment:
            note = self._api.notes.add(item['id'], task.comment)

        self._api.commit()

        return task
