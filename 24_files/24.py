from bs4 import BeautifulSoup
import markdownify
import os
import json
import re


# Define metadata type
class DocMetadata:
    def __init__(self, source, section, author, links):
        self.source = source
        self.section = section
        self.author = author
        self.links = links


# Define document type
class Document:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata


# Your helper function to extract links to metadata
def extract_links_to_metadata(docs):
    for doc in docs:
        i = 1
        url_to_placeholder = {}
        links = doc.metadata.links

        # Replace URLs with placeholders
        def url_replacer(url):
            nonlocal i
            if url not in url_to_placeholder:
                placeholder = f'$link{i}'
                i += 1
                url_to_placeholder[url] = placeholder
                links[placeholder] = url
            return url_to_placeholder[url]

        url_pattern = r'((http|https)://[^\s]+|\./[^\s]+)(?=\))'
        convert_match_to_string = lambda match: url_replacer(match.group(0))
        doc.page_content = re.sub(url_pattern, convert_match_to_string, doc.page_content)

    return docs


# Load HTML content
with open("aidevs.html", "r", encoding="utf-8") as html_file:
    html_content = html_file.read()

# Load HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Get authors section
authors = soup.select_one("#instructors") or ''

# Convert HTML to markdown
markdown = markdownify.markdownify(str(authors), heading_style="ATX")

# Split markdown into chunks
chunks = re.split('\!\[(?!\!\[).+\]', markdown)

docs = []
for chunk in chunks:
    # Get author name
    author_search = re.search('###\s(.*)\\n', chunk)
    author = author_search.group(1).replace(' \n', '').strip() if author_search else ''

    # Create metadata
    metadata = DocMetadata(
        source='aidevs',
        section='instructors',
        author=author,
        links={},
    )

    # Create document, clear data from newlines and multispaces
    doc_content = re.sub(r'[\n\\]', '', chunk)
    doc_content = re.sub(r'\s{2,}', ' ', doc_content)

    # Filter short documents and instantiate Document object
    if len(doc_content) > 50:
        docs.append(Document(doc_content, metadata))

# Extract links and update final list of documents
docs = extract_links_to_metadata(docs)

# Write to file
with open('aidevs.json', 'w', encoding='utf-8') as f:
    doc_dict = [{"pageContent": doc.page_content, "metadata": doc.metadata.__dict__} for doc in docs]
    json.dump(doc_dict, f, indent=2)