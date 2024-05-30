class AmbigiousDeleteRowError(Exception):
    """Thrown after more than one row is found in the database
    when trying to delete a row with a given primary key subset"""
