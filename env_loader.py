from dotenv import load_dotenv
import os


def load_openAI_api_key():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    return api_key

def load_gemini_api_key():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    print(api_key)
    return api_key

load_gemini_api_key()
