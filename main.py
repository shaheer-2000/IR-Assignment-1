from lib.index_builder import IndexBuilder
from lib.query_handler import QueryRunner

print("Building Index")
index = IndexBuilder()
index.build_index("./Assignment-1/Abstracts", "./Assignment-1/Stopword-List.txt", "./outputs/index.pickle")

print("Index built")

print("\n\nEnter your queries in the following prompt.\nIf you wish to stop, type in ! while being prompted for input.\n\n")

qr = QueryRunner(index.index)

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
