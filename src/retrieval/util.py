from org.apache.lucene import analysis, store
from java.io import File


INGREDIENT_COLUMN = "RecipeIngredientParts"


# Using this function to get th analyzer allows easily changing the analyzer
# used for the project.
def get_analyzer():
    return analysis.en.EnglishAnalyzer()


def get_index_dir(path: str):
    return store.FSDirectory.open(File(path).toPath())
