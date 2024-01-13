import lucene

lucene.initVM()

if __name__ == "__main__":
    print("Hello word")

    from lupyne import engine

    indexer = engine.Indexer('./index')

    # indexer.set('recipe_name', stored=True)
    # indexer.set('ingredients', engine.Field.Text)
    # # indexer.set('ingredients', engine.ShapeField)

    # indexer.add(recipe_name='sample', ingredients='hello world')
    # indexer.commit()

    indexer.set('name', stored=True)
    indexer.set('text', engine.Field.Text)
    indexer.add(name='sample', text='hello World')
    indexer.commit()

    hits = indexer.search('text:hello')
    print(len(hits), hits.count)
    (hit,) = hits
    print(hit['name'])
    print(hit.id, hit.score)
    print(hit.dict())

    # from org.apache.lucene.analysis.standard import StandardAnalyzer
    # from org.apache.lucene.document import Document, Field, StringField
    # from org.apache.lucene.index import IndexWriter, IndexWriterConfig
    # from org.apache.lucene.store import SimpleFSDirectory
    # from java.nio.file import Paths

    # def create_index(index_path, documents):
    #     analyzer = StandardAnalyzer()
    #     config = IndexWriterConfig(analyzer)
    #     directory = SimpleFSDirectory(Paths.get(index_path))
    #     writer = IndexWriter(directory, config)

    #     for doc_id, content in enumerate(documents):
    #         doc = Document()
    #         doc.add(StringField("id", str(doc_id), Field.Store.YES))
    #         doc.add(Field("content", content,
    #                 Field.Store.YES, Field.Index.ANALYZED))
    #         writer.addDocument(doc)

    #     writer.close()

    # # Example usage:
    # documents_to_index = [
    #     "This is the first document.",
    #     "Second document is here.",
    #     "And this is the third one."
    # ]

    # create_index("index_directory", documents_to_index)
