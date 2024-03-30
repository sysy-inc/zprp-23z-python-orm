import enum


class OperationType(enum.Enum):
    """Enum class for the type of operation that can be performed on a table or column."""

    CREATE = enum.auto()
    DELETE = enum.auto()
    RENAME = enum.auto()
    DTYPE_CHANGE = enum.auto()
    CONSTRAINT_CHANGE = enum.auto()
