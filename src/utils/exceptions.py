class TodoistException(Exception):
    pass


class BadCredentialsException(TodoistException):
    def __init__(self, email, key):
        super(BadCredentialsException, self).__init__('\n'.join([
            'User not found',
            '-> Email: {0}'.format(email),
            '-> Key: {0}'.format(key)
        ]))
        self.email = email
        self.key = key


class ProjectNotFoundException(TodoistException):
    def __init__(self, project_name):
        super(ProjectNotFoundException, self).__init__('Project "{0}" not found.'.format(project_name))
        self.project_name = project_name


class ItemAlreadyExistsException(TodoistException):
    def __init__(self, key):
        super(ItemAlreadyExistsException, self).__init__('Item with key "{0}" already exists.'.format(key))
        self.item_key = key
