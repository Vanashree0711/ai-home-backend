import json
import httpx
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()

async def stream_ai_architect(prompt: str):
    """
    Streams AI responses from Pollinations Text API using direct HTTP.
    Uses the simple GET endpoint which is the most reliable free option.
    """
    system_message = (
        "You are an expert AI Architect and Interior Designer with 20 years of experience. "
        "Provide concise, professional, and creative advice on home design, "
        "building materials, structural engineering, interior layout, and architecture. "
        "Always give practical, specific recommendations."
    )

    full_prompt = f"{system_message}\n\nUser question: {prompt}\n\nAnswer:"

    import urllib.parse
    encoded_prompt = urllib.parse.quote(full_prompt)
    url = f"https://text.pollinations.ai/{encoded_prompt}"

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("GET", url) as response:
                async for chunk in response.aiter_text():
                    if chunk:
                        # Stream each chunk as SSE data
                        yield f"data: {json.dumps({'text': chunk})}\n\n"
        yield "data: [DONE]\n\n"
    except Exception as e:
        print(f"Chat stream error: {str(e)}")
        # Fallback: return a static helpful message if streaming fails
        fallback = (
            "I'm your AI Architect assistant! I can help with home design, "
            "materials, layout planning, and construction costs. "
            "Please try asking your question again."
        )
        yield f"data: {json.dumps({'text': fallback})}\n\n"
        yield "data: [DONE]\n\n"

@router.get("/stream")
async def chat_stream(prompt: str):
    return StreamingResponse(
        stream_ai_architect(prompt),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
