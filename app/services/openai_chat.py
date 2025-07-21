from dotenv import load_dotenv
from openai import OpenAI
from app.utils.openai_tools import calculator_tool

# Load environment variables from .env file
load_dotenv()

# Create OpenAI client using the environment variable
client = OpenAI()

def ask_openai(message: str):
    response = client.responses.create(
        model="gpt-3.5-turbo",
        instructions="You are a helpful assistant.",
        input=[
            {"role": "user", "content": message}
        ],
        tools=[calculator_tool],
    )
    return response
