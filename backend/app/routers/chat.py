import json
import asyncio
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.chroma import retrieve

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


BRIDGE_KEYWORDS = [
    "桥", "拱桥", "梁桥", "索桥", "廊桥", "浮桥", "木桥", "石桥",
    "赵州桥", "洛阳桥", "卢沟桥", "广济桥", "安济桥", "泸定桥",
    "灞桥", "宝带桥", "八字桥", "虹桥", "霁虹桥", "汴水虹桥",
    "桥梁", "古桥", "石拱", "桥墩", "桥面", "桥身", "桥孔",
    "榫卯", "斗拱", "营造", "匠人", "李春", "营造法式",
    "建筑", "结构", "跨度", "拱券", "建造", "遗址"
]


def is_bridge_related(text: str) -> bool:
    return any(kw in text for kw in BRIDGE_KEYWORDS)


async def web_search(query: str, max_results: int = 5) -> str:
    """Search the web and return concatenated snippets."""
    try:
        import httpx
        # Use DuckDuckGo Instant Answer API (free, no key needed)
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                "https://api.duckduckgo.com/",
                params={"q": query + " 中国古桥", "format": "json", "no_html": 1, "skip_disambig": 1}
            )
            data = resp.json()

            parts = []
            if data.get("AbstractText"):
                parts.append(data["AbstractText"])
            if data.get("Answer"):
                parts.append(data["Answer"])

            for topic in data.get("RelatedTopics", [])[:max_results]:
                if isinstance(topic, dict) and topic.get("Text"):
                    parts.append(topic["Text"])

            if parts:
                return "\n".join(parts[:max_results])

            # Fallback: try HTML search
            resp2 = await client.get(
                "https://html.duckduckgo.com/html/",
                params={"q": query + " 中国古桥"},
                headers={"User-Agent": "Mozilla/5.0"}
            )
            from html.parser import HTMLParser

            class SnippetParser(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.snippets = []
                    self.in_snippet = False
                    self.current = ""

                def handle_starttag(self, tag, attrs):
                    attrs_dict = dict(attrs)
                    if "result__snippet" in attrs_dict.get("class", ""):
                        self.in_snippet = True
                        self.current = ""

                def handle_endtag(self, tag):
                    if self.in_snippet and tag == "td":
                        self.in_snippet = False
                        if self.current.strip():
                            self.snippets.append(self.current.strip())

                def handle_data(self, data):
                    if self.in_snippet:
                        self.current += data

            parser = SnippetParser()
            parser.feed(resp2.text)
            if parser.snippets:
                return "\n".join(parser.snippets[:max_results])

            return ""
    except Exception as e:
        print(f"Web search error: {e}")
        return ""


async def generate_sse(message: str, history: list[dict]):
    try:
        from openai import AsyncOpenAI
        from app.config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

        client = AsyncOpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

        # Step 1: Try RAG
        context_text = "暂无相关资料"
        try:
            chunks = await retrieve(message, k=3)
            if chunks:
                context_text = "\n".join([f"- {text}" for text, score in chunks])
        except Exception:
            pass

        # Step 2: If RAG returned nothing and question is bridge-related, try web search
        if context_text == "暂无相关资料" and is_bridge_related(message):
            search_results = await web_search(message)
            if search_results:
                context_text = "（以下内容来自网络搜索，请参考并结合你的知识回答）\n" + search_results

        # Build system prompt based on available context
        if context_text != "暂无相关资料":
            system_prompt = f"""你是「檐下千秋」的AI助手，专门回答关于中国古桥的问题。请基于以下参考资料回答用户问题，资料中不包含的信息可以结合你的知识补充，但需诚实说明。

参考资料：
{context_text}

请用中文回答，回答简洁专业。使用 Markdown 格式，适当使用**加粗**、- 列表、### 标题等来组织内容。如引用网络搜索结果，可注明"据网络资料"。"""
        else:
            system_prompt = f"""你是「檐下千秋」的AI助手，专门回答关于中国古桥、传统文化、建筑美学相关的问题。请用你的知识回答用户问题。

用户问题：{message}

请用中文回答，回答简洁专业。如果问题与中国古桥无关，可以友好地引导用户提问古桥相关问题。"""

        messages = [{"role": "system", "content": system_prompt}]
        for h in history[-10:]:
            messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
        messages.append({"role": "user", "content": message})

        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=True
        )

        async for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                delta = chunk.choices[0].delta.content
                yield f"data: {json.dumps({'delta': delta})}\n\n"

        yield "data: [DONE]\n\n"

    except Exception as e:
        fallback = f"感谢您的提问。目前AI服务暂不可用（{str(e)[:100]}），请稍后再试。您也可以浏览我们的桥梁地图和知识图谱来了解中国古桥。"
        for char in fallback:
            yield f"data: {json.dumps({'delta': char})}\n\n"
        yield "data: [DONE]\n\n"


@router.post("/chat/stream")
async def chat_stream(body: ChatRequest):
    return StreamingResponse(
        generate_sse(body.message, body.history),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
