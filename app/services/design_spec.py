"""
Master Design Specification Parser
==================================
Extracts a complete, deterministic, and structured Master House Design Specification
from the user's natural language prompt, style selection, budget, and plot size.

This specification serves as the SINGLE SOURCE OF TRUTH for all downstream
architectural visualization, cost analysis, and blueprint compilation.
"""

import re
from typing import Dict, Any, List


def parse_master_design_specification(
    prompt: str,
    selected_style: str = "Minimalist Scandinavian",
    budget: int = 150000,
    plot_size: int = 2500
) -> Dict[str, Any]:
    """
    Analyzes natural language prompt and synthesizes a structured Master Design Specification.
    Strictly preserves user requirements without inventing conflicting elements.
    """
    p = prompt.lower()

    # --------------------------------------------------------------------------
    # 1. FLOORS (Strict adherence to user requirement)
    # --------------------------------------------------------------------------
    floors = 2  # Standard architectural default if unspecified
    if any(kw in p for kw in [
        "single floor", "one floor", "1 floor", "single storey", "one storey",
        "1 storey", "single story", "one story", "ground floor only", "bungalow",
        "single-floor", "single-storey", "single-story", "1-floor", "1-storey"
    ]):
        floors = 1
    elif any(kw in p for kw in [
        "two floor", "2 floor", "double storey", "two storey", "2 storey",
        "two story", "2 story", "two-floor", "two-storey", "two-story",
        "2-floor", "2-storey", "duplex", "double story"
    ]):
        floors = 2
    elif any(kw in p for kw in [
        "three floor", "3 floor", "triple storey", "three storey", "3 storey",
        "three story", "3 story", "three-storey", "3-floor", "triplex"
    ]):
        floors = 3
    elif any(kw in p for kw in [
        "four floor", "4 floor", "four storey", "4 storey", "four story", "4 story"
    ]):
        floors = 4

    # --------------------------------------------------------------------------
    # 2. ARCHITECTURAL STYLE & HOUSE TYPE
    # --------------------------------------------------------------------------
    style = selected_style
    house_type = "Modern Residential Home"

    if any(kw in p for kw in ["traditional indian", "kerala style", "chettinad", "haveli", "courtyard house", "indian style", "aangan", "pooja room"]):
        style = "Traditional Indian"
        house_type = "Traditional Indian Heritage Courtyard Residence"
    elif any(kw in p for kw in ["classic luxury", "classical", "neoclassical", "mansion", "palace", "colonial", "georgian", "victorian", "estate"]):
        style = "Classic Luxury"
        house_type = "Luxury Neoclassical Estate"
    elif any(kw in p for kw in ["industrial", "loft", "urban loft", "concrete and steel", "exposed brick"]):
        style = "Modern Industrial"
        house_type = "Modern Industrial Loft Residence"
    elif any(kw in p for kw in ["scandinavian", "nordic", "scandi", "hygge", "minimalist"]):
        style = "Minimalist Scandinavian"
        house_type = "Scandinavian Minimalist Home"
    elif any(kw in p for kw in ["cyberpunk", "futuristic", "sci-fi", "ultra modern"]):
        style = "Cyberpunk Futuristic"
        house_type = "Futuristic High-Tech Residence"
    elif any(kw in p for kw in ["cottage", "farmhouse", "rustic", "cabin"]):
        style = "Rustic Farmhouse / Cottage"
        house_type = "Country Farmhouse Residence"
    elif any(kw in p for kw in ["mediterranean", "spanish revival", "tuscan", "villa"]):
        style = "Mediterranean Villa"
        house_type = "Mediterranean Luxury Villa"
    elif any(kw in p for kw in ["budget house", "compact house", "small house", "tiny house", "affordable house"]):
        house_type = "Compact Efficient Residence"

    # --------------------------------------------------------------------------
    # 3. BEDROOMS & BATHROOMS
    # --------------------------------------------------------------------------
    bedrooms = 3
    bhk_match = re.search(r'(\d+)\s*(?:bhk|bedroom|bed\s*room|bed)', p)
    if bhk_match:
        bedrooms = int(bhk_match.group(1))
    else:
        word_to_num = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8}
        for word, val in word_to_num.items():
            if f"{word} bedroom" in p or f"{word} bed" in p or f"{word} bhk" in p:
                bedrooms = val
                break

    bathrooms = max(1, min(bedrooms, 4))
    bath_match = re.search(r'(\d+)\s*(?:bathroom|bath\s*room|bath)', p)
    if bath_match:
        bathrooms = int(bath_match.group(1))
    else:
        word_to_num = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6}
        for word, val in word_to_num.items():
            if f"{word} bathroom" in p or f"{word} bath" in p:
                bathrooms = val
                break

    # --------------------------------------------------------------------------
    # 4. EXTERIOR ATTRIBUTES (Colors, Materials, Windows, Roof, Features)
    # --------------------------------------------------------------------------
    exterior_colors: List[str] = []
    color_map = {
        "white": "warm white", "off-white": "off-white", "cream": "cream",
        "beige": "warm beige", "grey": "slate grey", "gray": "slate grey",
        "charcoal": "dark charcoal", "black": "matte black", "terracotta": "terracotta red",
        "brick red": "warm brick red", "red": "warm brick red", "brown": "natural earth brown",
        "lavender": "soft lavender", "blue": "coastal blue", "green": "sage green"
    }
    for kw, val in color_map.items():
        if kw in p and val not in exterior_colors:
            exterior_colors.append(val)
    if not exterior_colors:
        exterior_colors = ["warm white", "natural wood tones"]

    primary_color = exterior_colors[0] if exterior_colors else "warm white"
    secondary_color = exterior_colors[1] if len(exterior_colors) > 1 else "natural wood"

    exterior_materials: List[str] = []
    material_map = {
        "wood": "natural wood cladding", "walnut": "walnut timber", "oak": "natural oak timber",
        "teak": "solid teak wood", "timber": "engineered timber", "stone": "natural stone cladding",
        "brick": "exposed brickwork", "concrete": "smooth architectural concrete",
        "glass": "high-performance glass", "steel": "structural steel", "slate": "natural slate",
        "terracotta": "terracotta clay tiles", "marble": "exterior stone panels"
    }
    for kw, val in material_map.items():
        if kw in p and val not in exterior_materials:
            exterior_materials.append(val)
    if not exterior_materials:
        exterior_materials = ["smooth concrete render", "natural timber accents", "clear glass"]

    if "floor-to-ceiling" in p or "floor to ceiling" in p or "large glass window" in p:
        windows = "large floor-to-ceiling glass windows"
    elif "black frame" in p or "black-frame" in p:
        windows = "large black-framed panoramic windows"
    elif "traditional" in p or "wooden window" in p:
        windows = "handcrafted wooden framed windows with shutters"
    elif "arched" in p:
        windows = "elegant arched architectural windows"
    else:
        windows = "expansive contemporary glass windows"

    if any(kw in p for kw in ["terracotta roof", "clay roof", "sloped tile", "tiled roof", "mangalore tile"]):
        roof = "sloping terracotta tile roof"
    elif any(kw in p for kw in ["pitched roof", "sloped roof", "gable roof", "gable"]):
        roof = "pitched gable roof"
    elif any(kw in p for kw in ["flat roof", "flat contemporary", "rooftop terrace"]):
        roof = "flat contemporary roof with terrace"
    else:
        roof = "flat contemporary roof" if style in ["Modern Luxury", "Minimalist Scandinavian", "Modern Industrial"] else "sloped pitched roof"

    doors = "grand pivot wooden entrance door"
    if "carved" in p or "traditional" in p:
        doors = "hand-carved traditional teak wood door"
    elif "glass door" in p:
        doors = "modern glass and steel pivot door"

    has_pool = ("pool" in p or "swimming pool" in p) and not ("no pool" in p or "no swimming pool" in p)
    has_balcony = ("balcony" in p or "terrace" in p) and not ("no balcony" in p)
    has_garden = ("garden" in p or "lawn" in p or "landscap" in p or "yard" in p)
    has_parking = ("parking" in p or "garage" in p or "carport" in p or "car park" in p)
    has_courtyard = ("courtyard" in p or "aangan" in p or "inner court" in p)
    has_porch = ("porch" in p or "verandah" in p or "patio" in p or "deck" in p)

    # --------------------------------------------------------------------------
    # 5. INTERIOR ATTRIBUTES (Flooring, Lighting, Materials, Colors, Furniture)
    # --------------------------------------------------------------------------
    if "red oxide" in p:
        flooring = "traditional polished red oxide flooring"
    elif "marble" in p:
        flooring = "large-format polished Italian marble"
    elif "hardwood" in p or "wood floor" in p or "oak floor" in p:
        flooring = "wide-plank natural hardwood flooring"
    elif "concrete" in p:
        flooring = "polished architectural concrete"
    elif "terracotta" in p:
        flooring = "handcrafted terracotta floor tiles"
    else:
        flooring = "large-format porcelain tiles and hardwood"

    if "brass" in p or "traditional" in p:
        lighting = "warm brass hanging lamps and natural daylight"
    elif "led" in p or "indirect" in p:
        lighting = "warm indirect LED architectural cove lighting"
    else:
        lighting = "warm natural daylight paired with ambient recessed lighting"

    interior_materials: List[str] = []
    if "wood" in p or "walnut" in p or "teak" in p or "oak" in p:
        interior_materials.append("natural timber woodwork")
    if "marble" in p:
        interior_materials.append("polished marble")
    if "stone" in p:
        interior_materials.append("natural stone accents")
    if not interior_materials:
        interior_materials = ["natural wood", "soft textiles", "polished stone"]

    interior_colors = list(dict.fromkeys(exterior_colors + ["soft beige", "warm ivory"]))

    if "teak" in p or "traditional" in p:
        furniture = "handcrafted teak wood furniture with artisanal finishes"
    elif style == "Classic Luxury":
        furniture = "neoclassical luxury upholstered designer furniture"
    elif style == "Modern Industrial":
        furniture = "minimalist industrial steel and leather furniture"
    else:
        furniture = "contemporary minimalist designer furniture"

    # --------------------------------------------------------------------------
    # 6. ROOMS & SPECIAL REQUIREMENTS
    # --------------------------------------------------------------------------
    rooms = [f"{bedrooms} Bedrooms", f"{bathrooms} Bathrooms", "Living Room", "Kitchen & Dining"]
    if has_courtyard:
        rooms.append("Central Open Courtyard (Aangan)")
    if "pooja" in p or "prayer" in p:
        rooms.append("Dedicated Pooja Room")
    if "office" in p or "study" in p:
        rooms.append("Home Office / Study")
    if "theatre" in p or "theater" in p:
        rooms.append("Home Theatre")
    if "gym" in p:
        rooms.append("Home Gym")
    if has_porch:
        rooms.append("Covered Verandah / Porch")

    special_requirements: List[str] = []
    if has_pool: special_requirements.append("Swimming Pool")
    if has_garden: special_requirements.append("Landscaped Garden")
    if has_parking: special_requirements.append("Covered Parking / Garage")
    if has_courtyard: special_requirements.append("Central Open Courtyard")
    if has_balcony: special_requirements.append("Balcony / Terrace Deck")
    if "no pool" in p: special_requirements.append("Strictly No Swimming Pool")
    if "budget" in p: special_requirements.append("Cost-Optimized Design")

    # --------------------------------------------------------------------------
    # 7. ASSEMBLE MASTER DESIGN SPECIFICATION SCHEMA
    # --------------------------------------------------------------------------
    master_spec = {
        "house_type": house_type,
        "architectural_style": style,
        "floors": floors,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "plot_size_sqft": plot_size,
        "budget_usd": budget,
        "exterior": {
            "primary_color": primary_color,
            "secondary_color": secondary_color,
            "colors": exterior_colors,
            "materials": exterior_materials,
            "windows": windows,
            "doors": doors,
            "roof": roof,
            "balcony": has_balcony,
            "pool": has_pool,
            "garden": has_garden,
            "parking": has_parking,
            "courtyard": has_courtyard,
            "porch": has_porch
        },
        "interior": {
            "style": style,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "colors": interior_colors,
            "materials": interior_materials,
            "flooring": flooring,
            "lighting": lighting,
            "furniture": furniture
        },
        "house": {
            "architectural_style": style,
            "floors": floors,
            "house_type": house_type,
            "plot_size_sqft": plot_size,
            "budget_usd": budget
        },
        "rooms": rooms,
        "special_requirements": special_requirements,
        "original_prompt": prompt
    }

    return master_spec
