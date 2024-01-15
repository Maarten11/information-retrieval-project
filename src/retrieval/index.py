# Hele dataset verwerken
import math
import os
import shutil
from datetime import datetime

import numpy as np

import lucene
import pandas as pd
from org.apache.lucene import document, index
from pyarrow import Table
from pyarrow import parquet as pq
from retrieval.util import get_analyzer, get_index_dir, pt_time_to_seconds


def has_index(path: str) -> bool:
    return os.path.isdir(path) and bool(len(os.listdir(path)))


def remove_index(path: str):
    if os.path.isdir(path):
        shutil.rmtree(path)


def index_data(pd_table: pd.DataFrame, column_mapping: dict, index_path: str) -> None:
    """
    Generates an index for the provided data
    Note: the data should be stored in a parquet file

    :param path: string to the parquet file
    """
    assert lucene.getVMEnv() or lucene.initVM()
    env = lucene.getVMEnv()
    env.attachCurrentThread()
    print(
        f"Writing data to index at '{index_path}'",
        flush=True
    )

    # NOTE: Use the english analyzer to enable stemming.
    #       This can be usefull for searching the ingredients.
    #       'apples' and 'apple' will both match to 'apple'.
    analyzer = get_analyzer()

    # Directory to store the index
    directory = get_index_dir(index_path)
    config = index.IndexWriterConfig(analyzer)
    iwriter = index.IndexWriter(directory, config)

    # table: Table = pq.read_table(
    #     file_path, columns=list(RECIPE_COLUMNS.keys()))

    # pd_table: pd.DataFrame = table.to_pandas()

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
            elif key == "Images":
                if len(value):
                    doc.add(document.Field(
                        key, list(value)[0], document.TextField.TYPE_STORED
                    ))
            elif column_mapping[key] == "list":
                new_value = "., ".join(value)
                doc.add(document.Field(
                        key, new_value, document.TextField.TYPE_STORED))
                # doc.add(document.Field(
                #     key, test, document.TextField.TYPE_STORED))
            elif column_mapping[key] == "int":
                # NOTE: unused
                doc.add(document.IntPoint(key, int(value)))
                doc.add(document.Field(
                    key, value, document.StringField.TYPE_STORED))
            elif column_mapping[key] == "datetime":
                new_value = int(pt_time_to_seconds(value))
                # New
                # point = document.IntPoint(key, new_value)
                # type = document.FieldType(point.fieldType())
                # type.setStored(True)
                # doc.add(document.Field(point.name(), new_value, type))
                # Old
                doc.add(document.IntPoint(key, new_value))
                doc.add(document.Field(key, new_value,
                        document.StringField.TYPE_STORED))
            elif column_mapping[key] == "float":
                if np.isnan(value):
                    continue
                v = math.floor(value + 0.5)
                doc.add(document.IntPoint(key, v))
                doc.add(document.Field(key, v,
                        document.StringField.TYPE_STORED))
            else:
                doc.add(document.Field(
                    key, value, document.TextField.TYPE_STORED))
        iwriter.addDocument(doc)

    print(f"added to index", flush=True)
    iwriter.close()
    directory.close()
