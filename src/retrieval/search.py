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


def query_recipes(
    searcher, name: str, include: list[str], exclude: list[str] = [],
    duration_upper: int | None = None, rating_lower: int | None = None,
    limit: int = 10
):
    assert lucene.getVMEnv() or lucene.initVM()
    env = lucene.getVMEnv()
    env.attachCurrentThread()

    query = build_query(name, include, exclude, duration_upper, rating_lower)

    hits = searcher.search(query, limit).scoreDocs
    return hits


def build_include_query(include: list[str]):
    include_handled = []
    for x in include:
        if len(x.split(" ")) == 1:
            # Single terms are fuzzy matched
            fuzzy_str = f"{x}~"
            if len(x) < 5:
                # Short terms get a smaller allowed levenshtein distance.
                # This is to limit wrong matches.
                fuzzy_str += "1"
            include_handled.append(fuzzy_str)
        else:
            # Handle phrases.
            # Allow some slack in the distance between the terms.
            include_handled.append(f'"{x}"~1')
    # Terms are combined with an OR operator, because we are still interested
    # in recipes that contain some of the ingredients.
    query_str = " OR ".join(include_handled)

    parser = queryparser.classic.QueryParser(INGREDIENT_COLUMN, get_analyzer())
    return parser.parse(query_str)


def build_exclude_query(exclude: list[str]):
    exclude_handled = [
        # Once again handle phrases.
        # We don't do any fuzzy matching here,
        # because we don't want to exclude recipes by mistake.
        x if len(x.split(" ")) == 1 else f'"{x}"' for x in exclude
    ]
    query_str = " OR ".join(exclude_handled)

    parser = queryparser.classic.QueryParser(INGREDIENT_COLUMN, get_analyzer())
    return parser.parse(query_str)


def build_recipe_name_query(name: str):
    splitted = name.split(" ")
    for i in range(len(splitted)):
        s = splitted[i]
        distance = 2
        if len(s) < 2:
            distance = 0
        elif len(s) < 4:
            distance = 1
        # We want to allow fuzzy matching on the terms.
        # This allows some `correction` of spelling mistakes.
        # The allowed levenshtein distance depends on the length of the term.
        # Smaller terms have a smaller distance to limit wrong matches.
        # (And there is less place for spelling mistakes to happen here)
        splitted[i] = f"{s}~{distance}"
    query_str = f'"{" ".join(splitted)}"~3'

    parser = queryparser.complexPhrase.ComplexPhraseQueryParser(
        "Name", get_analyzer())
    return parser.parse(query_str)


def build_cooking_time_query(duration_upper: int):
    """
    @param duration_upper: The upper bound of the cooking time in seconds.
        Should be >= 0.
    """
    assert duration_upper >= 0
    return IntPoint.newRangeQuery("CookTime", 0, duration_upper)


def build_rating_query(rating_lower: int):
    """
    @param rating_lower: The lower bound of the rating.
        Should be >= 0.
    """
    assert rating_lower >= 0
    return IntPoint.newRangeQuery("Rating", rating_lower, 5)


def build_query(
    name: str, include: list[str], exclude: list[str] = [],
    duration_upper: int | None = None, rating_lower: int | None = None
):
    assert lucene.getVMEnv() or lucene.initVM()
    # At least one of the parameters should be set.
    assert name or include
    env = lucene.getVMEnv()
    env.attachCurrentThread()

    query_builder = search.BooleanQuery.Builder()
    if name:
        query_builder.add(build_recipe_name_query(name),
                          search.BooleanClause.Occur.MUST)
    if include:
        query_builder.add(build_include_query(include),
                          search.BooleanClause.Occur.MUST)
    if exclude:
        query_builder.add(build_exclude_query(exclude),
                          search.BooleanClause.Occur.MUST_NOT)
    if duration_upper is not None:
        query_builder.add(build_cooking_time_query(duration_upper),
                          search.BooleanClause.Occur.FILTER)
    if rating_lower is not None:
        query_builder.add(build_rating_query(rating_lower),
                          search.BooleanClause.Occur.FILTER)

    return query_builder.build()


def create_ingredient_query(
    include: list[str], exclude: list[str],
    duration_upper: int | None, rating_lower: int | None = None
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

    if query_str != "()":
        ingredients_query = parser.parse(query_str)
    # if duration_upper is None:
    #     return ingredients_query

    query_builder = search.BooleanQuery.Builder()
    if duration_upper is not None:
        dur_query = IntPoint.newRangeQuery("CookTime", 0, duration_upper)
        query_builder.add(dur_query, search.BooleanClause.Occur.FILTER)
    if rating_lower is not None:
        rating_query = IntPoint.newRangeQuery("Rating", rating_lower, 5)
        query_builder.add(rating_query, search.BooleanClause.Occur.FILTER)
    if query_str != "()":
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
