class MissingDatabaseConfiguration(Exception):
    """Exception raised when no database configuration is set.
    """

    def __init__(self, message="Database configuration is missing"):
        self.message = message


class FaultyDatabaseConfiguration(Exception):
    """Exception raised when database is incomplete or contains invalid values
    """

    def __init__(self, message="Database configuration is faulty"):
        self.message = message
