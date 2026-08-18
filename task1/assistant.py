import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ["OPENROUTER_API_KEY"],
                base_url="https://openrouter.ai/api/v1")


def ask(question: str) -> str:

    resp = client.chat.completions.create(
        model="gpt-oss-120b",
        temperature=0,
        messages=[
            {"role":"system", "content":"You are a helpful assistant. You have no tools. Answer briefly within 20 words."},
            {"role":"user","content": question},
        ],
    )

    return resp.choices[0].message.content

if __name__== "__main__":
    print(ask("How many words are in the file notes.txt ?"))