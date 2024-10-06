# Semantic Notes Search

A FastAPI-based application for semantic search in text notes using modern transformer models. The project allows users to manage notes and perform semantic similarity searches across their content.

## Features

- Create, update, and delete text notes
- Generate semantic embeddings for notes using the E5-small-v2 model
- Perform semantic similarity search across notes
- Visualize semantic relationships between notes using graph visualization
- RESTful API for all operations

## Technical Stack

- Python 3.8+
- FastAPI
- PyTorch
- Transformers (Hugging Face)
- NetworkX
- Scikit-learn
- NumPy

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/semantic-notes-search.git
cd semantic-notes-search
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the FastAPI server:
```bash
python src/app.py
```

2. The API will be available at `http://localhost:8000`

3. API endpoints:
- POST `/build_embeddings/` - Generate embeddings for notes
- POST `/query_semantic/` - Perform semantic search

## API Documentation

After starting the server, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

- `src/` - Source code directory
  - `app.py` - FastAPI application and endpoints
  - `index_file.py` - Semantic embedding and search functionality
  - `notes_processing.py` - Note management operations
  - `visualization.py` - Graph visualization tools
- `tests/` - Test files
- `docs/` - Documentation
- `examples/` - Example usage scripts

## License

This project is licensed under the MIT License - see the LICENSE file for details.
