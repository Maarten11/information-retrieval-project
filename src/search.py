from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import SimpleFSDirectory
from java.nio.file import Paths


def search_index(index_path, query_str):
    directory = SimpleFSDirectory(Paths.get(index_path))
    searcher = IndexSearcher(directory)
    analyzer = StandardAnalyzer()

    query_parser = QueryParser("content", analyzer)
    query = query_parser.parse(query_str)

    hits = searcher.search(query, 10)

    for hit in hits.scoreDocs:
        doc = searcher.doc(hit.doc)
        print("Document ID:", doc.get("id"), "Score:", hit.score)


# Example usage:
search_index("index_directory", "document")
