import shutil

from retrieval import analysis, index, search
from retrieval import util

DATA_DIR = '../data/'
INDEX_DIR = '../.test_index/'

# recipes = util.pq_to_df(DATA_DIR + "recipes.parquet",
#                         list(util.RECIPE_COLUMNS.keys()))
# index.index_data(recipes, util.RECIPE_COLUMNS, INDEX_DIR)
recipes = util.pq_to_df(DATA_DIR + "recipes.parquet",
                        list(util.RECIPE_COLUMNS.keys()))
ratings = util.pq_to_df(DATA_DIR + "reviews.parquet",
                        list(util.RATINGS_COLUMNS.keys())).groupby([util.ID_COLUMN]).mean()

# TODO: check if other 'how' method is better
combined = recipes.join(ratings, on=util.ID_COLUMN, how="inner")
index.index_data(combined, util.COLUMNS, INDEX_DIR)

recipes = util.pq_to_df(DATA_DIR + "test_recipes.parquet",
                        list(util.RECIPE_COLUMNS.keys()))
ratings = util.pq_to_df(DATA_DIR + "test_reviews.parquet",
                        list(util.RATINGS_COLUMNS.keys())).groupby([util.ID_COLUMN]).mean()

# TODO: check if other 'how' method is better
combined = recipes.join(ratings, on=util.ID_COLUMN, how="inner")
index.index_data(combined, util.COLUMNS, INDEX_DIR)

searcher, reader = search.get_searcher(INDEX_DIR)

print()
print("########## Searching for name: 'glass milk' ##########")
name = "glass milk"
include = []
exclude = []
duration = None
rating = None

query = search.build_query(name, include, exclude, duration, rating)
results = search.query_recipes(
    searcher, name, include, exclude, duration, rating, limit=15)

for hit in results:
    analysis.print_hit(searcher, hit)

print()
print("########## Searching for name: 'glass milk' rating: 5 ##########")
name = "glass milk"
include = []
exclude = []
duration = None
rating = 5

query = search.build_query(name, include, exclude, duration, rating)
results = search.query_recipes(
    searcher, name, include, exclude, duration, rating, limit=15)

for hit in results:
    analysis.print_hit(searcher, hit)

print()
print("########## Searching for name: 'glass milk' duration: 500  ##########")
name = "glass milk"
include = []
exclude = []
duration = 500
rating = None

query = search.build_query(name, include, exclude, duration, rating)
results = search.query_recipes(
    searcher, name, include, exclude, duration, rating, limit=15)

for hit in results:
    analysis.print_hit(searcher, hit)

print()
print("########## Searching for name: 'milk' ##########")
name = "milk"
include = []
exclude = []
duration = None
rating = None

query = search.build_query(name, include, exclude, duration, rating)
results = search.query_recipes(
    searcher, name, include, exclude, duration, rating, limit=15)

for hit in results:
    analysis.print_hit(searcher, hit)

print()
print("########## Searching for name: 'milk' exclude: 'sugar' ##########")
name = "milk"
include = []
exclude = ["sugar"]
duration = None
rating = None

query = search.build_query(name, include, exclude, duration, rating)
results = search.query_recipes(
    searcher, name, include, exclude, duration, rating, limit=15)

for hit in results:
    analysis.print_hit(searcher, hit)

print()
print("########## Searching for ingredient: 'milk' ##########")
name = ""
include = ["milk"]
exclude = []
duration = None
rating = None

query = search.build_query(name, include, exclude, duration, rating)
# print(query)
results = search.query_recipes(
    searcher, name, include, exclude, duration, rating, limit=15)

for hit in results:
    analysis.print_hit(searcher, hit)

print()
print("########## Searching for ingredient: 'milk', 'sugar' ##########")
name = ""
include = ["milk", "sugar"]
exclude = []
duration = None
rating = None

query = search.build_query(name, include, exclude, duration, rating)
# print(query)
results = search.query_recipes(
    searcher, name, include, exclude, duration, rating, limit=15)

for hit in results:
    analysis.print_hit(searcher, hit)

print()
print("########## Searching for ingredient: 'sugar', egg', 'flour', 'butter' ##########")
name = ""
include = ["flour", "sugar", "butter", "egg"]
exclude = []
duration = None
rating = None

query = search.build_query(name, include, exclude, duration, rating)
# print(query)
results = search.query_recipes(
    searcher, name, include, exclude, duration, rating, limit=15)

for hit in results:
    analysis.print_hit(searcher, hit)

print()
print("########## Searching for ingredient: 'sugar', egg', 'flour', 'buter' ##########")
name = ""
include = ["flour", "sugar", "buter", "egg"]
exclude = []
duration = None
rating = None

query = search.build_query(name, include, exclude, duration, rating)
# print(query)
results = search.query_recipes(
    searcher, name, include, exclude, duration, rating, limit=15)

for hit in results:
    analysis.print_hit(searcher, hit)

print()
print("########## Searching for name: 'cookie' ingredient: 'sugar', egg', 'flour', 'butter' ##########")
name = "Cookie"
include = ["flour", "sugar", "butter", "egg"]
exclude = []
duration = None
rating = None

query = search.build_query(name, include, exclude, duration, rating)
results = search.query_recipes(
    searcher, name, include, exclude, duration, rating, limit=15)

for hit in results:
    analysis.print_hit(searcher, hit)

shutil.rmtree(INDEX_DIR, ignore_errors=True)
