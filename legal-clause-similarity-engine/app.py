from fastapi import FastAPI
from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

from src.utils import (
    load_pickle,
    load_word2vec
)

try:
    from src.similarity import (
        find_similar_clauses
    )
except Exception:  # pragma: no cover
    find_similar_clauses = None

app = FastAPI()

templates = Jinja2Templates(
    directory="templates"
)

model = load_word2vec(
    "models/word2vec.model"
)

clause_vectors = load_pickle(
    "models/clause_vectors.pkl"
)

df = load_pickle(
    "models/clauses.pkl"
)


@app.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "results": []
        }
    )


@app.post(
    "/search",
    response_class=HTMLResponse
)
def search(
        request: Request,
        query: str = Form(...)):

    if model is None or clause_vectors is None or len(clause_vectors) == 0 or df is None or len(df) == 0 or find_similar_clauses is None:
        return templates.TemplateResponse(
            request,
            "index.html",
            {
                "results": [],
                "query": query
            }
        )

    results = find_similar_clauses(
        query=query,
        model=model,
        clause_vectors=clause_vectors,
        df=df,
        top_k=5
    )

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "results": results,
            "query": query
        }
    )