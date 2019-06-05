import datetime
import enum

class Condition(enum.Enum):
    HEAVILY_WORN = 2
    MODERATELY_WORN = 1
    SLIGHTLY_WORN = 0

class Book(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NewBook(Book):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class UsedBook(Book):
    def __init__(self, *args, **kwargs):
        args[0]['condition'] = Condition(args[0]['condition']).name
        super().__init__(*args, **kwargs)