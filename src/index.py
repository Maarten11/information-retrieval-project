# Hele dataset verwerken
from org.apache.lucene import analysis, document, index, store
from java.io import File
import lucene
from pyarrow import Table, parquet as pq
import pandas as pd
import shutil


def index_data(path: str) -> None:
    """
    Generates an index for the provided data
    Note: the data should be stored in a parquet file

    :param path: string to the parquet file
    """

    shutil.rmtree("./store")

    assert lucene.getVMEnv() or lucene.initVM()

    # Define the columns you would like to use
    COLUMNS = {'RecipeId': int, 'Name': str,
               'RecipeIngredientParts': list, 'RecipeInstructions': list}

    # NOTE: Use the english analyzer to enable stemming.
    #       This can be usefull for searching the ingredients.
    #       'apples' and 'apple' will both match to 'apple'.
    analyzer = analysis.en.EnglishAnalyzer()

    # Directory to store the index
    directory = store.FSDirectory.open(File("./store").toPath())
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
            elif COLUMNS[key] == list:
                for v in value:
                    doc.add(document.Field(
                        key, v, document.TextField.TYPE_STORED))
            else:
                doc.add(document.Field(
                    key, value, document.TextField.TYPE_STORED))
        iwriter.addDocument(doc)

    iwriter.close()


# # Analyzes the data???
# # analyzer = analysis.standard.StandardAnalyzer()
# ##########
# # NOTE: Use the english analyzer to enable stemming.
# #       This can be usefull for searching the ingredients.
# #       'apples' and 'apple' will both match to 'apple'.
# analyzer = analysis.en.EnglishAnalyzer()

# # Directory to store the index
# directory = store.FSDirectory.open(File("./store").toPath())
# config = index.IndexWriterConfig(analyzer)
# iwriter = index.IndexWriter(directory, config)

# table: Table = pq.read_table(
#     "./data/recipes.parquet",
#     columns=["RecipeId", "Name", "RecipeIngredientParts", "RecipeInstructions"],
# )

# pd_table: pd.DataFrame = table.to_pandas()
# print(pd_table.head(10))

# for row in pd_table.itertuples():
#     print(row)
#     doc = document.Document()
#     doc.add(document.Field(""))

# return


# doc1 = document.Document()
# doc2 = document.Document()
# doc3 = document.Document()
# doc4 = document.Document()
# doc5 = document.Document()
# doc6 = document.Document()
# text1 = "This is the text to be indexed."
# text2 = "This is a test. Should not appear."
# text3 = "When will this text appear? Here is more text for you."
# text4 = "Hey, texting is all I do."
# text5 = "Texts is something right?"
# text6 = ["This", "is", "a", "list", "of", "words", "not", "a", "text"]
# doc1.add(document.Field("fieldname", text1, document.TextField.TYPE_STORED))
# doc2.add(document.Field("fieldname", text2, document.TextField.TYPE_STORED))
# doc3.add(document.Field("fieldname", text3, document.TextField.TYPE_STORED))
# doc4.add(document.Field("fieldname", text4, document.TextField.TYPE_STORED))
# doc5.add(document.Field("fieldname", text5, document.TextField.TYPE_STORED))
# for word in text6:
#     doc6.add(document.Field("fieldname", word,
#                             document.TextField.TYPE_STORED))
# iwriter.addDocument(doc1)
# iwriter.addDocument(doc2)
# iwriter.addDocument(doc3)
# iwriter.addDocument(doc4)
# iwriter.addDocument(doc5)
# iwriter.addDocument(doc6)
# iwriter.close()


# # from org.apache.lucene.analysis.standard import StandardAnalyzer
# # from org.apache.lucene.document import Document, Field, StringField
# # from org.apache.lucene.index import IndexWriter, IndexWriterConfig
# # from org.apache.lucene.store import SimpleFSDirectory
# # from java.nio.file import Paths


# # def create_index(index_path, documents):
# #     analyzer = StandardAnalyzer()
# #     config = IndexWriterConfig(analyzer)
# #     directory = SimpleFSDirectory(Paths.get(index_path))
# #     writer = IndexWriter(directory, config)

# #     for doc_id, content in enumerate(documents):
# #         doc = Document()
# #         doc.add(StringField("id", str(doc_id), Field.Store.YES))
# #         doc.add(Field("content", content, Field.Store.YES, Field.Index.ANALYZED))
# #         writer.addDocument(doc)

# #     writer.close()


# # # Example usage:
# # documents_to_index = [
# #     "This is the first document.",
# #     "Second document is here.",
# #     "And this is the third one."
# # ]

# # create_index("index_directory", documents_to_index)
