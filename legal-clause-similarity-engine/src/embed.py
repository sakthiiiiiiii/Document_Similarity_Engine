import numpy as np


def clause_to_vector(tokens, model):

    vectors = [
        model.wv[word]
        for word in tokens
        if word in model.wv
    ]

    if not vectors:
        return np.zeros(
            model.vector_size
        )

    doc_vector = np.mean(
        vectors,
        axis=0
    )

    norm = np.linalg.norm(
        doc_vector
    )

    if norm == 0:
        return doc_vector

    return doc_vector / norm