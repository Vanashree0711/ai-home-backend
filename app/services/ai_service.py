import openai
from app.core.config import settings
import asyncio

# Initialize OpenAI Client
openai.api_key = settings.OPENAI_API_KEY

class AIEngineService:
    
    @staticmethod
    async def generate_images(prompt: str, style: str, budget: int = 150000, plot_size: int = 2500):
        """
        Generates Exterior and Interior concepts using a free API.
        """
        import random
        import urllib.parse
        
        # Include budget and plot size in the prompt so the AI respects it!
        exterior_prompt = f"Photorealistic exterior architectural render, {style} style house, {plot_size} sqft, ${budget} budget. {prompt}. Daytime golden hour lighting, professional architectural photography, ultra detailed, 8k"
        interior_prompt = f"Photorealistic interior render, {style} style living room, {plot_size} sqft house. {prompt}. Wide angle shot, professional interior photography, ultra detailed, 8k"
        floorplan_prompt = f"3D isometric cutaway architectural floor plan, {style} style house, {plot_size} sqft. Roof removed to show all rooms from above at 45 degree isometric angle. Rooms colored differently: living room in warm beige, kitchen in soft blue, bedrooms in pale green, bathrooms in light grey. Thick solid walls, realistic furniture inside each room, clean pastel color palette, professional architectural visualization, bright natural daylight, high detail"
        
        safe_exterior = urllib.parse.quote(exterior_prompt)
        safe_interior = urllib.parse.quote(interior_prompt)
        safe_floorplan = urllib.parse.quote(floorplan_prompt)
        
        # Use a single master seed to enforce color and geometric consistency across all 3 images
        master_seed = random.randint(1, 1000000)
        fp_seed = random.randint(1, 1000000)  # Separate seed for floor plan so it doesn't mimic exterior

        ext_url = f"https://image.pollinations.ai/prompt/{safe_exterior}?width=1024&height=1024&nologo=true&seed={master_seed}&model=flux&enhance=true"
        int_url = f"https://image.pollinations.ai/prompt/{safe_interior}?width=1024&height=1024&nologo=true&seed={master_seed}&model=flux&enhance=true"
        fp_url = f"https://image.pollinations.ai/prompt/{safe_floorplan}?width=1024&height=1024&nologo=true&seed={fp_seed}&model=flux&enhance=false"

        return {
            "exterior_url": ext_url,
            "interior_url": int_url,
            "floorplan_url": fp_url
        }

    @staticmethod
    async def generate_cost_estimate(plot_size: int, budget: int, style: str, prompt: str):
        """
        Uses Pollinations Text API (via AsyncOpenAI) to generate a detailed JSON cost breakdown, material list, and sustainability score.
        """
        from openai import AsyncOpenAI
        import json
        
        client = AsyncOpenAI(
            api_key="pollinations",
            base_url="https://text.pollinations.ai/openai"
        )
        
        sys_prompt = "You are an expert luxury architect and construction estimator. Return ONLY a raw JSON object containing the specified keys. Do not include markdown code block syntax (like ```json)."
        user_prompt = f"Provide a detailed construction cost estimate, material recommendation, and sustainability score out of 100 for a {plot_size} sqft house in {style} style with a budget of ${budget}. User requirements: {prompt}. The JSON must have these exact keys: 'total_estimated_cost', 'cost_breakdown' (string), 'recommended_materials' (array of strings), 'sustainability_score' (number), 'sustainability_tips' (array of strings)."
        
        try:
            response = await client.chat.completions.create(
                model="openai",
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            result_text = response.choices[0].message.content
            return result_text
        except Exception as e:
            print(f"Pollinations Text Error: {str(e)}")
            return json.dumps({
                "total_estimated_cost": f"${budget}",
                "cost_breakdown": f"Detailed cost calculation failed, falling back to budget default. Primary cost centers: foundation, structure framing, plumbing, electrical, and interior finishes.",
                "recommended_materials": ["Reinforced Concrete", "Low-E Double Glazed Glass", "Recycled Steel Beams", "Sustainable Timber"],
                "sustainability_score": 85,
                "sustainability_tips": ["Install solar panels", "Use low-E glass windows", "Integrate rainwater harvesting system"]
            })
