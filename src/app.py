import lucene
import index
import search

lucene.initVM()

if __name__ == "__main__":
    # index.index_data("./data/recipes.parquet")

    searcher = search.get_searcher(search.get_index_dir())

    hits = search.query_ingredients(searcher, ["milk", "eggs"])
    print(len(hits))
    storedFields = searcher.storedFields()
    for hit in hits:
        hitDoc = storedFields.document(hit.doc)
        print(hitDoc.get("Name"))
        print(hit.score, hitDoc.getValues("RecipeIngredientParts"))
