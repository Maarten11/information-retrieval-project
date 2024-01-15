import lucene
from org.apache.lucene import index, queryparser, search
from org.apache.lucene.document import IntPoint
from retrieval.util import INGREDIENT_COLUMN, get_analyzer, get_index_dir


def get_searcher(index_path: str):
    assert lucene.getVMEnv() or lucene.initVM()
    env = lucene.getVMEnv()
    env.attachCurrentThread()

    directory = get_index_dir(index_path)
    reader = index.DirectoryReader.open(directory)
    searcher = search.IndexSearcher(reader)
    return searcher, reader


def query_ingredients(
    searcher, include: list[str], exclude: list[str] = [],
    duration_upper: int | None = None, rating_lower: int = 0, limit: int = 10
):
    assert lucene.getVMEnv() or lucene.initVM()
    env = lucene.getVMEnv()
    env.attachCurrentThread()

    query = create_ingredient_query(
        include, exclude, duration_upper, rating_lower)

    hits = searcher.search(query, limit).scoreDocs
    return hits


def create_ingredient_query(
    include: list[str], exclude: list[str], duration_upper: int | None, rating_lower: int = 0
):
    assert lucene.getVMEnv() or lucene.initVM()
    env = lucene.getVMEnv()
    env.attachCurrentThread()

    # Query parser is used to easily use the same analyzer used for the index,
    # for better matching of the terms (stemming etc.).
    parser = queryparser.classic.QueryParser(INGREDIENT_COLUMN, get_analyzer())

    # Restructure phrases to phrase queries
    include_handled = []
    for x in include:
        if len(x.split(" ")) == 1:
            fuzzy_str = f"{x}~"
            if len(x) < 5:
                fuzzy_str += "1"
            include_handled.append(fuzzy_str)
        else:
            include_handled.append(f'"{x}"~1')
    include_str = " OR ".join(include_handled)
    exclude_handled = [
        x if len(x.split(" ")) == 1 else f'"{x}"' for x in exclude
    ]
    query_str = '(' + include_str + ')'
    for excluded in exclude_handled:
        query_str += f" AND NOT {excluded}"

    ingredients_query = parser.parse(query_str)
    if duration_upper is None:
        return ingredients_query

    dur_query = IntPoint.newRangeQuery("CookTime", 0, duration_upper)
    rating_query = IntPoint.newRangeQuery("Rating", rating_lower, 5)

    query_builder = search.BooleanQuery.Builder()
    query_builder.add(dur_query, search.BooleanClause.Occur.FILTER)
    query_builder.add(rating_query, search.BooleanClause.Occur.FILTER)
    query_builder.add(ingredients_query, search.BooleanClause.Occur.MUST)
    query = query_builder.build()

    return query


def query_recipe_name(searcher, name: str, limit: int = 10):
    assert lucene.getVMEnv() or lucene.initVM()
    env = lucene.getVMEnv()
    env.attachCurrentThread()

    parser = queryparser.complexPhrase.ComplexPhraseQueryParser(
        "Name", get_analyzer())

    # Allow fuzzy matching on the terms
    splitted = name.split(" ")
    for i in range(len(splitted)):
        s = splitted[i]
        distance = 2
        if len(s) < 2:
            distance = 0
        elif len(s) < 4:
            distance = 1
        splitted[i] = f"{s}~{distance}"

    query_str = f'"{" ".join(splitted)}"'
    query = parser.parse(query_str)

    hits = searcher.search(query, limit).scoreDocs
    return hits
