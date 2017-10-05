class BadCredentialsException(Exception):
    def __init__(self, email, key):
        super(BadCredentialsException, self).__init__('\n'.join([
            'Auth error',
            '-> Email: {}'.format(email),
            '-> Key: {}'.format(key)
        ]))
        self.email = email
        self.key = key


class TodoistException(Exception):
    pass


class ProjectNotFoundException(TodoistException):
    def __init__(self, project_name):
        super(ProjectNotFoundException, self).__init__('Project "{}" not found.'.format(project_name))
        self.project_name = project_name


class ItemAlreadyExistsException(TodoistException):
    def __init__(self, key):
        super(ItemAlreadyExistsException, self).__init__('Item with key "{}" already exists.'.format(key))
        self.item_key = key
