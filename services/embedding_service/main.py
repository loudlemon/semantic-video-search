import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

app = FastAPI(title="Embedding Service", version="0.1.0")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")  # 384 dims


class EmbedRequest(BaseModel):
    text: str


class EmbedResponse(BaseModel):
    embedding: list[float]


@app.post("/embed-text", response_model=EmbedResponse)
def embed_text(req: EmbedRequest):
    vec = model.encode([req.text], normalize_embeddings=True)[0]
    return EmbedResponse(embedding=vec.tolist())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
