from fastapi import APIRouter
from app.db import get_db

router = APIRouter()


@router.get("/shop/products")
async def get_products():
    db = await get_db()
    cursor = await db.execute("SELECT * FROM products ORDER BY id")
    rows = await cursor.fetchall()
    return [dict(r) for r in rows]
