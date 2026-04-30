from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel, field_validator
from app.db import get_db
from app.auth import verify_password, create_token, verify_token
from app.chroma import upsert_chunk, delete_chunk as chroma_delete
import re

router = APIRouter()

# Only allow safe characters in relative paths: alphanumeric, underscore, dash, dot, slash
_SAFE_PATH_RE = re.compile(r'^[a-zA-Z0-9_\-./]+$')


def validate_asset_url(v: str | None) -> str | None:
    """Validate an asset URL. Accepts absolute http(s) URLs and ./ relative paths.
    Rejects paths with .. traversal or dangerous characters."""
    if v is None or v.strip() == '':
        return v
    trimmed = v.strip()
    # Absolute URLs pass through
    if trimmed.startswith('http://') or trimmed.startswith('https://'):
        return trimmed
    # Relative paths must start with ./ and contain no ..
    if trimmed.startswith('./'):
        if '..' in trimmed:
            raise ValueError('相对路径不允许包含 ".." 向上穿越字符')
        if not _SAFE_PATH_RE.match(trimmed):
            raise ValueError('相对路径包含非法字符，仅允许字母、数字、下划线、短横线、点和斜杠')
        return trimmed
    # Other formats pass through (could be a filename, etc.)
    return trimmed


class LoginRequest(BaseModel):
    username: str
    password: str


class BridgeCreate(BaseModel):
    name_zh: str
    name_en: str | None = None
    dynasty: str | None = None
    type: str | None = None
    material: str | None = None
    province: str | None = None
    city: str | None = None
    district: str | None = None
    coordinates: str | None = None
    year_built: str | None = None
    length_m: float | None = None
    width_m: float | None = None
    span_m: float | None = None
    description: str | None = None
    has_model: bool = False
    model_url: str | None = None
    image_url: str | None = None

    @field_validator('model_url', 'image_url')
    @classmethod
    def check_url(cls, v: str | None) -> str | None:
        return validate_asset_url(v)


class ProductCreate(BaseModel):
    name_zh: str
    price: float = 0
    description: str | None = None
    image_url: str | None = None
    buy_link: str | None = None

    @field_validator('image_url')
    @classmethod
    def check_url(cls, v: str | None) -> str | None:
        return validate_asset_url(v)


class ChunkCreate(BaseModel):
    bridge_id: int
    text: str


def get_current_admin(authorization: str | None = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ", 1)[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload.get("sub", "admin")


# --- Auth ---
@router.post("/admin/login")
async def login(body: LoginRequest):
    if not verify_password(body.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(body.username)
    return {"token": token, "token_type": "bearer"}


# --- Bridges Admin ---
@router.get("/admin/bridges")
async def get_bridges_admin(page: int = 1, limit: int = 20, _=Depends(get_current_admin)):
    db = await get_db()
    offset = (page - 1) * limit
    cursor = await db.execute("SELECT * FROM bridges ORDER BY id DESC LIMIT ? OFFSET ?", [limit, offset])
    rows = await cursor.fetchall()
    cursor = await db.execute("SELECT COUNT(*) FROM bridges")
    total = (await cursor.fetchone())[0]
    return {"items": [dict(r) for r in rows], "total": total, "page": page, "limit": limit}


@router.post("/admin/bridges")
async def create_bridge(body: BridgeCreate, _=Depends(get_current_admin)):
    db = await get_db()
    cursor = await db.execute("""
        INSERT INTO bridges (name_zh, name_en, dynasty, type, material, province, city, district,
            coordinates, year_built, length_m, width_m, span_m, description, has_model, model_url, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        body.name_zh, body.name_en, body.dynasty, body.type, body.material, body.province, body.city, body.district,
        body.coordinates, body.year_built, body.length_m, body.width_m, body.span_m,
        body.description, int(body.has_model), body.model_url, body.image_url
    ])
    await db.commit()
    return {"id": cursor.lastrowid}


@router.put("/admin/bridges/{bridge_id}")
async def update_bridge(bridge_id: int, body: BridgeCreate, _=Depends(get_current_admin)):
    db = await get_db()
    await db.execute("""
        UPDATE bridges SET name_zh=?, name_en=?, dynasty=?, type=?, material=?, province=?, city=?, district=?,
            coordinates=?, year_built=?, length_m=?, width_m=?, span_m=?, description=?,
            has_model=?, model_url=?, image_url=?, updated_at=CURRENT_TIMESTAMP
        WHERE id=?
    """, [
        body.name_zh, body.name_en, body.dynasty, body.type, body.material, body.province, body.city, body.district,
        body.coordinates, body.year_built, body.length_m, body.width_m, body.span_m,
        body.description, int(body.has_model), body.model_url, body.image_url, bridge_id
    ])
    await db.commit()
    return {"ok": True}


@router.delete("/admin/bridges/{bridge_id}")
async def delete_bridge(bridge_id: int, _=Depends(get_current_admin)):
    db = await get_db()
    await db.execute("DELETE FROM bridges WHERE id = ?", [bridge_id])
    await db.commit()
    return {"ok": True}


# --- Products Admin ---
@router.get("/admin/products")
async def get_products_admin(page: int = 1, limit: int = 20, _=Depends(get_current_admin)):
    db = await get_db()
    offset = (page - 1) * limit
    cursor = await db.execute("SELECT * FROM products ORDER BY id DESC LIMIT ? OFFSET ?", [limit, offset])
    rows = await cursor.fetchall()
    cursor = await db.execute("SELECT COUNT(*) FROM products")
    total = (await cursor.fetchone())[0]
    return {"items": [dict(r) for r in rows], "total": total, "page": page, "limit": limit}


@router.post("/admin/products")
async def create_product(body: ProductCreate, _=Depends(get_current_admin)):
    db = await get_db()
    cursor = await db.execute(
        "INSERT INTO products (name_zh, price, description, image_url, buy_link) VALUES (?, ?, ?, ?, ?)",
        [body.name_zh, body.price, body.description, body.image_url, body.buy_link]
    )
    await db.commit()
    return {"id": cursor.lastrowid}


@router.put("/admin/products/{product_id}")
async def update_product(product_id: int, body: ProductCreate, _=Depends(get_current_admin)):
    db = await get_db()
    await db.execute(
        "UPDATE products SET name_zh=?, price=?, description=?, image_url=?, buy_link=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
        [body.name_zh, body.price, body.description, body.image_url, body.buy_link, product_id]
    )
    await db.commit()
    return {"ok": True}


@router.delete("/admin/products/{product_id}")
async def delete_product(product_id: int, _=Depends(get_current_admin)):
    db = await get_db()
    await db.execute("DELETE FROM products WHERE id = ?", [product_id])
    await db.commit()
    return {"ok": True}


# --- Knowledge Chunks Admin ---
@router.get("/admin/knowledge-chunks")
async def get_chunks_admin(page: int = 1, limit: int = 20, _=Depends(get_current_admin)):
    db = await get_db()
    offset = (page - 1) * limit
    cursor = await db.execute("""
        SELECT kc.*, b.name_zh as bridge_name FROM knowledge_chunks kc
        LEFT JOIN bridges b ON kc.bridge_id = b.id
        ORDER BY kc.id DESC LIMIT ? OFFSET ?
    """, [limit, offset])
    rows = await cursor.fetchall()
    cursor = await db.execute("SELECT COUNT(*) FROM knowledge_chunks")
    total = (await cursor.fetchone())[0]
    return {"items": [dict(r) for r in rows], "total": total, "page": page, "limit": limit}


@router.post("/admin/knowledge-chunks")
async def create_chunk(body: ChunkCreate, _=Depends(get_current_admin)):
    db = await get_db()
    cursor = await db.execute(
        "INSERT INTO knowledge_chunks (bridge_id, text) VALUES (?, ?)",
        [body.bridge_id, body.text]
    )
    await db.commit()
    chunk_id = cursor.lastrowid

    # Get bridge name for Chroma metadata
    cursor = await db.execute("SELECT name_zh FROM bridges WHERE id = ?", [body.bridge_id])
    bridge_row = await cursor.fetchone()
    bridge_name = bridge_row[0] if bridge_row else "Unknown"

    try:
        await upsert_chunk(chunk_id, body.bridge_id, bridge_name, body.text)
    except Exception:
        pass

    return {"id": chunk_id}


@router.put("/admin/knowledge-chunks/{chunk_id}")
async def update_chunk(chunk_id: int, body: ChunkCreate, _=Depends(get_current_admin)):
    db = await get_db()
    await db.execute(
        "UPDATE knowledge_chunks SET bridge_id=?, text=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
        [body.bridge_id, body.text, chunk_id]
    )
    await db.commit()

    cursor = await db.execute("SELECT name_zh FROM bridges WHERE id = ?", [body.bridge_id])
    bridge_row = await cursor.fetchone()
    bridge_name = bridge_row[0] if bridge_row else "Unknown"

    try:
        await upsert_chunk(chunk_id, body.bridge_id, bridge_name, body.text)
    except Exception:
        pass

    return {"ok": True}


@router.delete("/admin/knowledge-chunks/{chunk_id}")
async def delete_chunk(chunk_id: int, _=Depends(get_current_admin)):
    db = await get_db()
    await db.execute("DELETE FROM knowledge_chunks WHERE id = ?", [chunk_id])
    await db.commit()

    try:
        await chroma_delete(chunk_id)
    except Exception:
        pass

    return {"ok": True}
