from skibidi_orm.query_engine.operations.functions import Count


def test_count():
    c = Count("id")
    assert c.column == "id"
    assert c.type == Count
