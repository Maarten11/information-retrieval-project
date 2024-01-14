from datetime import datetime
import isodate
import lucene
from org.apache.lucene import analysis, store
from java.io import File


INGREDIENT_COLUMN = "RecipeIngredientParts"

# Define the columns you would like to use
COLUMNS = {'RecipeId': int, 'Name': str,
           INGREDIENT_COLUMN: list, 'RecipeInstructions': list,
           "Images": list, "CookTime": datetime}


def hits_to_json_response(searcher, hits) -> list:
    storedFields = searcher.storedFields()
    results = []
    for hit in hits:
        hitDoc = storedFields.document(hit.doc)
        recipe = {}
        for field in hitDoc.getFields():
            name = field.name()
            value = hitDoc.getValues(name)[0]
            if COLUMNS[name] == list and name != 'Images':
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
