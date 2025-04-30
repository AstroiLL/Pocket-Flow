import os
import numpy as np
import hashlib

def get_embedding(text):
    """
    Создает простой эмбеддинг на основе хэша текста.
    Это локальная альтернатива OpenAI API, которая работает без интернет-соединения.
    
    Args:
        text (str): Входной текст для создания эмбеддинга
        
    Returns:
        np.array: Вектор эмбеддинга размерности 1536 (как у ada-002)
    """
    # Используем SHA-256 для хэширования текста
    text_bytes = text.encode('utf-8')
    hash_obj = hashlib.sha256(text_bytes)
    hash_digest = hash_obj.digest()
    
    # Получаем 32 байта из SHA-256
    # Преобразуем их в массив чисел с плавающей точкой
    hash_array = np.frombuffer(hash_digest, dtype=np.uint8)
    
    # Повторяем массив для получения 1536 элементов (как у ada-002)
    repeats = int(np.ceil(1536 / len(hash_array)))
    expanded = np.tile(hash_array, repeats)[:1536]
    
    # Нормализуем к диапазону [-1, 1]
    normalized = (expanded.astype(np.float32) / 127.5) - 1.0
    
    return normalized


if __name__ == "__main__":
    # Test the embedding function
    text1 = "The quick brown fox jumps over the lazy dog."
    text2 = "Python is a popular programming language for data science."
    text3 = "The quick brown cat jumps over the lazy dog."  # Same as text1
    
    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)
    emb3 = get_embedding(text3)
    
    print(f"Embedding 1 shape: {emb1.shape}")
    print(f"Embedding 2 shape: {emb2.shape}")
    
    # Calculate similarities using cosine similarity
    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    sim_1_2 = cosine_similarity(emb1, emb2)
    sim_1_3 = cosine_similarity(emb1, emb3)
    
    print(f"Similarity between different texts: {sim_1_2:.4f}")
    print(f"Similarity between identical texts: {sim_1_3:.4f}") 