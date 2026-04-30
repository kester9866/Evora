from fastapi import APIRouter, Query
from app.chroma import retrieve, unload_embed_fn

router = APIRouter()


@router.get("/knowledge/search")
async def search_knowledge(
    q: str = Query(..., min_length=1, description="Search query"),
    k: int = Query(default=10, ge=1, le=20, description="Number of results")
):
    chunks = []
    try:
        results = await retrieve(q, k=k)
        chunks = [{"text": text, "score": round(score, 3)} for text, score in results]
    except Exception:
        pass
    finally:
        try:
            unload_embed_fn()
        except Exception:
            pass

    return {"query": q, "total": len(chunks), "chunks": chunks}
