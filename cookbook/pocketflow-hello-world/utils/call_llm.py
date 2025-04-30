
def call_llm(prompt):
        from openai import OpenAI
        import os
        from dotenv import load_dotenv
        # Загружаем переменные из .env файла
        load_dotenv()
        
        # Получаем API ключ из переменной окружения или .env файла
        api_key = os.environ.get("OPENROUTER_API_KEY")
        
        if not api_key:
            raise ValueError("API ключ не найден. Создайте файл .env с переменной OPENROUTER_API_KEY или установите переменную окружения")
            
        client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        )

        completion = client.chat.completions.create(
        #extra_headers={
        #    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        #    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
        #},
        model="google/gemini-2.5-flash-preview",
        messages=prompt if isinstance(prompt, list) else [
            {
            "role": "user",
            "content": prompt
            }
        ]
        )
        return completion.choices[0].message.content
    
if __name__ == "__main__":
    prompt = "What is the meaning of life?"
    print(call_llm(prompt))