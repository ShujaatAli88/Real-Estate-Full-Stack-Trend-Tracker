class DataAPIRequestError(Exception):
    """handles error while making requests to Data API."""
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)