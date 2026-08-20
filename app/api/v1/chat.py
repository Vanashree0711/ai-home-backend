import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI

router = APIRouter()

# Use 100% free Pollinations LLM - no API key needed
client = AsyncOpenAI(
    api_key="pollinations",
    base_url="https://text.pollinations.ai/openai"
)

async def stream_ai_architect(prompt: str):
    try:
        response = await client.chat.completions.create(
            model="openai",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert AI Architect and Interior Designer with 20 years of experience. "
                        "Provide concise, professional, highly detailed, and creative advice on home design, "
                        "building materials, structural engineering, interior layout, and architecture. "
                        "Always give practical, specific recommendations. Be helpful and thorough."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        async for chunk in response:
            if chunk.choices[0].delta.content is not None:
                text = chunk.choices[0].delta.content
                yield f"data: {json.dumps({'text': text})}\n\n"
        yield "data: [DONE]\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"
        yield "data: [DONE]\n\n"

@router.get("/stream")
async def chat_stream(prompt: str):
    return StreamingResponse(
        stream_ai_architect(prompt),
        media_type="text/event-stream"
    )
