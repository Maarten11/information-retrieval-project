import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

data_recipes = {
    "Name": [
        "Glass of milk",
        "Suggary milk",
        "Cake"
    ],
    "RecipeId": [-1, -2, -3],
    "RecipeIngredientParts": [
        ["milk"],
        ["milk", "sugar"],
        ["eggs", "flour", "sugar", "butter"]
    ],
    "RecipeInstructions": [
        ["Pour milk into glass."],
        ["Pour milk into glass.", "Add sugar."],
        ["Mix ingredients.", "Bake."]
    ],
    "Images": [
        [""],
        [""],
        [""]
    ],
    "CookTime": [
        "PT1M",
        "PT1M",
        "PT30M"
    ],
}

data_reviews = {
    "RecipeId": [-1, -2, -3],
    "Rating": [5, 2, 3],
}

df_recipes = pd.DataFrame(data_recipes)
df_reviews = pd.DataFrame(data_reviews)


t_recipes = pa.Table.from_pandas(df_recipes)
t_reviews = pa.Table.from_pandas(df_reviews)

pq.write_table(t_recipes, "../data/test_recipes.parquet")
pq.write_table(t_reviews, "../data/test_reviews.parquet")
