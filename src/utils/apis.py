from youtrack import Connection, TokenAuth
import todoist

from .exceptions import *


class YouTrackApi:
    def _authorize(self, token, url, email):
        api = Connection(url, TokenAuth(token))
        if api.get_me()['email'] != email:
            raise BadCredentialsException(email, token)

        self._api = api

    def __init__(self, auth_token, tracker_url, user_email):
        self._authorize(auth_token, tracker_url, user_email)

    def get_tasks(self, max=10):
        filter = 'for: me #unresolved'

        return self._api.get_issues(filter, [], max)


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

    def __init__(self, user_email, api_key, project_name, label, default_priority):
        self._authorize(user_email, api_key)
        self._configure_target_project(project_name)
        self._configure_label(label)

        self._default_priority = default_priority

    def add_todo(self, key, title, comment=False, priority=False):
        self._api.sync()

        if key in [x['content'].split(' – ')[0]
                   for x in self._api.state['items']
                   if self._label_id in x['labels'] and not x['checked']
                   ]:
            raise ItemAlreadyExistsException(key)

        if not priority:
            priority = self._default_priority

        item = self._api.items.add(
            "{0} – {1}".format(key, title),
            self._target_project['id'],
            priority=priority,
            labels=[self._label_id]
        )

        if comment:
            note = self._api.notes.add(item['id'], comment)

        self._api.commit()
