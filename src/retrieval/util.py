from datetime import datetime
import isodate
import lucene
from org.apache.lucene import analysis, store
from java.io import File
from pyarrow import parquet as pq
import pandas as pd


INGREDIENT_COLUMN = "RecipeIngredientParts"
IMAGES_COLUMN = "Images"
ID_COLUMN = "RecipeId"

# Define the columns you would like to use
RECIPE_COLUMNS = {ID_COLUMN: "int", 'Name': "str",
                  INGREDIENT_COLUMN: "list", 'RecipeInstructions': "list",
                  IMAGES_COLUMN: "list", "CookTime": "datetime"}

RATINGS_COLUMNS = {
    ID_COLUMN: "int", "Rating": "float"
}


def merge_dicts(d1: dict, d2: dict) -> dict:
    result = dict()
    result.update(d1)
    result.update(d2)
    return result


COLUMNS = merge_dicts(RECIPE_COLUMNS, RATINGS_COLUMNS)


def pq_to_df(path: str, columns: list[str]) -> pd.DataFrame:
    return pq.read_table(path, columns=columns).to_pandas()


def hits_to_json_response(searcher, hits) -> list:
    storedFields = searcher.storedFields()
    results = []
    for hit in hits:
        hitDoc = storedFields.document(hit.doc)
        recipe = {}
        for field in hitDoc.getFields():
            name = field.name()
            value = hitDoc.getValues(name)[0]
            if COLUMNS[name] == "list" and name != IMAGES_COLUMN:
                value = value.split("., ")
            recipe[field.name()] = value
        results.append(recipe)

    return results


def pt_time_to_seconds(pt_time: str) -> float:
    return isodate.parse_duration(pt_time).total_seconds()

# Using this function to get th analyzer allows easily changing the analyzer
# used for the project.


def get_analyzer():
    return analysis.en.EnglishAnalyzer()


def get_index_dir(path: str):
    return store.FSDirectory.open(File(path).toPath())
