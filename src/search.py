import lucene
from java.io import File
from org.apache.lucene import analysis, index, queryparser, search, store


def get_index_dir():
    assert lucene.getVMEnv() or lucene.initVM()

    return store.FSDirectory.open(File("./store").toPath())


def get_searcher(index_dir):
    assert lucene.getVMEnv() or lucene.initVM()

    reader = index.DirectoryReader.open(index_dir)
    searcher = search.IndexSearcher(reader)
    return searcher


def get_analyzer():
    assert lucene.getVMEnv() or lucene.initVM()

    return analysis.en.EnglishAnalyzer()


def query_ingredients(
    searcher, include: list[str], exclude: list[str] = [], limit: int = 10
):
    assert lucene.getVMEnv() or lucene.initVM()

    parser = queryparser.classic.QueryParser(
        "RecipeIngredientParts", get_analyzer())

    include_handled = [x if len(x.split(" ")) ==
                       1 else f'"{x}"' for x in include]
    include_str = " OR ".join(include_handled)
    exclude_handled = [x if len(x.split(" ")) ==
                       1 else f'"{x}"' for x in exclude]
    query_str = f"({include_str})"
    for excluded in exclude_handled:
        query_str += f" AND NOT {excluded}"

    print(query_str)
    query = parser.parse(query_str)
    hits = searcher.search(query, limit).scoreDocs
    return hits
