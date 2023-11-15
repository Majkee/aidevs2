import json
import os
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, Distance, VectorParams, PointStruct
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader, JSONLoader
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
MEMORY_PATH = "archiwum.json"
COLLECTION_NAME = "ai_devs"

qdrant = QdrantClient("localhost", port=6333)
embeddings = OpenAIEmbeddings()
query = "Dalle-3"
query_embedding = embeddings.embed_query(query)
result = qdrant.get_collections()

indexed = None
for collection in result.collections:
    if collection.name == COLLECTION_NAME:
        indexed = collection
        break


# Create collection if not exists
if not indexed:
    qdrant.create_collection(
        COLLECTION_NAME,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        on_disk_payload=True
    )

collection_info = qdrant.get_collection(COLLECTION_NAME)

# Add data to collection if empty
if not collection_info.points_count:
    # Read File
    with open(MEMORY_PATH, 'r') as f:
        memory = json.load(f)

    documents_with_meta = []
    for document in memory:
        title = document['title']
        content = document['info']
        url = document['url']
        document_with_meta = [
            {
                'source': COLLECTION_NAME,
                'title': title,
                'content': content,
                'url': url,
                'uuid': str(uuid.uuid4())
            }
        ]
        documents_with_meta.append(document_with_meta)
    # Generate embeddings and index
    points = []
    for document in documents_with_meta[:300]:
        print(document)
        embedding = embeddings.embed_query(document[0]['content'])
        points.append({
            'id': document[0]['uuid'],
            'payload': document[0],
            'vector': embedding
        })

    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        wait=True,
        points=[
            PointStruct(id=point['id'], vector=point['vector'], payload=point['payload']) for point in points
        ]
    )

search_result = qdrant.search(
    collection_name=COLLECTION_NAME,
    query_vector=query_embedding,
    query_filter=Filter(
        must=[FieldCondition(key="source", match=MatchValue(value=COLLECTION_NAME))]
    ),
    limit=1,
)

print(search_result)