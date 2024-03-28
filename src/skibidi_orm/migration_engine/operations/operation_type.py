import enum


class OperationType(enum.Enum):
    """Enum class for the type of operation that can be performed on a table or column."""

    CREATE = enum.auto()
    DELETE = enum.auto()
    ALTER = enum.auto()
    RENAME = enum.auto()
