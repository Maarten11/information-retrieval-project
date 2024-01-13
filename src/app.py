import lucene

lucene.initVM()

if __name__ == "__main__":
    from lupyne import engine

    indexer = engine.Indexer('./index')

    indexer.set('name', stored=True)
    indexer.set("image", stored=True)
    indexer.set('ingredients', engine.Field.String, stored=True)
    indexer.add(name="sample", image="test", ingredients="ui")
    indexer.add(name="sample1", image="test1", ingredients="ui look")
    indexer.add(name="sample2", image="test2", ingredients="ei look")
    indexer.commit()

    hits = indexer.search("ingredients:ui")
    print(hits)
    for hit in hits:
        print(hit['name'])
        print(hit.id, hit.score)
        print(hit.dict())
