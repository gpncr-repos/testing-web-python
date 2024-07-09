class ServiceError(Exception):
    """Service error."""


class CannotDivideByZeroError(ServiceError):
    """Cannot divide by zero error."""

    def __init__(self):
        self.msg = "Cannot divide by zero!"
