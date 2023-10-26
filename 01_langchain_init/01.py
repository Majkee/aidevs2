from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

text = [HumanMessage(content="Hey There!")]

chat = ChatOpenAI()
content = chat.predict_messages(text)

print(content)