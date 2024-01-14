import lucene
from org.apache.lucene import index, queryparser, search

from retrieval.util import get_analyzer, get_index_dir, INGREDIENT_COLUMN


def get_searcher(index_path: str):
    assert lucene.getVMEnv() or lucene.initVM()
    env = lucene.getVMEnv()
    env.attachCurrentThread()

    directory = get_index_dir(index_path)
    reader = index.DirectoryReader.open(directory)
    searcher = search.IndexSearcher(reader)
    return searcher, reader


def query_ingredients(
    searcher, include: list[str], exclude: list[str] = [], limit: int = 10
):
    assert lucene.getVMEnv() or lucene.initVM()
    env = lucene.getVMEnv()
    env.attachCurrentThread()

    query = create_ingredient_query(include, exclude)

    hits = searcher.search(query, limit).scoreDocs
    return hits


def create_ingredient_query(include: list[str], exclude: list[str]):
    assert lucene.getVMEnv() or lucene.initVM()
    env = lucene.getVMEnv()
    env.attachCurrentThread()

    # Query parser is used to easily use the same analyzer used for the index,
    # for better matching of the terms (stemming etc.).
    parser = queryparser.classic.QueryParser(INGREDIENT_COLUMN, get_analyzer())

    # Restructure phrases to phrase queries
    include_handled = [
        f"{x}~" if len(x.split(" ")) == 1 else f'"{x}"~1' for x in include
    ]
    include_str = " OR ".join(include_handled)
    exclude_handled = [
        x if len(x.split(" ")) == 1 else f'"{x}"' for x in exclude
    ]

    query_str = include_str
    if exclude:
        query_str = '(' + query_str + ')'
    for excluded in exclude_handled:
        query_str += f" AND NOT {excluded}"

    return parser.parse(query_str)
