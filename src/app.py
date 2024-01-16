import json
import lucene
from flask import Flask, request
from flask_cors import CORS

from retrieval import index, search, util

INDEX_DIR = "./store"
DATA_DIR = "../data/"


app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/search", methods=["POST"])
def search_recipes():
    data = request.form

    name = data.get("name", "")
    include = data.get("include", "[]")
    if not name and include == "[]":
        return "Provide at least a name or an included ingredient", 400

    include = json.loads(include)
    if len(include) == 1 and not include[0]:
        return "Include has a wrong format", 400
    exclude = json.loads(data.get("exclude", "[]"))
    duration = data.get("duration", None)
    if duration is not None:
        duration = int(duration)
    rating = data.get("rating", None)
    if rating is not None:
        rating = int(rating)

    searcher, reader = search.get_searcher(INDEX_DIR)
    hits = search.query_recipes(
        searcher, name, include, exclude, duration, rating, limit=10)

    results = util.hits_to_json_response(searcher, hits, include)

    reader.close()
    return results


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
    duration = data.get("Duration", None)
    if duration is not None:
        duration = int(duration)
    rating = data.get("Rating", None)
    if rating is not None:
        rating = int(rating)

    searcher, reader = search.get_searcher(INDEX_DIR)

    hits = search.query_ingredients(
        searcher, include, exclude, duration, rating)
    results = util.hits_to_json_response(searcher, hits, include)

    reader.close()
    return results


# FORCE_REINDEX = True
FORCE_REINDEX = False

if __name__ == "__main__":
    lucene.initVM()
    if not index.has_index(INDEX_DIR) or FORCE_REINDEX:
        if FORCE_REINDEX:
            index.remove_index(INDEX_DIR)
        recipes = util.pq_to_df(DATA_DIR + "recipes.parquet",
                                list(util.RECIPE_COLUMNS.keys()))
        ratings = util.pq_to_df(DATA_DIR + "reviews.parquet",
                                list(util.RATINGS_COLUMNS.keys())).groupby([util.ID_COLUMN]).mean()

        # TODO: check if other 'how' method is better
        combined = recipes.join(ratings, on=util.ID_COLUMN, how="inner")
        index.index_data(combined, util.COLUMNS, INDEX_DIR)

    app.run(host="0.0.0.0")
