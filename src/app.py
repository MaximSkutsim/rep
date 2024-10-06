import sys
import os
from typing import List
# Настройка пути к проекту
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from index_file import build_embedding_array, query_semantic
import uvicorn

app = FastAPI()

class Notes(BaseModel):
    """Model for notes."""
    notes: dict

class QuerySemanticRequest(BaseModel):
    """Model for query semantic request."""
    query: str
    embeddings: list
    n_results: int = 2
    threshold: float = 0.9

@app.post("/build_embeddings/")
async def build_embeddings(notes: Notes):
    try:
        embedding_array = build_embedding_array(notes.notes)
        return {"embeddings": embedding_array.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query_semantic/")
async def query_semantic_endpoint(request: QuerySemanticRequest):
    try:
        embeddings = np.array(request.embeddings)
        top_indices = query_semantic(
            request.query, 
            embeddings, 
            n_results=request.n_results, 
            threshold=request.threshold
        )
        return {"top_indices": top_indices.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def main() -> None:
    """Run application"""
    uvicorn.run("app:app", host="localhost")


if __name__ == "__main__":
    main()
