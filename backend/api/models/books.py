import datetime
import enum

class Condition(enum.Enum):
    SLIGHTLY_WORN = 0
    MODERATELY_WORN = 1
    HEAVILY_WORN = 2


class Genre(enum.Enum):
    FICTION = 0
    NON_FICTION = 1
    

class Book(dict):
    def __init__(self, *args, **kwargs):
        args[0]['genre'] = Genre(args[0]['genre']).name
        super().__init__(*args, **kwargs)

class NewBook(Book):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class UsedBook(Book):
    def __init__(self, *args, **kwargs):
        args[0]['condition'] = Condition(args[0]['condition']).name
        super().__init__(*args, **kwargs)