from langchain.document_loaders import TextLoader
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.openai import ChatOpenAI
import os
from dotenv import load_dotenv, find_dotenv
import json

# Specify the path to the parent directory
load_dotenv(find_dotenv())

loader = TextLoader("docs.md")
doc = loader.load()[0]
documents = [{"page_content": content} for content in doc.page_content.split("\n\n")]
print(documents)
model = ChatOpenAI()
descriptions = []

# Nie ogarnąłem, czy da się w pythonie zrobić równolegle zapytanie na 5 wątków jak w oryginalny przykładnie,
# więc na razie mamy jednowątkowość
for doc in documents:
    response = model([
    SystemMessage(content="Describe the following document with one of the following keywords: "
                          "Mateusz, Jakub, Adam. Return the keyword and nothing else."
    ),
    HumanMessage(
        content=f"Document: {doc['page_content']}"
    ),
    ])
    doc["metadata"] = {"source": response.content}

print(documents)
with open('docs.json', 'w') as json_file:
    json.dump(documents, json_file)
