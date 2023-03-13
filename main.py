from lib.index_builder import IndexBuilder
from lib.query_handler import QueryRunner

print("Building Index")
index = IndexBuilder()
index.build_index("./Assignment-1-Updated/CricketReviews/Dataset", "./Assignment-1-Updated/Stopword-List.txt", "./outputs/index.pickle")

print("Index built")

qr = QueryRunner(index.index)

if __name__ == "__main__":
    # Update this part for testing
    import sys
    from pathlib import Path
    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        VAL_PATH=Path("./Assignment-1-Updated/Gold Query-Set Boolean Queries.txt")
        with open(VAL_PATH, "r") as f:
            content = f.read()
        examples = content.strip().split("\n\n")
        for example in examples:
            query, result = example.split("\n")
            q = query.split("Example Query:")[1].strip()
            r = result.split("Result-Set:")[1].strip()
            r = list(map(lambda v: int(v), r.split(","))) if len(r) > 0 else []
            results = qr.run_query(q)
            matched = len(set(results).intersection(set(r))) == len(results)
            print(f"Query:\t{q}\nResult-Set:\t{r}\nObtained:\t{results}\nMatches:\t{matched}")
        exit(1)

    print("\n\nEnter your queries in the following prompt.\nIf you wish to stop, type in ! while being prompted for input.\n\n")
    print("Enter query: ")
    q = input()

    while q != "!":
        print("Running query: ", q)
        print("Result: ", qr.run_query(q))

        print("Do you wish to continue? [y/n]")
        q = input()
        if q.lower() != "y":
            break

        print("Enter query: ")
        q = input()
