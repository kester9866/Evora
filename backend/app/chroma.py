import chromadb
from chromadb.config import Settings
from app.config import CHROMA_PATH

_client = None
_collection = None
_embed_fn = None


def _get_embed_fn():
    global _embed_fn
    if _embed_fn is None:
        from chromadb.utils import embedding_functions
        _embed_fn = embedding_functions.DefaultEmbeddingFunction()
    return _embed_fn


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
            metadata={"hnsw:space": "cosine"},
            embedding_function=_get_embed_fn()
        )
    return _collection


async def embed_text(text: str) -> list[float]:
    try:
        return _get_embed_fn()([text])[0].tolist()
    except Exception as e:
        print(f"Embedding error: {e}")
        return [0.0] * 384


async def retrieve(query_text: str, k: int = 3, threshold: float = 0.28) -> list[tuple[str, float]]:
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
            if similarity >= threshold:
                chunks.append((doc, similarity))
    return chunks


async def upsert_chunk(chunk_id: int, bridge_id: int, bridge_name: str, text: str):
    collection = _get_collection()
    embedding = await embed_text(text)

    collection.upsert(
        ids=[str(chunk_id)],
        embeddings=[embedding],
        documents=[text],
        metadatas=[{"bridge_id": bridge_id, "bridge_name": bridge_name}]
    )


def unload_embed_fn():
    global _embed_fn
    if _embed_fn is not None:
        del _embed_fn
        _embed_fn = None


async def delete_chunk(chunk_id: int):
    collection = _get_collection()
    try:
        collection.delete(ids=[str(chunk_id)])
    except Exception:
        pass
