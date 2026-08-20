import asyncio

class AIEngineService:

    @staticmethod
    async def generate_images(prompt: str, style: str, budget: int = 150000, plot_size: int = 2500):
        """
        Generates Exterior, Interior and Floor Plan images using free Pollinations Flux API.
        Takes the raw user prompt directly - no OpenAI parsing needed.
        """
        import random
        import urllib.parse

        # USER PROMPT IS THE MAIN DRIVER - put it first and most prominently
        exterior_prompt = (
            f"{prompt}. "
            f"This is a {style} style home, {plot_size} sqft, built with a ${budget} budget. "
            f"Photorealistic exterior architectural render. Professional architectural photography. "
            f"Beautiful landscaping, realistic materials, ultra detailed, cinematic lighting, 8k resolution. "
            f"No cartoon, no illustration, no sketch, no generic building."
        )

        interior_prompt = (
            f"{prompt}. "
            f"This is the interior living room of a {style} style home, {plot_size} sqft. "
            f"Photorealistic interior architectural photography. "
            f"Wide angle shot showing the full room, professional staging, soft natural light, "
            f"ultra detailed, realistic furniture and materials, 8k resolution. "
            f"No cartoon, no illustration, no empty room."
        )

        floorplan_prompt = (
            f"Photorealistic 3D architectural top-down floor plan of a {style} style house, {plot_size} sqft. "
            f"Based on this design: {prompt}. "
            f"The roof is completely removed showing all interior rooms from directly above at 90 degrees. "
            f"Orthographic top-down camera. Thick dark charcoal walls. "
            f"Warm lighting inside rooms, hardwood floors, realistic furniture visible from above, "
            f"vibrant colors, highly detailed luxury visualization. "
            f"No hallway perspective, no corridor view, no first-person view."
        )

        safe_exterior = urllib.parse.quote(exterior_prompt)
        safe_interior = urllib.parse.quote(interior_prompt)
        safe_floorplan = urllib.parse.quote(floorplan_prompt)

        # Use a single master seed for style consistency across all 3 images
        master_seed = random.randint(1, 1000000)

        ext_url = f"https://image.pollinations.ai/prompt/{safe_exterior}?width=1024&height=1024&nologo=true&seed={master_seed}&model=flux&enhance=true"
        int_url = f"https://image.pollinations.ai/prompt/{safe_interior}?width=1024&height=1024&nologo=true&seed={master_seed}&model=flux&enhance=true"
        fp_url  = f"https://image.pollinations.ai/prompt/{safe_floorplan}?width=1024&height=1024&nologo=true&seed={master_seed}&model=flux&enhance=true"

        return {
            "exterior_url": ext_url,
            "interior_url": int_url,
            "floorplan_url": fp_url
        }

    @staticmethod
    async def generate_cost_estimate(plot_size: int, budget: int, style: str, prompt: str):
        """
        Uses free Pollinations Text API to generate a detailed JSON cost breakdown,
        material list, and sustainability score. No API key required.
        """
        from openai import AsyncOpenAI
        import json

        # Use Pollinations free LLM endpoint - completely free, no key needed
        client = AsyncOpenAI(
            api_key="pollinations",
            base_url="https://text.pollinations.ai/openai"
        )

        sys_prompt = (
            "You are an expert luxury architect and construction estimator. "
            "Return ONLY a raw JSON object containing the specified keys. "
            "Do not include markdown code block syntax like ```json. "
            "Respond with raw JSON only."
        )

        user_prompt = (
            f"Provide a detailed construction cost estimate, material recommendation, and sustainability score "
            f"for a {plot_size} sqft house in {style} style with a budget of ${budget}. "
            f"User requirements: {prompt}. "
            f"The JSON must have these exact keys: "
            f"'total_estimated_cost' (string like '$450,000'), "
            f"'cost_breakdown' (string describing cost split), "
            f"'recommended_materials' (array of 5 strings), "
            f"'sustainability_score' (number 0-100), "
            f"'sustainability_tips' (array of 3 strings)."
        )

        try:
            response = await client.chat.completions.create(
                model="openai",
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Pollinations LLM Error: {str(e)}")
            return json.dumps({
                "total_estimated_cost": f"${budget:,}",
                "cost_breakdown": "Foundation & Structure: 30%, Exterior & Roofing: 20%, Interior Finishes: 25%, MEP (Mechanical/Electrical/Plumbing): 15%, Landscaping & Misc: 10%",
                "recommended_materials": [
                    "Reinforced Concrete Frame",
                    "Low-E Double Glazed Glass",
                    "Recycled Steel Beams",
                    "Sustainable Hardwood Timber",
                    "Natural Stone Cladding"
                ],
                "sustainability_score": 82,
                "sustainability_tips": [
                    "Install rooftop solar panels to offset 60% of energy consumption",
                    "Use low-E glass windows to reduce heat transfer and HVAC load",
                    "Integrate a rainwater harvesting system for garden irrigation"
                ]
            })
