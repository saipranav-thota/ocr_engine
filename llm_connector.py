from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import env_loader



def run_prompt_openAI():
    api_key = env_loader.load_openAI_api_key()
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        openai_api_key=api_key
    )
    return llm


def run_prompt_gemini():
    api_key = env_loader.load_gemini_api_key()
    llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",  #can support 1,000,000 tokens or 750,00 words
            google_api_key=api_key
    )
    return llm