class IrreversibleOperationError(TypeError):
    """Error thrown after an attempt to reverse an irreversible
    database operation"""


class UnsupportedOperationError(ValueError):
    """Error thrown after an attempt to convert or perform an operation
    unsupported by the current adapter or converter"""
