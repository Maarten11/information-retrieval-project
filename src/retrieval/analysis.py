from retrieval.util import INGREDIENT_COLUMN


def explain_hit(searcher, query, hit):
    return searcher.explain(query, hit.doc)


def print_hit(searcher, hit, column):
    storedFields = searcher.storedFields()
    hitDoc = storedFields.document(hit.doc)
    print(hitDoc.get("Name"), hitDoc.getValues(INGREDIENT_COLUMN))
    print(hit.score)
