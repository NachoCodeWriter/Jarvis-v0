import os

def search_files(directory, query):

    results = []

    query_words = query.lower().split()

    for root, dirs, files in os.walk(directory):

        for file in files:

            filename = file.lower()

            if any(word in filename for word in query_words):

                results.append(
                    os.path.join(root, file)
                )

    return results[:20]
