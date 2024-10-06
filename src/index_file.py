import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

def build_embedding_array(notes: dict, batch_size=4) -> np.ndarray:
    """
    Embed all notes and return normalized embedding array.
    
    Args:
        notes: Dictionary of notes.
        batch_size: Size of document batch to embed each time. Defaults to 4.
    
    Returns:
        Numpy array of n_notes x embedding-dim normalized document embeddings.
    """

    # Load the tokenizer and model from transformers
    tokenizer = AutoTokenizer.from_pretrained('intfloat/e5-small-v2')
    model = AutoModel.from_pretrained('intfloat/e5-small-v2')
    # Ensure the model is in evaluation mode
    model.eval()
    # Collect all note contents
    data = [f"passage: {note['title']} {note['content']}" for note in notes.values() if 'content' in note]
    # Initialize list to hold embeddings
    all_embeddings = []
    
    # Process data in batches
    for i in range(0, len(data), batch_size):
        batch_data = data[i:i + batch_size]
        batch_dict = tokenizer(batch_data, max_length=512, padding=True, truncation=True, return_tensors='pt')
        outputs = model(**batch_dict)
        # Use the mean of token embeddings as sentence embeddings
        embeddings = outputs.last_hidden_state.mean(dim=1)
        # Normalize the embeddings
        # embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
        all_embeddings.append(embeddings.detach().cpu().numpy())
    # Concatenate all embeddings
    doc_embeddings_array = np.vstack(all_embeddings)
    return doc_embeddings_array

def query_semantic(query, doc_embeddings_array, n_results=2, threshold=0.9):
    """
    Performs semantic search on a given query and returns the indices of the most relevant documents.

    Args:
    - query (str): The user's query.
    - doc_embeddings_array (np.ndarray): An array of embeddings for all documents in the collection.
    - n_results (int, optional): The number of results to return. Default is 2.
    - threshold (float, optional): A threshold value for cosine similarity to filter results. Default is 0.9.

    Returns:
    - top_indices (list): A list of indices of the most relevant documents.
    """
    # Load the tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained('intfloat/e5-small-v2')
    model = AutoModel.from_pretrained('intfloat/e5-small-v2')
    # Tokenize and encode the query
    inputs = tokenizer(f"passage: {query}", return_tensors='pt', padding=True, truncation=True)
    # Get the embedding of the query
    outputs = model(**inputs)
    # Extract the [CLS] token embedding (first token) for the query
    query_embedding = outputs.last_hidden_state.mean(dim=1).detach().numpy()
    # Normalize the query embedding
    # query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
    # Compute cosine similarities between the query and document embeddings
    cos_sims = cosine_similarity(doc_embeddings_array, query_embedding).flatten()
    # Filter documents by threshold
    relevant_indices = np.where(cos_sims >= threshold)[0]
    # Sort the filtered indices by similarity score in descending order and return top n results
    top_indices = relevant_indices[np.argsort(-cos_sims[relevant_indices])[:n_results]]
    return top_indices

# notes = {
#     "note1": {
#         "title": "Основы кулинарии",
#         "content": "Кулинария — это искусство приготовления пищи. Основные техники включают варку, жарку, тушение и запекание."
#     },
#     "note2": {
#         "title": "История Древнего Египта",
#         "content": "Древний Египет — одна из древнейших цивилизаций, известная своими пирамидами, иероглифами и фараонами."
#     },
#     "note3": {
#         "title": "Основы фотографии",
#         "content": "Фотография — это искусство захвата моментов на пленку или цифровой носитель. Основные параметры включают диафрагму, выдержку и ISO."
#     }
# }

# query = "Древний Египет"
# embedding_array = build_embedding_array(notes)

# top_indices = query_semantic(query, embedding_array)
# print(top_indices)
# # [1 2]