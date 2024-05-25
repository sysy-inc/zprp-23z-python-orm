from skibidi_orm.migration_engine.revisions.revision import Revision


class RevisionManager:
    """Class responsible for moving between revisions"""

    def __init__(self):
        # todo : get all revisions and store them in a list
        ...

    def find_revision_table(self) -> bool:
        """Used to find the revision table with the name
        specified by the user. Returns True if found,
        False otherwise"""
        raise NotImplementedError()

    def create_revision_table(self) -> None:
        """If the revision table is not found when migrating,
        this is called to create it"""
        raise NotImplementedError()

    def save_revision(self, revision: Revision) -> None:
        """Saves a given revision to the revision database"""
        raise NotImplementedError()

    def get_all_revisions(self) -> list[Revision]:
        """Returns all revisions in the database"""
        raise NotImplementedError()

    def go_to_revision(self, revision_id: int) -> None:
        """Checkouts the user to a given revision.
        THIS SHOULD BE ONLY PERFORMED ON AN EMPTY TABLE!"""
        raise NotImplementedError()

    def get_revision_by_id(self, revision_id: int) -> None:
        """Returns a revision object by its id. If not found,
        throws an exception"""
        raise NotImplementedError()

    def get_revision_SQL(self, revision: Revision) -> str:
        """Returns the SQL string, the execution of which
        will result in checkouting the revision"""
        raise NotImplementedError()
