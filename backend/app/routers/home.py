import random
from fastapi import APIRouter
from app.db import get_db

router = APIRouter()

FACTS = [
    "中国现存古桥超过100万座，其中百年以上历史的约有7万多座。",
    "赵州桥是世界上现存最古老、跨度最大的敞肩石拱桥。",
    "榫卯结构可以在不使用一颗钉子的情况下实现稳固连接。",
    "汴水虹桥是《清明上河图》中最著名的桥梁形象。",
    "闽浙木拱廊桥已被列入联合国教科文组织世界遗产预备名录。",
    "中国古代桥梁可分为梁桥、拱桥、索桥和浮桥四大类型。",
    "榫卯节点的精确度要求达到毫米级，体现了古代匠人的高超技艺。",
    "广济桥是世界上最早的启闭式桥梁。"
]


@router.get("/home/on-this-day")
async def get_on_this_day(month: int, day: int):
    db = await get_db()
    cursor = await db.execute("SELECT name_zh, dynasty, type, description FROM bridges ORDER BY RANDOM() LIMIT 1")
    row = await cursor.fetchone()
    if row:
        return {"description": f"{row[0]}（{row[1]}·{row[2]}）：{row[3] or '一座中国古代桥梁典范。'}"}
    return {"description": "今天，我们回望中国古代桥梁的辉煌成就。"}


@router.get("/home/random-fact")
async def get_random_fact():
    return {"text": random.choice(FACTS)}
