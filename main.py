from langchain_openai import ChatOpenAI
from langchain_openai import embeddings

llm = ChatOpenAI()
llm.invoke("Hello, world!")