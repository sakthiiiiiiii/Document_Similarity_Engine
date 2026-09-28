import re
import string

try:
    import spacy
except ImportError:  # pragma: no cover
    spacy = None

try:
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words("english"))
except LookupError:  # pragma: no cover
    stop_words = {
        "a", "an", "the", "and", "or", "but", "if", "then", "else",
        "when", "while", "for", "from", "with", "without", "in", "on",
        "at", "by", "of", "to", "as", "is", "it", "its", "this", "that",
        "these", "those", "be", "been", "being", "am", "are", "was", "were",
        "do", "does", "did", "has", "have", "had", "not", "no", "yes", "can",
        "could", "should", "would", "may", "might", "must", "shall", "will"
    }

try:
    nlp = spacy.load("en_core_web_sm") if spacy is not None else None
except OSError:  # pragma: no cover
    nlp = None

legal_words = {
    "shall",
    "may",
    "must",
    "not",
    "without",
    "upon"
}

stop_words = stop_words - legal_words


def preprocess_text(text):

    if not isinstance(text, str):
        return []

    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    if nlp is not None:
        doc = nlp(text)
        tokens = [
            token.lemma_
            for token in doc
            if token.text not in stop_words
            and not token.is_punct
            and len(token.text) > 1
        ]
        return tokens

    tokens = re.findall(r"[a-z]+", text)
    return [
        token for token in tokens
        if token not in stop_words and len(token) > 1
    ]