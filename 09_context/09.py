from langchain.document_loaders import TextLoader
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Specify the path to the parent directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

loader = TextLoader("memory.md")
doc = loader.load()[0]

chat = ChatOpenAI()

content = chat([
    SystemMessage(content="""
        Answer questions as truthfully using the context below and nothing more. If you don't know the answer, say "don't know".
        context###{}###
    """.format(doc.page_content)),
    HumanMessage(
        content="Who is Greg?"
    ),
])

print(content)