import random
import urllib.parse
from app.services.design_spec import parse_master_design_specification


class AIEngineService:

    @staticmethod
    async def generate_images(prompt: str, style: str, budget: int = 150000, plot_size: int = 2500):
        # 1. Master Design Specification (Single Source of Truth)
        spec = parse_master_design_specification(prompt, style, budget, plot_size)

        # 2. Master Seed for color & aesthetic synchronicity across views
        master_seed = random.randint(1, 1000000)

        # 3. Formulate prompts respecting the Master Design Specification
        theme_anchor = f"{spec['architectural_style']} home with design requirements: {prompt}"

        # Exterior View
        exterior_prompt = (
            f"A photorealistic exterior architectural render of a {plot_size} sqft house in {spec['architectural_style']} style. "
            f"Budget constraints: ${budget}. {prompt}. "
            f"Front elevation view showing clean architectural facade, large floor-to-ceiling glass windows with warm indoor lighting visible inside, "
            f"balcony with glass railing, modern geometry, beautiful landscaping with garden plants, soft natural daylight and twilight glow, "
            f"professional architectural photography, 8k resolution"
        )

        # Interior View (Matching the same house specification)
        interior_prompt = (
            f"A photorealistic interior architectural render of the modern living room inside the SAME {spec['architectural_style']} house, {plot_size} sqft. "
            f"{prompt}. "
            f"Large floor-to-ceiling glass windows matching the exterior architecture, soft warm ambient lighting, elegant modern sofa, "
            f"matching wall color palette and textures, professional architectural digest photography, 8k resolution"
        )
        
        # 3D Architectural View (Matching the same house specification)
        floorplan_prompt = (
            f"A photorealistic 3D architectural top-down floor plan layout showing the complete interior of the SAME {plot_size} sqft house in {spec['architectural_style']} style. "
            f"The roof is completely removed to reveal all interior rooms from directly above. "
            f"Camera looking straight down at 90 degrees, orthographic projection. "
            f"Thick structural interior walls with a solid dark charcoal slice-cut top fill, making wall divisions easily identifiable. "
            f"Warm inviting lighting, hardwood floors, furnished bedrooms, modern bathrooms, kitchen and living spaces. "
            f"Vibrant realistic colors matching the house theme: {prompt}"
        )

        safe_exterior = urllib.parse.quote(exterior_prompt)
        safe_interior = urllib.parse.quote(interior_prompt)
        safe_floorplan = urllib.parse.quote(floorplan_prompt)

        # Unified parameters across all three images
        ext_url = f"https://image.pollinations.ai/prompt/{safe_exterior}?width=1024&height=1024&nologo=true&seed={master_seed}&model=flux&enhance=true"
        int_url = f"https://image.pollinations.ai/prompt/{safe_interior}?width=1024&height=1024&nologo=true&seed={master_seed}&model=flux&enhance=true"
        fp_url  = f"https://image.pollinations.ai/prompt/{safe_floorplan}?width=1024&height=1024&nologo=true&seed={master_seed}&model=flux&enhance=true"

        return {
            "exterior_url": ext_url,
            "interior_url": int_url,
            "floorplan_url": fp_url,
            "spec": spec,
            "seed": master_seed,
        }

    @staticmethod
    async def regenerate_single_image(image_type: str, spec: dict, seed: int = None):
        if seed is None:
            seed = random.randint(1, 1000000)

        prompt_str = spec.get("original_prompt", "")
        style = spec.get("architectural_style") or spec.get("house", {}).get("architectural_style", "Minimalist Scandinavian")
        budget = spec.get("budget_usd") or spec.get("house", {}).get("budget_usd", 150000)
        plot_size = spec.get("plot_size_sqft") or spec.get("house", {}).get("plot_size_sqft", 2500)

        if image_type == "exterior":
            prompt = (
                f"A photorealistic exterior architectural render of a {plot_size} sqft house in {style} style. "
                f"Budget constraints: ${budget}. {prompt_str}. "
                f"Front elevation view showing clean architectural facade, large floor-to-ceiling glass windows with warm indoor lighting visible inside, "
                f"balcony with glass railing, modern geometry, beautiful landscaping with garden plants, soft natural daylight and twilight glow, "
                f"professional architectural photography, 8k resolution"
            )
        elif image_type == "interior":
            prompt = (
                f"A photorealistic interior architectural render of the modern living room inside the SAME {style} house, {plot_size} sqft. "
                f"{prompt_str}. "
                f"Large floor-to-ceiling glass windows matching the exterior architecture, soft warm ambient lighting, elegant modern sofa, "
                f"matching wall color palette and textures, professional architectural digest photography, 8k resolution"
            )
        else:  # "3d"
            prompt = (
                f"A photorealistic 3D architectural top-down floor plan layout showing the complete interior of the SAME {plot_size} sqft house in {style} style. "
                f"The roof is completely removed to reveal all interior rooms from directly above. "
                f"Camera looking straight down at 90 degrees, orthographic projection. "
                f"Thick structural interior walls with a solid dark charcoal slice-cut top fill, making wall divisions easily identifiable. "
                f"Warm inviting lighting, hardwood floors, furnished bedrooms, modern bathrooms, kitchen and living spaces. "
                f"Vibrant realistic colors matching the house theme: {prompt_str}"
            )

        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1024&height=1024&nologo=true&seed={seed}&model=flux&enhance=true"
        return {"url": url, "seed": seed}

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
