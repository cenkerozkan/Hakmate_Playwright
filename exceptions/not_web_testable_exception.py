from typing import Text

class NotWebTestableException(Exception):
    def __init__(self, message: Text) -> None:
        self.message = message
        super().__init__(self.message)