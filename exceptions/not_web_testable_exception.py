from typing import Text

class NotWebTestableException(Exception):
    def __init__(
            self,
            message: Text = "Decorated method can only take testable Page objects!"
    ) -> None:
        self.message = message
        super().__init__(self.message)