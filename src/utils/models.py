class Task:
    def __init__(self, key, title, comment=None, priority=1):
        self.key = key
        self.title = title
        self.comment = comment
        self.priority = priority

    def __str__(self):
        return '{0} – {1}'.format(self.key, self.title)

    def __repr__(self):
        return self.__str__()
