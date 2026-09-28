import os
import pickle

from gensim.models import (
    Word2Vec
)


def save_pickle(obj, path):
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def load_pickle(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return []

    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except (EOFError, FileNotFoundError, pickle.UnpicklingError, ValueError):
        return []


def load_word2vec(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return None

    try:
        return Word2Vec.load(path)
    except (EOFError, FileNotFoundError, ValueError, AttributeError):
        return None