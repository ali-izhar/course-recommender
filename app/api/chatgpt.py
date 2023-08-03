import os
import openai
import dotenv

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_completion(prompt, model_engine="gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(e)
        return "Sorry, I don't understand."


def get_embeddings(text, model_engine="text-embedding-ada-002"):
    try:
        response = openai.Embedding.create(
            input = text,
            model = model_engine,
        )["data"][0]["embedding"]
        return response
    except Exception as e:
        print(e)
        return "Sorry, I don't understand."