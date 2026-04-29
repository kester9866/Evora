from fastapi import APIRouter
from app.db import get_db

router = APIRouter()

DYNASTY_COLORS = {
    "先秦": "#e74c3c", "秦": "#e74c3c", "汉": "#e74c3c",
    "隋": "#f1c40f", "唐": "#f1c40f",
    "宋": "#2ecc71",
    "元": "#3498db",
    "明": "#9b59b6",
    "清": "#1abc9c"
}


@router.get("/kg/graph-data")
async def get_graph_data():
    db = await get_db()
    cursor = await db.execute("SELECT id, name_zh, dynasty, type, description, has_model FROM bridges")
    bridges = [dict(r) for r in await cursor.fetchall()]

    nodes = []
    for b in bridges:
        nodes.append({
            "id": b["id"],
            "label": b["name_zh"],
            "dynasty": b["dynasty"],
            "summary": f'{b["dynasty"]} · {b["type"]} · {b.get("description", "")[:80]}' if b.get("description") else "",
            "has_model": bool(b.get("has_model"))
        })

    edges = []
    for i, a in enumerate(bridges):
        for b in bridges[i + 1:]:
            relation = None
            if a["dynasty"] == b["dynasty"]:
                relation = "同朝代"
            elif a["type"] == b["type"]:
                relation = "同类型"
            elif a.get("province") and a["province"] == b.get("province"):
                relation = "同地区"
            if relation:
                edges.append({
                    "source": a["id"],
                    "target": b["id"],
                    "relation": relation
                })

    return {"nodes": nodes, "edges": edges[:200]}
