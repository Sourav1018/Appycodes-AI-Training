from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create OpenAI client using the environment variable
client = OpenAI()

response = client.responses.create(
    model="gpt-3.5-turbo",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)