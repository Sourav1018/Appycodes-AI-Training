from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Create OpenAI client using the environment variable
client = OpenAI()

def ask_openai(message: str) -> str:
    response = client.responses.create(
        model="gpt-3.5-turbo",
        instructions="You are a helpful assistant.",
        input=[
            {"role": "user", "content": message}
        ]
    )
    return response.output_text
