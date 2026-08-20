import json
import httpx
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()

async def stream_ai_architect(prompt: str):
    """
    Streams AI responses from Pollinations OpenAI-compatible POST endpoint.
    POST endpoint is more reliable and not rate limited like the GET endpoint.
    """
    system_message = (
        "You are an expert AI Architect and Interior Designer with 20 years of experience. "
        "Provide concise, professional, and creative advice on home design, "
        "building materials, structural engineering, interior layout, and architecture. "
        "Always give practical, specific recommendations."
    )

    payload = {
        "model": "openai-large",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "stream": True
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
    }

    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            async with client.stream(
                "POST",
                "https://text.pollinations.ai/openai",
                json=payload,
                headers=headers
            ) as response:
                if response.status_code == 429:
                    # Rate limited - return a helpful message instead of raw error
                    yield f"data: {json.dumps({'text': 'The AI is currently busy. Please wait a moment and try again!'})}\n\n"
                    yield "data: [DONE]\n\n"
                    return

                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            content = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if content:
                                yield f"data: {json.dumps({'text': content})}\n\n"
                        except Exception:
                            pass

        yield "data: [DONE]\n\n"

    except Exception as e:
        print(f"Chat stream error: {str(e)}")
        yield f"data: {json.dumps({'text': 'Sorry, the AI is temporarily unavailable. Please try again in a moment!'})}\n\n"
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
