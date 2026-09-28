import os
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import nltk
from gensim.models import Word2Vec

nltk.download('stopwords', quiet=True)

from src.preprocess import preprocess_text

base_dir = Path(__file__).resolve().parent
project_root = base_dir.parent
csv_path = project_root / 'legal_docs.csv'
model_dir = base_dir / 'models'
model_dir.mkdir(exist_ok=True)

df = pd.read_csv(csv_path)
if 'clause_text' not in df.columns:
    raise ValueError('CSV must contain a clause_text column.')

df = df[['clause_text', 'clause_type']].dropna().reset_index(drop=True)
df['clause_text'] = df['clause_text'].astype(str)

sentences = [preprocess_text(text) for text in df['clause_text']]
sentences = [tokens for tokens in sentences if tokens]

if not sentences:
    raise ValueError('No valid clause text found in the CSV.')

model = Word2Vec(
    sentences=sentences,
    vector_size=100,
    window=5,
    min_count=1,
    workers=1,
    sg=1,
    epochs=20,
)
model.save(str(model_dir / 'word2vec.model'))

vectors = []
for tokens in sentences:
    word_vectors = [model.wv[word] for word in tokens if word in model.wv]
    if not word_vectors:
        vectors.append(np.zeros(model.vector_size, dtype=np.float32))
    else:
        vectors.append(np.mean(word_vectors, axis=0).astype(np.float32))

clause_vectors = np.vstack(vectors).astype(np.float32)

with open(model_dir / 'clause_vectors.pkl', 'wb') as f:
    pickle.dump(clause_vectors, f)

with open(model_dir / 'clauses.pkl', 'wb') as f:
    pickle.dump(df, f)

print(f'Generated model and vectors for {len(df)} clauses.')
print(f'Vector shape: {clause_vectors.shape}')
print(f'Model path: {model_dir / "word2vec.model"}')
