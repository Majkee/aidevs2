from langchain.document_loaders import TextLoader, UnstructuredHTMLLoader, WebBaseLoader
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.openai import ChatOpenAI
from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain.tools.playwright.utils import (
    create_async_playwright_browser,
    create_sync_playwright_browser,  # A synchronous browser is available, though it isn't compatible with jupyter.
)
from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv, find_dotenv
import json
import re

# Uwaga: plik niedopracowany, działa tylko częściowo
# Specify the path to the parent directory
load_dotenv(find_dotenv())

# lanchainowe podejście playwright
def langchain_playwright():
    sync_browser = create_sync_playwright_browser()
    toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=sync_browser)
    tools = toolkit.get_tools()

    tools_by_name = {tool.name: tool for tool in tools}
    print(tools_by_name)
    navigate_tool = tools_by_name["navigate_browser"]
    get_elements_tool = tools_by_name["get_elements"]

    navigate_tool.run(
        {"url": "https://brain.overment.com"}
    )
    page_text = get_elements_tool.run({"selector": "main"})
    page_text = page_text
    print(page_text)

# klasyczne podejście z playwrightem
def classical_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.promptingguide.ai/techniques/tot")
        page_text = page.text_content('main')
        print(page_text)
        browser.close()

classical_playwright()