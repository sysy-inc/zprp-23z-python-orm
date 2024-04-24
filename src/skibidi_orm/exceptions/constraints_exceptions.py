class UnsupportedConstraintError(ValueError):
    """Thrown after an attempt to convert a constraint unsupported by
    a given database adapter to a SQL string specific for this adapter"""
