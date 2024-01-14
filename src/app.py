import json
import lucene
from flask import Flask, request
from flask_cors import CORS

from retrieval import index, search

INDEX_DIR = "./store"


app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/search_recipe", methods=["POST"])
def search_recipe():
    data = request.form
    name = data.get("Name", None)
    if name is None:
        return "Please provide a name", 400
    return "Hello World"


@app.route("/search_ingredients", methods=["POST"])
def search_ingredients():
    data = request.form
    print(data, flush=True)

    include = data.get("include", None)
    if include is None:
        return "At least give one ingredient", 400
    include = json.loads(include)
    print(include, type(include), flush=True)
    exclude = json.loads(data.get("exclude", "[]"))
    print(exclude, type(exclude), flush=True)
    name = data.get("Name", None)
    duration = data.get("Duration", None)
    rating = data.get("Rating", None)

    searcher, reader = search.get_searcher(INDEX_DIR)

    hits = search.query_ingredients(searcher, include, exclude)
    storedFields = searcher.storedFields()
    results = []
    for hit in hits:
        hitDoc = storedFields.document(hit.doc)
        print(hitDoc.get("Name"))
        print(hit.score, hitDoc.getValues("RecipeIngredientParts"))
        recipe = {}
        for field in hitDoc.getFields():
            name = field.name()
            value = hitDoc.getValues(name)[0]
            if index.COLUMNS[name] == list and name != 'Images':
                value = value.split("., ")
            recipe[field.name()] = value
        results.append(recipe)

    reader.close()
    return results


FORCE_REINDEX = False

if __name__ == "__main__":
    lucene.initVM()
    if not index.has_index(INDEX_DIR) or FORCE_REINDEX:
        index.index_data("./data/recipes.parquet", INDEX_DIR)

    app.run(host="0.0.0.0")
