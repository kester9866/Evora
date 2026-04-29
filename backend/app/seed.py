from app.db import get_db

SEED_BRIDGES = [
    {
        "name_zh": "赵州桥", "name_en": "Zhaozhou Bridge", "dynasty": "隋", "type": "拱桥",
        "material": "石材", "province": "河北", "city": "石家庄市", "district": "赵县",
        "coordinates": "37.75,114.77",
        "year_built": "605", "length_m": 50.82, "width_m": 9.6, "span_m": 37.37,
        "description": "世界最古老的敞肩石拱桥，由隋代匠人李春设计建造，至今已1400余年。",
        "has_model": 1, "model_url": "https://models.example.com/zhaozhou.glb"
    },
    {
        "name_zh": "洛阳桥", "name_en": "Luoyang Bridge", "dynasty": "宋", "type": "梁桥",
        "material": "石材", "province": "福建", "city": "泉州市", "district": "洛江",
        "coordinates": "24.94,118.67",
        "year_built": "1053", "length_m": 1200, "width_m": 5.0,
        "description": "中国现存最早的跨海梁式石桥，采用筏形基础和牡蛎固基法建造。",
        "has_model": 0
    },
    {
        "name_zh": "卢沟桥", "name_en": "Lugou Bridge", "dynasty": "金", "type": "拱桥",
        "material": "石材", "province": "北京", "city": "北京", "district": "丰台",
        "coordinates": "39.85,116.21",
        "year_built": "1192", "length_m": 266.5, "width_m": 9.3, "span_m": 11.0,
        "description": "北京现存最古老的石造联拱桥，以石狮雕刻闻名。",
        "has_model": 0
    },
    {
        "name_zh": "广济桥", "name_en": "Guangji Bridge", "dynasty": "宋", "type": "浮桥",
        "material": "木石混合", "province": "广东", "city": "潮州市", "district": "湘桥",
        "coordinates": "23.67,116.65",
        "year_built": "1171", "length_m": 518,
        "description": "中国四大古桥之一，集梁桥、浮桥、拱桥于一体的启闭式桥梁。",
        "has_model": 0
    },
    {
        "name_zh": "安济桥", "name_en": "Anji Bridge", "dynasty": "隋", "type": "拱桥",
        "material": "石材", "province": "河北", "city": "石家庄市", "district": "赵县",
        "coordinates": "37.72,114.77",
        "year_built": "595", "length_m": 50.82, "span_m": 37.02,
        "description": "又名赵州桥，采用敞肩拱结构，减轻桥身重量同时增加泄洪能力。",
        "has_model": 1, "model_url": "https://models.example.com/anji.glb"
    },
    {
        "name_zh": "泸定桥", "name_en": "Luding Bridge", "dynasty": "清", "type": "索桥",
        "material": "铁索", "province": "四川", "city": "甘孜藏族自治州", "district": "泸定",
        "coordinates": "29.91,102.23",
        "year_built": "1706", "length_m": 103.67, "width_m": 3.0,
        "description": "大渡河上的铁索悬桥，由13根铁链组成，每根铁链重约1.5吨。",
        "has_model": 0
    },
    {
        "name_zh": "灞桥", "name_en": "Ba Bridge", "dynasty": "唐", "type": "梁桥",
        "material": "木石混合", "province": "陕西", "city": "西安市", "district": "灞桥",
        "coordinates": "34.25,109.05",
        "year_built": "732", "length_m": 386,
        "description": "唐代长安城东重要桥梁，因折柳送别的习俗而闻名。",
        "has_model": 0
    },
    {
        "name_zh": "汴水虹桥", "name_en": "Rainbow Bridge", "dynasty": "宋", "type": "木桥",
        "material": "木材", "province": "河南", "city": "开封市", "district": "开封",
        "coordinates": "34.79,114.35",
        "year_built": "1050", "description": "清明上河图中描绘的木拱桥，采用叠梁结构，无柱飞渡汴水。",
        "has_model": 0
    },
    {
        "name_zh": "宝带桥", "name_en": "Baodai Bridge", "dynasty": "唐", "type": "拱桥",
        "material": "石材", "province": "江苏", "city": "苏州市", "district": "吴中",
        "coordinates": "31.25,120.62",
        "year_built": "816", "length_m": 316.8, "width_m": 4.1,
        "description": "中国最长的多孔联拱石桥，共53孔，横跨澹台湖。",
        "has_model": 0
    },
    {
        "name_zh": "八字桥", "name_en": "Bazi Bridge", "dynasty": "宋", "type": "梁桥",
        "material": "石材", "province": "浙江", "city": "绍兴市", "district": "越城",
        "coordinates": "30.00,120.58",
        "year_built": "1256", "description": "宋代石梁桥，桥面呈八字形布局，连接三条街道，结构精巧。",
        "has_model": 0
    },
    {
        "name_zh": "虹桥", "name_en": "Hong Bridge", "dynasty": "明", "type": "廊桥",
        "material": "木石混合", "province": "浙江", "city": "温州市", "district": "泰顺",
        "coordinates": "27.56,119.72",
        "year_built": "1500", "length_m": 41.6, "width_m": 4.86,
        "description": "泰顺廊桥代表，木拱廊桥结构，桥上有廊屋，为过往行人遮风避雨。",
        "has_model": 0
    },
    {
        "name_zh": "霁虹桥", "name_en": "Jihong Bridge", "dynasty": "明", "type": "索桥",
        "material": "铁索", "province": "云南", "city": "保山市", "district": "隆阳",
        "coordinates": "25.11,98.87",
        "year_built": "1475", "length_m": 106, "width_m": 3.7,
        "description": "澜沧江上的古铁索桥，是古代南方丝绸之路的重要通道。",
        "has_model": 0
    }
]


async def seed_if_empty():
    db = await get_db()
    cursor = await db.execute("SELECT COUNT(*) FROM bridges")
    row = await cursor.fetchone()
    if row and row[0] == 0:
        for b in SEED_BRIDGES:
            await db.execute("""
                INSERT INTO bridges (name_zh, name_en, dynasty, type, material, province, city, district,
                    coordinates, year_built, length_m, width_m, span_m, description, has_model, model_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                b["name_zh"], b.get("name_en"), b["dynasty"], b["type"], b.get("material"),
                b["province"], b.get("city"), b.get("district"), b.get("coordinates"), b.get("year_built"),
                b.get("length_m"), b.get("width_m"), b.get("span_m"), b.get("description"),
                b.get("has_model", 0), b.get("model_url")
            ))
        await db.commit()
