import json
import httpx
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()

async def stream_ai_architect(prompt: str):
    """
    Tries multiple free LLM endpoints with fallback.
    """
    system_message = (
        "You are an expert AI Architect and Interior Designer with 20 years of experience. "
        "Provide professional, detailed, and creative advice on home design, building materials, "
        "structural engineering, interior layout, and architecture. Be specific and helpful."
    )

    payload = {
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "stream": True
    }

    # Try multiple free endpoints in order
    endpoints = [
        {
            "url": "https://text.pollinations.ai/openai",
            "payload": {**payload, "model": "openai"},
            "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
        },
        {
            "url": "https://text.pollinations.ai/openai",
            "payload": {**payload, "model": "mistral"},
            "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
        }
    ]

    for endpoint in endpoints:
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream(
                    "POST",
                    endpoint["url"],
                    json=endpoint["payload"],
                    headers=endpoint["headers"]
                ) as response:
                    if response.status_code in [429, 403, 500, 503]:
                        print(f"Endpoint {endpoint['url']} returned {response.status_code}, trying next...")
                        continue

                    got_content = False
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data_str = line[6:]
                            if data_str == "[DONE]":
                                break
                            try:
                                data = json.loads(data_str)
                                content = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                                if content:
                                    got_content = True
                                    yield f"data: {json.dumps({'text': content})}\n\n"
                            except Exception:
                                pass

                    if got_content:
                        yield "data: [DONE]\n\n"
                        return

        except Exception as e:
            print(f"Endpoint failed: {str(e)}, trying next...")
            continue

    # All endpoints failed — use a smart rule-based response
    response_text = get_rule_based_response(prompt)
    # Stream it word by word to simulate typing effect
    words = response_text.split(' ')
    for i, word in enumerate(words):
        text = word + (' ' if i < len(words) - 1 else '')
        yield f"data: {json.dumps({'text': text})}\n\n"

    yield "data: [DONE]\n\n"


def get_rule_based_response(prompt: str) -> str:
    """Smart rule-based architectural advisor as fallback."""
    prompt_lower = prompt.lower()

    if any(w in prompt_lower for w in ['floor', 'flooring', 'tile', 'marble', 'wood', 'hardwood']):
        return ("For luxury home flooring, I recommend these top options:\n\n"
                "1. **Marble** — The ultimate luxury choice. Calacatta and Carrara marble offer timeless elegance. Best for entrance halls, bathrooms, and formal living rooms. Cost: $50-$200/sqft installed.\n\n"
                "2. **Engineered Hardwood** — More stable than solid wood, resistant to humidity changes. White Oak and Walnut are the most popular for modern luxury homes. Cost: $15-$40/sqft installed.\n\n"
                "3. **Porcelain Large Format Tiles** — 120x120cm or larger tiles create a seamless, contemporary look with minimal grout lines. Perfect for open plan spaces. Cost: $20-$80/sqft installed.\n\n"
                "4. **Travertine Stone** — Natural, warm, and earthy. Excellent for Mediterranean or classic styles. Cost: $25-$75/sqft.\n\n"
                "**My recommendation:** For a true luxury feel, use Calacatta marble in the entrance and bathrooms, paired with wide-plank white oak hardwood in the living and bedroom areas.")

    elif any(w in prompt_lower for w in ['material', 'exterior', 'facade', 'cladding', 'wall']):
        return ("The best exterior materials for a luxury home are:\n\n"
                "1. **Natural Limestone Ashlar** — Used in the finest European estates. Extremely durable, ages beautifully, and gives a timeless prestigious appearance. Cost: $80-$200/sqft.\n\n"
                "2. **Architectural Concrete** — Smooth board-formed or polished concrete gives a bold contemporary look. Incredibly durable and low maintenance. Cost: $40-$100/sqft.\n\n"
                "3. **Corten Steel Panels** — Develops a natural rust-red patina that protects the steel underneath. Striking industrial-modern aesthetic. Cost: $60-$150/sqft.\n\n"
                "4. **Zinc or Copper Cladding** — Premium metal cladding that develops a beautiful patina over time. Used in high-end contemporary architecture globally. Cost: $70-$180/sqft.\n\n"
                "5. **Natural Timber Cladding** — Thermally modified wood (Accoya or Kebony) is extremely stable and durable outdoors, requiring minimal maintenance.")

    elif any(w in prompt_lower for w in ['cost', 'budget', 'price', 'expensive', 'cheap', 'afford']):
        return ("Here is a realistic construction cost breakdown for a luxury home:\n\n"
                "**Cost per Square Foot (Luxury Grade):**\n"
                "• Basic structure & foundation: $80-$120/sqft\n"
                "• Exterior envelope (walls, roof, windows): $60-$100/sqft\n"
                "• Interior finishes (luxury grade): $100-$200/sqft\n"
                "• MEP (Mechanical, Electrical, Plumbing): $60-$90/sqft\n"
                "• Landscaping: 10-15% of build cost\n\n"
                "**Total Luxury Home Cost Estimate:**\n"
                "• 2,000 sqft: $700,000 - $1,100,000\n"
                "• 3,500 sqft: $1,200,000 - $1,800,000\n"
                "• 5,000 sqft: $1,800,000 - $2,600,000\n\n"
                "**Key cost drivers:** Site conditions, location, material selection, and the complexity of the architectural design are the four biggest variables in final construction cost.")

    elif any(w in prompt_lower for w in ['safe', 'lake', 'flood', 'water', 'river', 'coastal', 'ocean', 'beach']):
        return ("Building near a lake or water body requires careful consideration of several factors:\n\n"
                "**✅ Safety Considerations:**\n"
                "1. **Flood Zone Assessment** — Check FEMA flood maps. If in a 100-year flood zone, your foundation must be elevated above the Base Flood Elevation (BFE) by at least 1-2 feet.\n\n"
                "2. **Foundation Type** — Use deep pile foundations (concrete piles driven 10-15m deep) or elevated slab-on-grade. Never use a standard shallow slab near water.\n\n"
                "3. **Moisture Protection** — All exterior materials must be rated for high humidity. Use pressure-treated lumber, marine-grade stainless steel fixings, and waterproof membranes on all below-grade walls.\n\n"
                "4. **Setback Requirements** — Most municipalities require 15-50 meter setbacks from the water's edge. Always check local regulations before designing.\n\n"
                "5. **Drainage** — Install a comprehensive French drain system around the perimeter and ensure the site grades away from the building at minimum 2% slope.\n\n"
                "**✅ With proper engineering, lakeside homes are absolutely safe and incredibly beautiful!**")

    elif any(w in prompt_lower for w in ['sustainable', 'eco', 'green', 'energy', 'solar', 'environment']):
        return ("Here are the most impactful sustainable design strategies for a luxury home:\n\n"
                "1. **Passive Solar Design** — Orient the house with the long axis East-West. Place large windows on the south-facing facade to capture winter sun and use deep overhangs to block summer sun.\n\n"
                "2. **High Performance Insulation** — Use mineral wool insulation (R-30 walls, R-60 roof) to dramatically reduce heating and cooling loads. Pair with triple-glazed windows (U-value < 0.8 W/m²K).\n\n"
                "3. **Solar PV System** — A 10kW rooftop solar array (approximately 30 panels) can offset 80-100% of a typical luxury home's electricity consumption.\n\n"
                "4. **Heat Pump HVAC** — Air-source or ground-source heat pumps are 300-400% efficient compared to gas boilers. They provide both heating and cooling from a single system.\n\n"
                "5. **Rainwater Harvesting** — A 10,000-liter underground cistern can collect enough rainwater for all landscape irrigation and toilet flushing needs.\n\n"
                "6. **Green Roof** — Reduces urban heat island effect, improves insulation, and manages stormwater runoff naturally.")

    elif any(w in prompt_lower for w in ['bedroom', 'bathroom', 'kitchen', 'living', 'layout', 'plan', 'room']):
        return ("Here are the key principles for luxury home room layout:\n\n"
                "**Bedroom Design:**\n"
                "• Primary suite minimum 40sqm including ensuite and walk-in wardrobe\n"
                "• Guest bedrooms minimum 20sqm with ensuite\n"
                "• Ceiling height minimum 3m for luxury feel\n\n"
                "**Kitchen Design:**\n"
                "• The 'work triangle' (sink-fridge-cooktop) should be max 6m perimeter total\n"
                "• Island minimum 1.2m x 2.4m with seating on one side\n"
                "• Separate prep kitchen/butler's pantry for large luxury homes\n\n"
                "**Living Areas:**\n"
                "• Open plan living/dining/kitchen works best for modern luxury\n"
                "• Formal living room should have direct access to outdoor entertaining area\n"
                "• Ceiling heights: 3m standard, 4-5m for feature spaces like entrance halls\n\n"
                "**General Principles:**\n"
                "• Always provide a visual axis through the home from entrance to garden\n"
                "• Separate guest circulation from family circulation in large homes\n"
                "• Every primary room should have access to natural daylight")

    else:
        return ("As your AI Architect, here is my expert advice:\n\n"
                "For any successful luxury home project, the three fundamental principles are:\n\n"
                "1. **Site Response** — The best architecture responds to its specific site. Study sun angles, prevailing winds, views, and topography before designing a single wall. A building that works WITH its site rather than against it will always perform better and look more natural.\n\n"
                "2. **Material Integrity** — Use materials honestly. If you use concrete, let it express its natural texture. If you use timber, let the grain show. Authentic material use creates timeless architecture that ages gracefully.\n\n"
                "3. **Spatial Sequence** — The journey through a home matters as much as the individual rooms. Design a clear sequence from arrival to private spaces — entry → living → dining → private zones — with moments of compression and expansion to create emotional impact.\n\n"
                f"Regarding your specific question about '{prompt}': I recommend consulting with a licensed architect in your region who can evaluate your specific site conditions, local building codes, and climate requirements to give you the most accurate and safe design recommendations.")


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
