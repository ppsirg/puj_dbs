from franz.openrdf.query.query import QueryLanguage


def search(conn, query_string: str, headers: list):
    tuple_query = conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
    result = tuple_query.evaluate()
    response = []
    with result:
        print(result)
        for binding_set in result:
            dt = {h: str(binding_set.getValue(h)) for h in headers}
            print(dt)
            response.append(dt)
    return response