import json
import lucene
from flask import Flask, request
from flask_cors import CORS

from retrieval import index, search, util

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
    searcher, reader = search.get_searcher(INDEX_DIR)
    hits = search.query_recipe_name(searcher, name)
    results = util.hits_to_json_response(searcher, hits)
    reader.close()
    return results


@app.route("/search_ingredients", methods=["POST"])
def search_ingredients():
    data = request.form

    include = data.get("include", None)
    if include is None:
        return "At least give one ingredient", 400
    include = json.loads(include)
    exclude = json.loads(data.get("exclude", "[]"))
    name = data.get("Name", None)
    duration = data.get("Duration", None)
    rating = data.get("Rating", None)

    searcher, reader = search.get_searcher(INDEX_DIR)

    hits = search.query_ingredients(searcher, include, exclude)
    # storedFields = searcher.storedFields()
    # results = []
    # for hit in hits:
    #     hitDoc = storedFields.document(hit.doc)
    #     print(hitDoc.get("Name"))
    #     print(hit.score, hitDoc.getValues("RecipeIngredientParts"))
    #     recipe = {}
    #     for field in hitDoc.getFields():
    #         name = field.name()
    #         value = hitDoc.getValues(name)[0]
    #         if util.COLUMNS[name] == list and name != 'Images':
    #             value = value.split("., ")
    #         recipe[field.name()] = value
    #     results.append(recipe)
    results = util.hits_to_json_response(searcher, hits)

    print(results, type(results), flush=True)

    reader.close()
    return results


FORCE_REINDEX = True
# FORCE_REINDEX = False

if __name__ == "__main__":
    lucene.initVM()
    if not index.has_index(INDEX_DIR) or FORCE_REINDEX:
        recipes = util.pq_to_df("./data/recipes.parquet",
                                list(util.RECIPE_COLUMNS.keys()))
        ratings = util.pq_to_df("./data/reviews.parquet",
                                list(util.RATINGS_COLUMNS.keys())).groupby([util.ID_COLUMN]).mean()

        combined = recipes.join(ratings, on=util.ID_COLUMN)
        index.index_data(combined, util.COLUMNS, INDEX_DIR)

    app.run(host="0.0.0.0")
