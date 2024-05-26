from skibidi_orm.query_engine.operations.clauses import Eq


def test_properties_clause():
    cl = Eq("id", 2)
    assert cl.val == 2
    assert cl.col == "id"
    assert cl.type == Eq
