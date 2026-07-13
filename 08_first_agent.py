from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b")
response = llm.invoke("What is 5 + 3?")
print(response.content)
