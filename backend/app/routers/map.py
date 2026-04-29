from fastapi import APIRouter, Query
from app.db import get_db

router = APIRouter()


@router.get("/map/provinces")
async def get_provinces(
    dynasty: str = Query(None),
    type: str = Query(None)
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

    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    cursor = await db.execute(
        f"SELECT province, COUNT(*) as count FROM bridges {where} GROUP BY province ORDER BY count DESC",
        params
    )
    return [{"province": r[0], "count": r[1]} for r in await cursor.fetchall()]


@router.get("/map/cities")
async def get_cities(
    province: str = Query(...),
    dynasty: str = Query(None),
    type: str = Query(None)
):
    db = await get_db()
    conditions = ["province = ?"]
    params = [province]
    if dynasty:
        conditions.append("dynasty = ?")
        params.append(dynasty)
    if type:
        conditions.append("type = ?")
        params.append(type)

    where = "WHERE " + " AND ".join(conditions)
    cursor = await db.execute(
        f"SELECT city, COUNT(*) as count FROM bridges {where} GROUP BY city ORDER BY count DESC",
        params
    )
    return [{"city": r[0], "count": r[1]} for r in await cursor.fetchall()]


@router.get("/map/districts")
async def get_districts(
    province: str = Query(None),
    dynasty: str = Query(None),
    type: str = Query(None)
):
    db = await get_db()
    conditions = []
    params = []
    if province:
        conditions.append("province = ?")
        params.append(province)
    if dynasty:
        conditions.append("dynasty = ?")
        params.append(dynasty)
    if type:
        conditions.append("type = ?")
        params.append(type)

    if conditions:
        where = "WHERE " + " AND ".join(conditions) + " AND district IS NOT NULL AND district != ''"
    else:
        where = "WHERE district IS NOT NULL AND district != ''"
    cursor = await db.execute(
        f"SELECT district, COUNT(*) as count FROM bridges {where} GROUP BY district ORDER BY count DESC",
        params
    )
    return [{"district": r[0], "count": r[1]} for r in await cursor.fetchall()]


@router.get("/map/regions")
async def get_regions():
    db = await get_db()
    cursor = await db.execute("SELECT DISTINCT province FROM bridges ORDER BY province")
    return [r[0] for r in await cursor.fetchall()]
