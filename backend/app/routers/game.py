from fastapi import APIRouter

router = APIRouter()


@router.get("/game/levels")
async def get_levels():
    return [
        {
            "level": 1,
            "name": "基础榫卯",
            "tenon": {"x": 100, "y": 250, "width": 60, "height": 40},
            "mortise": {"x": 450, "y": 250, "width": 70, "height": 50},
            "knowledge": "榫卯节点是中国木结构建筑的核心技术。"
        }
    ]
