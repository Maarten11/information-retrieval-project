import lucene
import index

lucene.initVM()

if __name__ == "__main__":
    index.index_data("./data/recipes.parquet")
    print("Hello world")
