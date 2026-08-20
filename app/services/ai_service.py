"""
AI Home Designer — Master Design Specification Pipeline
=======================================================
Generates 3 visually CONSISTENT images (Exterior, Interior, 3D) from a single
Master Design Specification extracted from the user prompt.

Pipeline:
  USER PROMPT
    → parse_design_spec()     (keyword extraction — no external API needed)
    → MASTER DESIGN SPEC      (single source of truth)
    → Design DNA String       (injected into ALL 3 prompts)
    → build_exterior_prompt() / build_interior_prompt() / build_3d_prompt()
    → Pollinations Flux API   (same seed for all 3)
    → CONSISTENT RESULTS
"""

import random
import urllib.parse


# ──────────────────────────────────────────────────────────────────────────────
# SPEC EXTRACTION  — reliable keyword parser, no external API dependency
# ──────────────────────────────────────────────────────────────────────────────

def _num(word: str) -> int:
    """Convert number-word to int."""
    mapping = {"one": 1, "two": 2, "three": 3, "four": 4,
                "five": 5, "six": 6, "seven": 7, "eight": 8}
    return mapping.get(word, 0)


def parse_design_spec(prompt: str, style: str, budget: int, plot_size: int) -> dict:
    """
    Extract a structured Master Design Specification from the user prompt.
    This spec becomes the SINGLE SOURCE OF TRUTH for all 3 image generations.
    """
    p = prompt.lower()

    # ── FLOORS ────────────────────────────────────────────────────────────────
    floors = 2  # default
    for pattern, val in [
        (["single floor", "one floor", "1 floor", "single storey", "one storey",
          "1 storey", "single story", "one story", "ground floor only", "bungalow"], 1),
        (["two floor", "2 floor", "double storey", "two storey", "2 storey",
          "two story", "2 story", "two-floor", "two-storey", "2-floor"], 2),
        (["three floor", "3 floor", "three storey", "3 storey",
          "three story", "3 story", "three-storey"], 3),
        (["four floor", "4 floor", "four storey", "4 storey", "four story"], 4),
    ]:
        if any(kw in p for kw in pattern):
            floors = val
            break

    # ── BEDROOMS ──────────────────────────────────────────────────────────────
    bedrooms = 3  # default
    for i in range(8, 0, -1):
        word = ["", "one", "two", "three", "four", "five", "six", "seven", "eight"][i]
        if (f"{i} bedroom" in p or f"{i} bed room" in p or
                f"{word} bedroom" in p or f"{i}bhk" in p or f"{i} bhk" in p):
            bedrooms = i
            break

    # ── BATHROOMS ─────────────────────────────────────────────────────────────
    bathrooms = 2  # default
    for i in range(6, 0, -1):
        word = ["", "one", "two", "three", "four", "five", "six"][i]
        if (f"{i} bathroom" in p or f"{i} bath" in p or f"{word} bathroom" in p):
            bathrooms = i
            break

    # ── PRIMARY COLOR ─────────────────────────────────────────────────────────
    color_map = {
        "white": "warm white", "off-white": "warm off-white", "cream": "warm cream",
        "beige": "warm beige", "grey": "light grey", "gray": "light grey",
        "dark grey": "dark charcoal grey", "charcoal": "charcoal grey",
        "black": "matte black", "brown": "warm brown", "terracotta": "terracotta",
        "brick red": "warm brick red", "red": "warm red brick", "blue": "coastal blue",
        "navy": "deep navy blue", "green": "olive green", "sage": "sage green",
        "yellow": "warm honey yellow", "gold": "champagne gold",
        "lavender": "soft lavender", "purple": "deep plum", "pink": "blush pink",
    }
    primary_color = "warm white"
    for color_key, color_val in color_map.items():
        if color_key in p:
            primary_color = color_val
            break

    # ── SECONDARY / ACCENT ────────────────────────────────────────────────────
    secondary = "natural stone"
    if any(w in p for w in ["walnut", "oak", "teak", "cedar", "bamboo", "timber", "wood"]):
        wood_type = "walnut wood"
        if "oak" in p: wood_type = "natural oak wood"
        if "teak" in p: wood_type = "warm teak wood"
        if "cedar" in p: wood_type = "cedar wood"
        secondary = wood_type
    elif "stone" in p:
        secondary = "natural stone"
    elif "brick" in p:
        secondary = "exposed brick"
    elif "metal" in p or "steel" in p:
        secondary = "brushed steel"

    # ── MATERIALS ─────────────────────────────────────────────────────────────
    materials = []
    material_keywords = {
        "concrete": "architectural concrete",
        "glass": "large floor-to-ceiling glass",
        "wood": "natural wood cladding",
        "walnut": "walnut wood panels",
        "oak": "natural oak wood",
        "stone": "natural stone cladding",
        "marble": "polished marble",
        "brick": "exposed brick",
        "steel": "brushed steel",
        "zinc": "zinc cladding",
        "copper": "copper cladding",
        "travertine": "travertine stone",
        "limestone": "limestone cladding",
        "render": "smooth render",
        "stucco": "textured stucco",
        "corten": "corten weathering steel",
    }
    for kw, mat in material_keywords.items():
        if kw in p:
            materials.append(mat)
    if not materials:
        materials = ["white concrete", "natural stone", "glass"]

    # ── WINDOWS ───────────────────────────────────────────────────────────────
    windows = "large modern windows"
    if any(w in p for w in ["floor-to-ceiling", "floor to ceiling", "full height", "panoramic"]):
        windows = "large floor-to-ceiling glass windows"
    if "black frame" in p or "black-frame" in p or "dark frame" in p:
        windows = "large black-framed floor-to-ceiling glass windows"
    if "skylight" in p:
        windows += " with skylights"

    # ── ROOF ──────────────────────────────────────────────────────────────────
    roof = "modern flat roof"
    if any(w in p for w in ["sloped roof", "pitched roof", "slanting roof", "gable"]):
        roof = "sloped pitched roof"
    elif any(w in p for w in ["hip roof", "hipped"]):
        roof = "hipped roof"
    elif any(w in p for w in ["flat roof", "contemporary roof", "modern roof"]):
        roof = "flat contemporary roof"
    if "green roof" in p or "rooftop garden" in p:
        roof += " with rooftop garden"

    # ── EXTERIOR FEATURES ─────────────────────────────────────────────────────
    has_pool = any(w in p for w in ["swimming pool", "pool", "lap pool", "infinity pool"])
    has_balcony = any(w in p for w in ["balcony", "balconies", "glass railing balcony"])
    has_terrace = any(w in p for w in ["rooftop terrace", "terrace", "roof terrace"])
    has_garden = any(w in p for w in ["garden", "landscap", "lawn", "yard"])
    has_parking = any(w in p for w in ["parking", "garage", "car park", "carport"])
    has_courtyard = any(w in p for w in ["courtyard", "inner court"])

    # ── INTERIOR FEATURES ─────────────────────────────────────────────────────
    kitchen_type = "modular kitchen"
    if "open kitchen" in p:
        kitchen_type = "open-plan modular kitchen"
    elif "island" in p and "kitchen" in p:
        kitchen_type = "modular kitchen with large island"
    elif "traditional kitchen" in p:
        kitchen_type = "traditional kitchen"

    has_home_theatre = any(w in p for w in ["home theatre", "home theater", "cinema room"])
    has_study = any(w in p for w in ["study", "home office", "library", "reading room"])
    has_gym = any(w in p for w in ["gym", "fitness", "workout"])

    # ── FLOORING ──────────────────────────────────────────────────────────────
    flooring = "large-format porcelain tiles"
    if "marble" in p and ("floor" in p or "interior" in p):
        flooring = "large-format polished marble"
    elif "hardwood" in p or "wood floor" in p:
        flooring = "wide-plank hardwood"
    elif "concrete floor" in p:
        flooring = "polished concrete"
    elif "travertine floor" in p:
        flooring = "travertine stone"

    # ── LIGHTING ──────────────────────────────────────────────────────────────
    lighting = "warm architectural lighting"
    if "natural light" in p or "sunlight" in p:
        lighting = "abundant natural daylight with warm accent lighting"
    elif "led" in p or "indirect" in p:
        lighting = "warm indirect LED architectural lighting"
    elif "warm" in p:
        lighting = "warm 3000K architectural lighting"

    # ── STYLE OVERRIDES from prompt ───────────────────────────────────────────
    # Allow prompt to override the selected style if explicitly stated
    effective_style = style
    style_keywords = {
        "Minimalist Scandinavian": ["scandinavian", "nordic", "scandi", "minimalist nordic"],
        "Modern Industrial": ["industrial", "loft", "warehouse style", "exposed concrete"],
        "Classic Luxury": ["classical", "neoclassical", "traditional luxury", "colonial",
                           "georgian", "mediterranean", "tuscan"],
        "Cyberpunk Futuristic": ["futuristic", "cyberpunk", "sci-fi", "ultra modern", "space age"],
    }
    for s, keywords in style_keywords.items():
        if any(kw in p for kw in keywords):
            effective_style = s
            break

    # ── DESIGN LANGUAGE ───────────────────────────────────────────────────────
    design_language_map = {
        "Minimalist Scandinavian": "clean minimalist Nordic design, white tones, natural wood, hygge warmth",
        "Modern Industrial": "industrial modern design, exposed concrete, steel, brick, dark tones",
        "Classic Luxury": "classic luxury design, ornate details, marble, gold accents, symmetrical",
        "Cyberpunk Futuristic": "cyberpunk futuristic design, LED strips, dark metal, neon accents, glass",
    }
    design_language = design_language_map.get(effective_style, "modern luxury architectural design")

    # Adjust for prompt content
    if any(w in p for w in ["luxury", "luxurious", "premium", "high-end", "opulent"]):
        design_language += ", premium luxury finish"
    if any(w in p for w in ["minimalist", "minimal", "simple", "clean"]):
        design_language += ", clean minimal lines"

    # ── VISUAL IDENTITY (the Design DNA shared across all 3 images) ───────────
    visual_identity = {
        "primary_color": primary_color,
        "secondary_color": secondary,
        "materials": materials,
        "windows": windows,
        "lighting": lighting,
        "design_language": design_language,
        "style": effective_style,
    }

    # ── ASSEMBLED SPEC ────────────────────────────────────────────────────────
    spec = {
        "original_prompt": prompt,
        "house": {
            "floors": floors,
            "architectural_style": effective_style,
            "design_language": design_language,
            "plot_size_sqft": plot_size,
            "budget_usd": budget,
        },
        "exterior": {
            "primary_color": primary_color,
            "secondary_color": secondary,
            "materials": materials,
            "windows": windows,
            "roof": roof,
            "has_balcony": has_balcony,
            "has_rooftop_terrace": has_terrace,
            "has_swimming_pool": has_pool,
            "has_landscaped_garden": has_garden,
            "has_parking": has_parking,
            "has_courtyard": has_courtyard,
        },
        "interior": {
            "style": effective_style,
            "flooring": flooring,
            "lighting": lighting,
            "kitchen_type": kitchen_type,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "has_home_theatre": has_home_theatre,
            "has_study": has_study,
            "has_gym": has_gym,
        },
        "visual_identity": visual_identity,
    }
    return spec


# ──────────────────────────────────────────────────────────────────────────────
# DESIGN DNA  — shared identity string injected into all 3 prompts
# ──────────────────────────────────────────────────────────────────────────────

def build_design_dna(spec: dict) -> str:
    """
    Creates a compact Visual Identity string (Design DNA) that is injected
    into ALL three prompts to enforce cross-image consistency.
    """
    vi = spec["visual_identity"]
    h = spec["house"]
    ext = spec["exterior"]
    materials_str = ", ".join(vi["materials"][:3])
    features = []
    if ext["has_swimming_pool"]: features.append("rectangular swimming pool")
    if ext["has_balcony"]: features.append("glass-railed balcony")
    if ext["has_rooftop_terrace"]: features.append("rooftop terrace")
    if ext["has_landscaped_garden"]: features.append("landscaped garden")
    features_str = ", ".join(features) if features else "landscaped garden"

    dna = (
        f"[DESIGN DNA: {h['floors']}-storey {vi['style']} residence. "
        f"Primary: {vi['primary_color']}. Accent: {vi['secondary_color']}. "
        f"Materials: {materials_str}. Windows: {vi['windows']}. "
        f"Roof: {ext['roof']}. Features: {features_str}. "
        f"Lighting: {vi['lighting']}. Language: {vi['design_language']}.]"
    )
    return dna


# ──────────────────────────────────────────────────────────────────────────────
# PROMPT BUILDERS
# ──────────────────────────────────────────────────────────────────────────────

def build_exterior_prompt(spec: dict, dna: str) -> str:
    h = spec["house"]
    ext = spec["exterior"]
    vi = spec["visual_identity"]

    materials_str = " and ".join(ext["materials"][:4])
    features = []
    if ext["has_swimming_pool"]: features.append("a rectangular swimming pool")
    if ext["has_balcony"]: features.append("a spacious glass-railed balcony")
    if ext["has_rooftop_terrace"]: features.append("a rooftop terrace")
    if ext["has_landscaped_garden"]: features.append("a landscaped tropical garden")
    if ext["has_parking"]: features.append("a covered car parking area")
    if ext["has_courtyard"]: features.append("an inner courtyard")
    features_str = (", ".join(features) + ". ") if features else ""

    prompt = (
        f"Professional photorealistic architectural exterior visualization. "
        f"{dna} "
        f"Subject: A {h['floors']}-storey {h['architectural_style']} luxury residence. "
        f"The facade is finished in {ext['primary_color']} with {ext['secondary_color']} accents. "
        f"Materials used: {materials_str}. "
        f"Windows: {ext['windows']}. Roof: {ext['roof']}. "
        f"{features_str}"
        f"Camera: eye-level three-quarter front perspective, wide architectural composition. "
        f"Lighting: golden hour warm natural sunlight, realistic shadows, HDR sky. "
        f"Rendering: ultra-photorealistic, physically based materials, realistic reflections, "
        f"sharp architectural details, high dynamic range, professional architectural photography, "
        f"architectural magazine quality, 8K resolution. "
        f"Negative: no cartoon, no illustration, no warped geometry, no extra floors, "
        f"no floating objects, no text, no watermark, no generic building."
    )
    return prompt


def build_interior_prompt(spec: dict, dna: str) -> str:
    h = spec["house"]
    interior = spec["interior"]
    vi = spec["visual_identity"]
    ext = spec["exterior"]

    special_rooms = []
    if interior["has_home_theatre"]: special_rooms.append("home theatre")
    if interior["has_study"]: special_rooms.append("home office/study")
    if interior["has_gym"]: special_rooms.append("home gym")
    special_str = (", ".join(special_rooms) + ", ") if special_rooms else ""

    prompt = (
        f"Professional photorealistic interior architectural visualization of THE SAME HOUSE. "
        f"{dna} "
        f"Subject: The open-plan living room of this {h['architectural_style']} {h['floors']}-storey luxury residence. "
        f"CRITICAL: This interior MUST visually belong to the same house shown on the exterior. "
        f"Maintain IDENTICAL: {ext['primary_color']} walls, {vi['secondary_color']} accents, "
        f"{ext['windows']} matching the exterior, {vi['lighting']} — same architectural DNA throughout. "
        f"Room: Spacious open-plan living room with {interior['flooring']} flooring, "
        f"premium contemporary furniture, {interior['kitchen_type']} visible in background, "
        f"{special_str}large windows matching the exterior facade. "
        f"Interior style: {vi['design_language']}. "
        f"Camera: eye-level wide-angle 24mm lens, realistic perspective, straight vertical lines. "
        f"Lighting: {interior['lighting']}, realistic bounce light, warm ambient. "
        f"Rendering: ultra-photorealistic, physically accurate materials, realistic shadows, "
        f"professional interior architectural photography, architectural magazine quality, 8K. "
        f"Negative: no mismatched style, no rustic/industrial/cartoon interior if not requested, "
        f"no empty room, no generic hotel lobby, no text, no warped furniture."
    )
    return prompt


def build_3d_prompt(spec: dict, dna: str) -> str:
    h = spec["house"]
    ext = spec["exterior"]
    vi = spec["visual_identity"]

    materials_str = ", ".join(ext["materials"][:3])
    features = []
    if ext["has_swimming_pool"]: features.append("swimming pool visible from above")
    if ext["has_landscaped_garden"]: features.append("landscaped garden")
    if ext["has_balcony"]: features.append("balconies visible")
    if ext["has_parking"]: features.append("parking area")
    features_str = (", ".join(features) + ". ") if features else ""

    prompt = (
        f"Professional photorealistic architectural 3D top-down visualization. "
        f"{dna} "
        f"Subject: A roof-removed top-down isometric 3D architectural view of THE SAME {h['floors']}-storey "
        f"{h['architectural_style']} residence shown in this project. "
        f"The roof is COMPLETELY REMOVED revealing all interior rooms from directly above. "
        f"Camera: orthographic top-down view at exactly 90 degrees looking straight down, "
        f"elevated three-quarter isometric perspective. "
        f"Exterior walls in {ext['primary_color']}, {ext['secondary_color']} accent walls, "
        f"materials: {materials_str}. "
        f"{features_str}"
        f"Interior visible: hardwood flooring, furniture from above, warm room lighting, "
        f"room divisions clearly visible with thick dark charcoal walls. "
        f"Rendering: ultra-photorealistic 3D architectural visualization, "
        f"physically based rendering, realistic shadows from above, warm interior lighting, "
        f"vibrant realistic colors, sharp wall edges, professional architectural 3D studio quality, 8K. "
        f"Negative: no first-person view, no corridor view, no hallway perspective, "
        f"no floating camera inside rooms, no dark unlit rooms, no cartoon, no watermark."
    )
    return prompt


# ──────────────────────────────────────────────────────────────────────────────
# IMAGE URL BUILDER
# ──────────────────────────────────────────────────────────────────────────────

def build_pollinations_url(prompt: str, seed: int, width: int = 1280, height: int = 960) -> str:
    encoded = urllib.parse.quote(prompt)
    return (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width={width}&height={height}&nologo=true&seed={seed}&model=flux&enhance=true"
    )


# ──────────────────────────────────────────────────────────────────────────────
# MAIN SERVICE CLASS
# ──────────────────────────────────────────────────────────────────────────────

class AIEngineService:

    @staticmethod
    async def generate_images(prompt: str, style: str, budget: int = 150000, plot_size: int = 2500):
        """
        Master Design Specification Pipeline.

        Step 1: Parse user prompt → structured design spec
        Step 2: Build Design DNA (visual identity shared by all 3 prompts)
        Step 3: Build specialized prompts for each image type
        Step 4: Generate all 3 images using the SAME seed for consistency
        Step 5: Return image URLs + full spec (for regeneration)
        """
        # Step 1 — Extract Master Design Specification
        spec = parse_design_spec(prompt, style, budget, plot_size)

        # Step 2 — Build Design DNA (injected into all 3 prompts)
        dna = build_design_dna(spec)

        # Step 3 — Build specialized prompts
        ext_prompt = build_exterior_prompt(spec, dna)
        int_prompt = build_interior_prompt(spec, dna)
        fp_prompt  = build_3d_prompt(spec, dna)

        # Step 4 — Single master seed for maximum consistency
        master_seed = random.randint(100000, 999999)

        # Step 5 — Generate all 3 at higher resolution (1280x960 for wider architectural shots)
        ext_url = build_pollinations_url(ext_prompt, seed=master_seed, width=1280, height=960)
        int_url = build_pollinations_url(int_prompt, seed=master_seed, width=1280, height=960)
        fp_url  = build_pollinations_url(fp_prompt,  seed=master_seed, width=1024, height=1024)

        return {
            "exterior_url": ext_url,
            "interior_url": int_url,
            "floorplan_url": fp_url,
            "spec": spec,           # returned so frontend can store it for regeneration
            "seed": master_seed,
        }

    @staticmethod
    async def regenerate_single_image(image_type: str, spec: dict, seed: int = None):
        """
        Regenerate ONE image using the SAME design spec.
        The spec is unchanged — only a new seed creates visual variation
        while preserving the same house design.

        image_type: "exterior" | "interior" | "3d"
        """
        if seed is None:
            seed = random.randint(100000, 999999)

        dna = build_design_dna(spec)

        if image_type == "exterior":
            prompt = build_exterior_prompt(spec, dna)
            url = build_pollinations_url(prompt, seed=seed, width=1280, height=960)
        elif image_type == "interior":
            prompt = build_interior_prompt(spec, dna)
            url = build_pollinations_url(prompt, seed=seed, width=1280, height=960)
        else:  # "3d"
            prompt = build_3d_prompt(spec, dna)
            url = build_pollinations_url(prompt, seed=seed, width=1024, height=1024)

        return {"url": url, "seed": seed}

    @staticmethod
    async def generate_cost_estimate(plot_size: int, budget: int, style: str, prompt: str):
        """
        Uses free Pollinations Text API with fallback to generate a JSON cost breakdown.
        """
        from openai import AsyncOpenAI
        import json

        client = AsyncOpenAI(
            api_key="pollinations",
            base_url="https://text.pollinations.ai/openai"
        )

        sys_prompt = (
            "You are an expert luxury architect and construction estimator. "
            "Return ONLY a raw JSON object. No markdown, no code blocks."
        )
        user_prompt = (
            f"Estimate construction cost for a {plot_size} sqft house, {style} style, "
            f"budget ${budget}. Requirements: {prompt}. "
            f"Return JSON with: 'total_estimated_cost' (string), 'cost_breakdown' (string), "
            f"'recommended_materials' (array of 5 strings), 'sustainability_score' (0-100), "
            f"'sustainability_tips' (array of 3 strings)."
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
            print(f"Cost estimate LLM error: {e}")
            # Intelligent fallback based on budget and style
            per_sqft = max(150, min(600, budget // plot_size))
            estimated = plot_size * per_sqft
            return json.dumps({
                "total_estimated_cost": f"${estimated:,.0f}",
                "cost_breakdown": (
                    "Foundation & Structure: 30%, "
                    "Exterior & Roofing: 20%, "
                    "Interior Finishes: 25%, "
                    "MEP (Mechanical/Electrical/Plumbing): 15%, "
                    "Landscaping & Misc: 10%"
                ),
                "recommended_materials": [
                    "Reinforced Concrete Frame",
                    "Low-E Double Glazed Glass",
                    "Natural Stone Cladding",
                    "Wide-Plank Engineered Hardwood",
                    "Architectural Porcelain Tiles"
                ],
                "sustainability_score": 82,
                "sustainability_tips": [
                    "Install rooftop solar panels to offset 60% of energy consumption",
                    "Use low-E triple-glazed windows to reduce heat transfer by 40%",
                    "Integrate rainwater harvesting system for garden and toilet flushing"
                ]
            })
