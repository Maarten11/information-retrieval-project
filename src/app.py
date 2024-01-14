from flask import Flask, jsonify, request
from flask_cors import CORS
import lucene
import index
import search

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/search_recipe", methods=["POST"])
def search_recipe():
    data = request.form
    print(data, flush=True)

    include = data.get("include", None)
    if include is None:
        return {"message": "At least give one ingredient", "status": 400}

    searcher = search.get_searcher(search.get_index_dir())

    hits = search.query_ingredients(searcher, ["milk", "eggs"])
    storedFields = searcher.storedFields()
    results = []
    for hit in hits:
        hitDoc = storedFields.document(hit.doc)
        print(hitDoc.get("Name"))
        print(hit.score, hitDoc.getValues("RecipeIngredientParts"))
        recipe = {}
        for field in hitDoc.getFields():
            name = field.name()
            value = hitDoc.getValues(name)
            # Extract real type
            if index.COLUMNS[name] == list and name != "Images":
                value = list(value)
            else:
                value = list(value)[0]
            recipe[field.name()] = value
        results.append(recipe)

    return results


if __name__ == "__main__":
    lucene.initVM()
    if not index.has_index():
        index.index_data("./data/recipes.parquet")

    app.run(host="0.0.0.0")
