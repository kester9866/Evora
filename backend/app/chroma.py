import chromadb
from chromadb.config import Settings
from app.config import CHROMA_PATH, DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

_client = None
_collection = None


def _get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(
            path=CHROMA_PATH,
            settings=Settings(anonymized_telemetry=False)
        )
    return _client


def _get_collection():
    global _collection
    if _collection is None:
        client = _get_client()
        _collection = client.get_or_create_collection(
            name="bridge_knowledge",
            metadata={"hnsw:space": "cosine"}
        )
    return _collection


async def embed_text(text: str) -> list[float]:
    """Embed a single text using DeepSeek embedding API."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
        response = client.embeddings.create(
            model="deepseek-embedding",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Embedding error: {e}")
        return [0.0] * 1024


async def retrieve(query_text: str, k: int = 3) -> list[tuple[str, float]]:
    """Retrieve top-k relevant chunks for a query."""
    collection = _get_collection()
    query_embedding = await embed_text(query_text)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    chunks = []
    if results["documents"] and results["documents"][0]:
        for i, doc in enumerate(results["documents"][0]):
            distance = results["distances"][0][i] if results.get("distances") else 0
            similarity = 1 - distance if distance else 1.0
            if similarity >= 0.6:
                chunks.append((doc, similarity))
    return chunks


async def upsert_chunk(chunk_id: int, bridge_id: int, bridge_name: str, text: str):
    """Insert or update a knowledge chunk."""
    collection = _get_collection()
    embedding = await embed_text(text)

    collection.upsert(
        ids=[str(chunk_id)],
        embeddings=[embedding],
        documents=[text],
        metadatas=[{"bridge_id": bridge_id, "bridge_name": bridge_name}]
    )


async def delete_chunk(chunk_id: int):
    """Delete a knowledge chunk from the vector store."""
    collection = _get_collection()
    try:
        collection.delete(ids=[str(chunk_id)])
    except Exception:
        pass
