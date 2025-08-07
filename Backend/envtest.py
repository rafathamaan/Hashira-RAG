from dotenv import load_dotenv
import os
load_dotenv()  
import os
print('CWD:', os.getcwd())
print('.env exists:', os.path.exists('.env'))
print("QDRANT_URL:", os.getenv("QDRANT_URL"))
print("QDRANT_API_KEY:", os.getenv("QDRANT_API_KEY"))
import openai, os
openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "hello"}])
print(response.choices[0].message.content)
