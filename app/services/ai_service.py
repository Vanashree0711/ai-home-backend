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

        # Build prompts directly from user input - clean and simple
        exterior_prompt = (
            f"Photorealistic exterior architectural render, {style} style house, "
            f"{plot_size} sqft, ${budget} budget. {prompt}. "
            f"Daytime golden hour lighting, professional architectural photography, ultra detailed, 8k resolution, no cartoon, no drawing"
        )

        interior_prompt = (
            f"Photorealistic interior architectural render, {style} style living room, "
            f"{plot_size} sqft house. {prompt}. "
            f"Wide angle shot, professional interior photography, soft natural light, ultra detailed, 8k resolution, no cartoon, no drawing"
        )

        floorplan_prompt = (
            f"A photorealistic 3D architectural top-down floor plan layout showing the complete interior of a "
            f"{plot_size} sqft house in {style} style. "
            f"The roof is completely removed to reveal all interior rooms from directly above. "
            f"Camera looking straight down at 90 degrees, orthographic projection. "
            f"Thick structural interior walls with a solid dark charcoal slice-cut top fill, making wall divisions easily identifiable. "
            f"Warm inviting lighting, hardwood floors, highly detailed luxury architectural visualization, "
            f"vibrant realistic colors, contrasting walls. {prompt}"
        )

        safe_exterior = urllib.parse.quote(exterior_prompt)
        safe_interior = urllib.parse.quote(interior_prompt)
        safe_floorplan = urllib.parse.quote(floorplan_prompt)

        # Use a single master seed to enforce style consistency across all 3 images
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
