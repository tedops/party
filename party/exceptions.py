"""Party exceptions."""


class PartyError(Exception):
    """Party base exception."""


class UnknownQueryType(PartyError):
    """Query type is not supported."""
