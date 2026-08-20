import random
import urllib.parse
from app.services.design_spec import parse_master_design_specification
from app.services.prompt_engine import (
    generate_all_specialized_prompts,
    build_exterior_prompt,
    build_interior_prompt,
    build_3d_prompt
)


class AIEngineService:

    @staticmethod
    async def generate_images(prompt: str, style: str, budget: int = 150000, plot_size: int = 2500):
        # 1. Master Design Specification (Single Source of Truth - Stage 1)
        spec = parse_master_design_specification(prompt, style, budget, plot_size)

        # 2. Specialized Image Prompt Engine (Stage 2)
        specialized_prompts = generate_all_specialized_prompts(spec)

        # 3. Master Seed for color, material & atmospheric synchronization
        master_seed = random.randint(1, 1000000)

        safe_exterior = urllib.parse.quote(specialized_prompts["exterior_prompt"])
        safe_interior = urllib.parse.quote(specialized_prompts["interior_prompt"])
        safe_floorplan = urllib.parse.quote(specialized_prompts["floorplan_prompt"])

        # Unified parameters across all three image pipelines
        ext_url = f"https://image.pollinations.ai/prompt/{safe_exterior}?width=1024&height=1024&nologo=true&seed={master_seed}&model=flux&enhance=true"
        int_url = f"https://image.pollinations.ai/prompt/{safe_interior}?width=1024&height=1024&nologo=true&seed={master_seed}&model=flux&enhance=true"
        fp_url  = f"https://image.pollinations.ai/prompt/{safe_floorplan}?width=1024&height=1024&nologo=true&seed={master_seed}&model=flux&enhance=true"

        return {
            "exterior_url": ext_url,
            "interior_url": int_url,
            "floorplan_url": fp_url,
            "spec": spec,
            "seed": master_seed,
            "prompts": specialized_prompts
        }

    @staticmethod
    async def regenerate_single_image(image_type: str, spec: dict, seed: int = None):
        if seed is None:
            seed = random.randint(1, 1000000)

        if image_type == "exterior":
            prompt = build_exterior_prompt(spec)
        elif image_type == "interior":
            prompt = build_interior_prompt(spec)
        else:  # "3d"
            prompt = build_3d_prompt(spec)

        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1024&height=1024&nologo=true&seed={seed}&model=flux&enhance=true"
        return {"url": url, "seed": seed, "prompt": prompt}

    @staticmethod
    async def generate_cost_estimate(plot_size: int, budget: int, style: str, prompt: str):
        from openai import AsyncOpenAI
        import json

        client = AsyncOpenAI(
            api_key="pollinations",
            base_url="https://text.pollinations.ai/openai"
        )

        sys_prompt = "You are an expert luxury architect and construction estimator. Return ONLY a raw JSON object. No markdown, no code blocks."
        user_prompt = (
            f"Estimate construction cost for a {plot_size} sqft house, {style} style, budget ${budget}. "
            f"Requirements: {prompt}. Return JSON with: 'total_estimated_cost' (string), 'cost_breakdown' (string), "
            f"'recommended_materials' (array of 5 strings), 'sustainability_score' (0-100), 'sustainability_tips' (array of 3 strings)."
        )

        try:
            response = await client.chat.completions.create(
                model="openai",
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                timeout=20
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Cost estimate error: {e}")
            return json.dumps({
                "total_estimated_cost": f"${budget:,}",
                "cost_breakdown": "Foundation & Structure: 30%, Exterior & Roofing: 20%, Interior Finishes: 25%, MEP: 15%, Landscaping: 10%",
                "recommended_materials": ["Reinforced Concrete", "Glass", "Wood", "Steel", "Stone"],
                "sustainability_score": 85,
                "sustainability_tips": ["Install solar panels", "Use low-E glass", "Rainwater harvesting"]
            })
