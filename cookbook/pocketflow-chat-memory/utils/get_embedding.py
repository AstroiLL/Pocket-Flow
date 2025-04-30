import os
import numpy as np


def get_embedding(text):
    from dotenv import load_dotenv
    from mistralai import Mistral
    # Загружаем переменные из .env файла
    load_dotenv()
    # OpenRouter API endpoint for embeddings
    
    # Get API key from environment variable
    api_key = os.environ.get("MISTRAL_API_KEY")
    mistral_embed = os.environ.get("MISTRAL_EMBED")
    
    client = Mistral(api_key=api_key)
    response = client.embeddings.create(
        model=mistral_embed,
        inputs=text
    )
    # Extract the embedding vector from the response
    embedding = response.data[0].embedding

    # Convert to numpy array for consistency with other embedding functions
    return np.array(embedding, dtype=np.float32)


if __name__ == "__main__":
    # Test the embedding function
    text1 = "The quick brown cat jumps over the lazy dog."
    text2 = "The quick brown fox jumps over the lazy dog."
    text3 = "The quick brown kitten jumps over the lazy dog."
    
    try:
        emb1 = get_embedding(text1)
        emb2 = get_embedding(text2)
        emb3 = get_embedding(text3)
        print(f"Embedding 1 shape: {emb1.shape}")
        print(f"Embedding 2 shape: {emb2.shape}")
        print(f"Embedding 3 shape: {emb3.shape}")
        # Calculate similarity (dot product)
        similarity12 = np.dot(emb1, emb2)
        similarity13 = np.dot(emb1, emb3)
        print(f"Similarity between texts: {similarity12:.4f}")
        print(f"Similarity between texts: {similarity13:.4f}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}") 