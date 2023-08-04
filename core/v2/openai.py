from langchain.llms import OpenAI
import tiktoken

from dotenv import load_dotenv

load_dotenv()

tokenize = tiktoken.get_encoding('cl100k_base')
llm = OpenAI(temperature=0, max_tokens=2048)


def tiktoken_len(text):
    tokens = tokenize.encode(text, disallowed_special=())

    return len(tokens)
