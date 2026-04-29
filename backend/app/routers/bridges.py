from fastapi import APIRouter, Query
from app.db import get_db

router = APIRouter()


@router.get("/bridges")
async def get_bridges(
    dynasty: str = Query(None),
    type: str = Query(None),
    province: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200)
):
    db = await get_db()
    conditions = []
    params = []

    if dynasty:
        conditions.append("dynasty = ?")
        params.append(dynasty)
    if type:
        conditions.append("type = ?")
        params.append(type)
    if province:
        conditions.append("province = ?")
        params.append(province)

    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    offset = (page - 1) * limit

    cursor = await db.execute(
        f"SELECT * FROM bridges {where} ORDER BY id LIMIT ? OFFSET ?",
        params + [limit, offset]
    )
    rows = await cursor.fetchall()

    cursor = await db.execute(f"SELECT COUNT(*) FROM bridges {where}", params)
    total = (await cursor.fetchone())[0]

    return {
        "items": [dict(r) for r in rows],
        "total": total,
        "page": page,
        "limit": limit
    }


@router.get("/bridges/{bridge_id}")
async def get_bridge(bridge_id: int):
    db = await get_db()
    cursor = await db.execute("SELECT * FROM bridges WHERE id = ?", [bridge_id])
    row = await cursor.fetchone()
    if not row:
        return {"error": "Bridge not found"}, 404
    return dict(row)
