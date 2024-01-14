# Hele dataset verwerken
from datetime import datetime
from org.apache.lucene import analysis, document, index, store
from java.io import File
import lucene
from pyarrow import Table, parquet as pq
import pandas as pd
import shutil
import os

from util import pt_time_to_seconds

INDEX_DIR = "./store"

# Define the columns you would like to use
COLUMNS = {'RecipeId': int, 'Name': str,
           'RecipeIngredientParts': list, 'RecipeInstructions': list,
           "Images": list, "CookTime": datetime}


def has_index() -> bool:
    return bool(len(os.listdir(INDEX_DIR)))


def index_data(path: str) -> None:
    """
    Generates an index for the provided data
    Note: the data should be stored in a parquet file

    :param path: string to the parquet file
    """

    print("Writing new index", flush=True)
    shutil.rmtree(INDEX_DIR)

    assert lucene.getVMEnv() or lucene.initVM()
    env = lucene.getVMEnv()
    env.attachCurrentThread()

    # NOTE: Use the english analyzer to enable stemming.
    #       This can be usefull for searching the ingredients.
    #       'apples' and 'apple' will both match to 'apple'.
    analyzer = analysis.en.EnglishAnalyzer()

    # Directory to store the index
    directory = store.FSDirectory.open(File(INDEX_DIR).toPath())
    config = index.IndexWriterConfig(analyzer)
    iwriter = index.IndexWriter(directory, config)

    table: Table = pq.read_table(path, columns=list(COLUMNS.keys()))

    pd_table: pd.DataFrame = table.to_pandas()

    for row in pd_table.itertuples():
        # Convert to dict
        recipe: dict = row._asdict()
        doc = document.Document()
        for key, value in recipe.items():
            # Skip index
            if key == 'Index':
                continue
            if value is None:
                # TODO: what to do with missing data?
                continue
            elif COLUMNS[key] == list:
                for v in value:
                    doc.add(document.Field(
                        key, v, document.StringField.TYPE_STORED))
            elif COLUMNS[key] == int:
                doc.add(document.IntPoint(key, int(value)))
                doc.add(document.Field(
                    key, value, document.StringField.TYPE_STORED))
            elif COLUMNS[key] == datetime:
                new_value = int(pt_time_to_seconds(value))
                doc.add(document.IntPoint(key, new_value))
                doc.add(document.Field(key, new_value,
                        document.StringField.TYPE_STORED))
            else:
                doc.add(document.Field(
                    key, value, document.TextField.TYPE_STORED))
        iwriter.addDocument(doc)

    print("New index written", flush=True)
    iwriter.close()
