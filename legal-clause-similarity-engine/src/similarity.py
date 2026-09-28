import numpy as np

from sklearn.metrics.pairwise import (
    cosine_similarity
)

from src.preprocess import (
    preprocess_text
)

from src.embed import (
    clause_to_vector
)


def find_similar_clauses(
        query,
        df,
        clause_vectors,
        model,
        top_k
):
    # --- NOTE ---
    # This middle section scrolled past between visible frames in the
    # recording, so it wasn't legible. Rebuilt here to match the
    # imports/variables used just above and below it (preprocess_text,
    # clause_to_vector, query_vector, "return []"). Double check this
    # part against your actual file.
    query_tokens = preprocess_text(query)
    query_vector = clause_to_vector(query_tokens, model)

    if not np.any(query_vector):
        return []
    # --- END NOTE ---

    query_vector = query_vector.reshape(1,-1)

    similarities = cosine_similarity(query_vector,clause_vectors)[0]

    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []

    for idx in top_indices:
        results.append({"clause":df.iloc[idx]["clause_text"],"clause_type":df.iloc[idx]["clause_type"],
                        "similarity_score":round(float(similarities[idx]),4)
                })


    return results