#!/usr/bin/env python3
"""Rebuild Chroma vector store from SQLite knowledge chunks."""
import asyncio
import aiosqlite
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from app.chroma import _get_collection, embed_text

DATABASE_PATH = os.getenv("DATABASE_PATH", "evora.db")


async def rebuild_chroma():
    db = await aiosqlite.connect(DATABASE_PATH)
    db.row_factory = aiosqlite.Row

    cursor = await db.execute("""
        SELECT kc.id, kc.text, kc.bridge_id, b.name_zh as bridge_name
        FROM knowledge_chunks kc
        LEFT JOIN bridges b ON kc.bridge_id = b.id
        ORDER BY kc.id
    """)
    rows = await cursor.fetchall()
    await db.close()

    print(f"Found {len(rows)} chunks. Rebuilding Chroma collection...")

    # Clear existing collection
    collection = _get_collection()
    try:
        existing = collection.get()
        if existing["ids"]:
            collection.delete(ids=existing["ids"])
            print(f"  Deleted {len(existing['ids'])} existing embeddings")
    except Exception:
        pass

    batch_size = 20
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i+batch_size]
        ids = []
        embeddings = []
        documents = []
        metadatas = []

        for j, row in enumerate(batch):
            try:
                embedding = await embed_text(row["text"])
                ids.append(str(row["id"]))
                embeddings.append(embedding)
                documents.append(row["text"])
                metadatas.append({
                    "bridge_id": row["bridge_id"] or 0,
                    "bridge_name": row["bridge_name"] or ""
                })
            except Exception as e:
                print(f"  Error embedding chunk {row['id']}: {e}")

        if ids:
            collection.upsert(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
            print(f"  Batch {i//batch_size + 1}: {len(ids)} chunks embedded and stored")

        if i + batch_size < len(rows):
            await asyncio.sleep(1)

    print(f"\nChroma rebuild complete: {len(rows)} chunks in vector store.")


if __name__ == "__main__":
    asyncio.run(rebuild_chroma())
