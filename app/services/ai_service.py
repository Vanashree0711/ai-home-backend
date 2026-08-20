import random
import urllib.parse

def parse_design_spec(prompt: str, style: str, budget: int, plot_size: int) -> dict:
    p = prompt.lower()
    floors = 2
    if any(kw in p for kw in ["single floor", "one floor", "1 floor", "bungalow"]):
        floors = 1
    elif any(kw in p for kw in ["three floor", "3 floor", "three storey"]):
        floors = 3
        
    bedrooms = 3
    for i in range(6, 0, -1):
        if f"{i} bedroom" in p or f"{i} bhk" in p:
            bedrooms = i
            break
            
    bathrooms = 2
    for i in range(5, 0, -1):
        if f"{i} bathroom" in p or f"{i} bath" in p:
            bathrooms = i
            break

    materials = []
    if "wood" in p or "walnut" in p or "oak" in p:
        materials.append("Natural Wood")
    if "stone" in p:
        materials.append("Natural Stone")
    if "concrete" in p:
        materials.append("Concrete")
    if not materials:
        materials = ["Concrete", "Glass", "Wood"]

    return {
        "original_prompt": prompt,
        "house": {
            "floors": floors,
            "architectural_style": style,
            "plot_size_sqft": plot_size,
            "budget_usd": budget,
        },
        "exterior": {
            "primary_color": "warm white" if "white" in p else "grey" if "grey" in p else "natural tones",
            "secondary_color": "walnut wood" if "walnut" in p else "stone" if "stone" in p else "wood accents",
            "materials": materials,
            "roof": "flat roof" if "flat" in p else "pitched roof",
        },
        "interior": {
            "style": style,
            "flooring": "polished marble" if "marble" in p else "hardwood" if "wood" in p else "porcelain tiles",
            "lighting": "LED lighting" if "led" in p else "natural light",
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
        }
    }


class AIEngineService:

    @staticmethod
    async def generate_images(prompt: str, style: str, budget: int = 150000, plot_size: int = 2500):
        # Ultra HD Exterior prompt with photorealistic octane rendering keywords
        exterior_prompt = (
            f"masterpiece, best quality, ultra high resolution 8k, photorealistic architectural photography of a luxury {style} house exterior, {plot_size} sqft, ${budget} budget. "
            f"{prompt}. "
            f"shot on Hasselblad H6D-100c, 35mm architectural lens, crisp sharp focus, natural daylight, raytracing reflections, photorealistic foliage and landscaping, no blur, unreal engine 5 architecture render, archdaily featured"
        )

        # Ultra HD Interior prompt
        interior_prompt = (
            f"masterpiece, best quality, ultra high resolution 8k, photorealistic luxury interior design magazine photography of an expansive living room in a {style} house, {plot_size} sqft. "
            f"{prompt}. "
            f"shot on Canon EOS R5 24mm tilt-shift lens, soft ambient warm lighting, photorealistic textures, clean sharp reflections, modern designer furniture, architectural digest interior, crisp sharp details"
        )
        
        # Ultra HD Top-Down 3D Floorplan
        floorplan_prompt = (
            f"masterpiece, best quality, ultra high resolution 8k, clean 3D architectural top-down floor plan model, full house layout cutaway from directly above, "
            f"strictly 90 degree orthographic top-down view, bird's-eye aerial view, entire roof completely sliced away to reveal all furnished interior rooms, "
            f"thick dark charcoal cut walls, warm wooden floors, furnished bedrooms, modern bathrooms, kitchen and living room, clean architectural visualization diorama, "
            f"crisp sharp lines, beautiful soft studio lighting, high detail, V-Ray render, archdaily plan. {style} style house. {prompt}"
        )

        safe_exterior = urllib.parse.quote(exterior_prompt)
        safe_interior = urllib.parse.quote(interior_prompt)
        safe_floorplan = urllib.parse.quote(floorplan_prompt)

        # Separate seeds for clean rendering
        seed_ext = random.randint(1, 1000000)
        seed_int = random.randint(1, 1000000)
        seed_fp  = random.randint(1, 1000000)

        # High resolution 1024x1024 flux rendering
        ext_url = f"https://image.pollinations.ai/prompt/{safe_exterior}?width=1024&height=1024&nologo=true&seed={seed_ext}&model=flux&enhance=true"
        int_url = f"https://image.pollinations.ai/prompt/{safe_interior}?width=1024&height=1024&nologo=true&seed={seed_int}&model=flux&enhance=true"
        fp_url  = f"https://image.pollinations.ai/prompt/{safe_floorplan}?width=1024&height=1024&nologo=true&seed={seed_fp}&model=flux&enhance=true"

        spec = parse_design_spec(prompt, style, budget, plot_size)

        return {
            "exterior_url": ext_url,
            "interior_url": int_url,
            "floorplan_url": fp_url,
            "spec": spec,
            "seed": seed_ext,
        }

    @staticmethod
    async def regenerate_single_image(image_type: str, spec: dict, seed: int = None):
        if seed is None:
            seed = random.randint(1, 1000000)

        prompt_str = spec["original_prompt"]
        style = spec["house"]["architectural_style"]
        budget = spec["house"]["budget_usd"]
        plot_size = spec["house"]["plot_size_sqft"]

        if image_type == "exterior":
            prompt = (
                f"masterpiece, best quality, ultra high resolution 8k, photorealistic architectural photography of a luxury {style} house exterior, {plot_size} sqft, ${budget} budget. "
                f"{prompt_str}. "
                f"shot on Hasselblad H6D-100c, 35mm architectural lens, crisp sharp focus, natural daylight, raytracing reflections, photorealistic foliage and landscaping, no blur, unreal engine 5 architecture render, archdaily featured"
            )
        elif image_type == "interior":
            prompt = (
                f"masterpiece, best quality, ultra high resolution 8k, photorealistic luxury interior design magazine photography of an expansive living room in a {style} house, {plot_size} sqft. "
                f"{prompt_str}. "
                f"shot on Canon EOS R5 24mm tilt-shift lens, soft ambient warm lighting, photorealistic textures, clean sharp reflections, modern designer furniture, architectural digest interior, crisp sharp details"
            )
        else:  # "3d"
            prompt = (
                f"masterpiece, best quality, ultra high resolution 8k, clean 3D architectural top-down floor plan model, full house layout cutaway from directly above, "
                f"strictly 90 degree orthographic top-down view, bird's-eye aerial view, entire roof completely sliced away to reveal all furnished interior rooms, "
                f"thick dark charcoal cut walls, warm wooden floors, furnished bedrooms, modern bathrooms, kitchen and living room, clean architectural visualization diorama, "
                f"crisp sharp lines, beautiful soft studio lighting, high detail, V-Ray render, archdaily plan. {style} style house. {prompt_str}"
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
