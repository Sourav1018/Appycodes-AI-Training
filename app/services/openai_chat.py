from dotenv import load_dotenv
from openai import OpenAI

from app.utils.openai_tools import calculator_tool, weather_tool

# Load environment variables from .env file
load_dotenv()

# Create OpenAI client using the environment variable
client = OpenAI()


def ask_openai(message):
    if not isinstance(message, (str, list)):
        raise TypeError("messages must be a string or a list of message dicts")

    # if isinstance(message, list):
    #     for msg in message:
    #         if not isinstance(msg, dict) or "role" not in msg:
    #             raise ValueError(
    #                 "Each message in the list must be a dict with 'role' and 'content'"
    #             )
    response = client.responses.create(
        model="gpt-3.5-turbo",
        instructions="You are a helpful assistant.",
        input=message,
        tools=[calculator_tool, weather_tool],
    )
    return response
