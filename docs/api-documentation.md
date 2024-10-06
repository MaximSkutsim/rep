# Semantic Notes Search API Documentation

This document provides detailed information about the REST API endpoints available in the Semantic Notes Search application.

## Base URL

All endpoints are relative to the base URL: `http://localhost:8000`

## Authentication

Currently, the API does not require authentication. This may change in future versions.

## API Endpoints

### Build Embeddings

Generate embeddings for a collection of notes using the E5-small-v2 model.

**Endpoint**: `POST /build_embeddings/`

**Request Body**:
```json
{
    "notes": {
        "note1": {
            "title": "Example Title",
            "content": "Example content of the note"
        },
        "note2": {
            "title": "Another Title",
            "content": "More content here"
        }
    }
}
```

**Response**:
```json
{
    "embeddings": [[0.1, 0.2, ...], [0.3, 0.4, ...]]
}
```

**Status Codes**:
- `200 OK`: Embeddings successfully generated
- `500 Internal Server Error`: Error during embedding generation

### Query Semantic Search

Perform semantic search across notes using a query string.

**Endpoint**: `POST /query_semantic/`

**Request Body**:
```json
{
    "query": "search query text",
    "embeddings": [[0.1, 0.2, ...], [0.3, 0.4, ...]],
    "n_results": 2,
    "threshold": 0.9
}
```

**Parameters**:
- `query` (string, required): The search query text
- `embeddings` (array, required): Pre-computed embeddings array
- `n_results` (integer, optional): Number of results to return (default: 2)
- `threshold` (float, optional): Similarity threshold (default: 0.9)

**Response**:
```json
{
    "top_indices": [1, 4]
}
```

**Status Codes**:
- `200 OK`: Search completed successfully
- `500 Internal Server Error`: Error during search operation

## Data Models

### Notes Model
```json
{
    "notes": {
        "type": "object",
        "properties": {
            "note_id": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["title", "content"]
            }
        }
    }
}
```

### QuerySemanticRequest Model
```json
{
    "query": "string",
    "embeddings": "array",
    "n_results": "integer",
    "threshold": "float"
}
```

## Example Usage

### Python
```python
import requests
import json

# Example notes
notes = {
    "notes": {
        "note1": {
            "title": "Python Programming",
            "content": "Python is a versatile programming language."
        }
    }
}

# Generate embeddings
response = requests.post(
    "http://localhost:8000/build_embeddings/",
    json=notes
)
embeddings = response.json()["embeddings"]

# Perform semantic search
search_request = {
    "query": "programming languages",
    "embeddings": embeddings,
    "n_results": 2,
    "threshold": 0.9
}

response = requests.post(
    "http://localhost:8000/query_semantic/",
    json=search_request
)
results = response.json()["top_indices"]
```

### cURL
```bash
# Generate embeddings
curl -X POST "http://localhost:8000/build_embeddings/" \
     -H "Content-Type: application/json" \
     -d '{"notes":{"note1":{"title":"Example","content":"Content"}}}'

# Perform semantic search
curl -X POST "http://localhost:8000/query_semantic/" \
     -H "Content-Type: application/json" \
     -d '{"query":"search text","embeddings":[[0.1,0.2]],"n_results":2,"threshold":0.9}'
```

## Error Handling

The API uses standard HTTP status codes for error responses. Error responses include a detail message explaining the error:

```json
{
    "detail": "Error message description"
}
```

Common error codes:
- `400 Bad Request`: Invalid input data
- `500 Internal Server Error`: Server-side error

## Rate Limiting

Currently, there are no rate limits implemented. This may change in future versions.

## Notes

1. The embedding model used is E5-small-v2 from Hugging Face.
2. Embeddings are normalized before similarity calculation.
3. The threshold parameter can be adjusted to control the strictness of semantic matching.



