# Hele dataset verwerken
import os
from datetime import datetime

import lucene
import pandas as pd
from org.apache.lucene import document, index
from pyarrow import Table
from pyarrow import parquet as pq
from retrieval.util import get_analyzer, get_index_dir, INGREDIENT_COLUMN

from util import pt_time_to_seconds

# Define the columns you would like to use
COLUMNS = {'RecipeId': int, 'Name': str,
           INGREDIENT_COLUMN: list, 'RecipeInstructions': list,
           "Images": list, "CookTime": datetime}


def has_index(path: str) -> bool:
    return os.path.isdir(path) and bool(len(os.listdir(path)))


def index_data(file_path: str, index_path: str) -> None:
    """
    Generates an index for the provided data
    Note: the data should be stored in a parquet file

    :param path: string to the parquet file
    """

    print(
        f"Writing data to index at '{index_path}' from '{file_path}'",
        flush=True
    )
    # Don't remove the index so that we can add to it???
    # if os.path.isdir(INDEX_DIR):
    #     shutil.rmtree(INDEX_DIR)

    assert lucene.getVMEnv() or lucene.initVM()
    env = lucene.getVMEnv()
    env.attachCurrentThread()

    # NOTE: Use the english analyzer to enable stemming.
    #       This can be usefull for searching the ingredients.
    #       'apples' and 'apple' will both match to 'apple'.
    analyzer = get_analyzer()

    # Directory to store the index
    directory = get_index_dir(index_path)
    config = index.IndexWriterConfig(analyzer)
    iwriter = index.IndexWriter(directory, config)

    table: Table = pq.read_table(file_path, columns=list(COLUMNS.keys()))

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

    print(f"'{file_path}' added to index", flush=True)
    iwriter.close()
    directory.close()
