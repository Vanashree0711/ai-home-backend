"""
Master House Design Specification & Spatial Blueprint Engine — INTELLIGENT ARCHITECT v2
========================================================================================
Operates as an AI Architect + Interior Designer + 3D Visualizer.

Pipeline:
  USER PROMPT → UNDERSTAND INTENT → PROFESSIONAL DESIGN DECISIONS → MASTER SPECIFICATION
  → 3 CONSISTENT VIEWS (Exterior + Interior + 3D Isometric Floor Plan)

Principles:
  1. USER INTENT FIRST — every detail in the prompt shapes the design.
  2. STYLE INTELLIGENCE — each style has its own material palette, colors, furniture, lighting.
  3. ONE HOUSE — all 3 views derive from a single locked Master Specification.
  4. INTELLIGENT DEFAULTS — missing details are filled by professional architectural logic.
  5. ENVIRONMENTAL ACCURACY — if user says "lake", the lake appears; "beach" means ocean is present.
"""

import re
from typing import Dict, Any, List


# ══════════════════════════════════════════════════════════════════════════════
# STYLE KNOWLEDGE BASE — Professional architectural DNA per style
# ══════════════════════════════════════════════════════════════════════════════
STYLE_DNA = {
    "Minimalist Scandinavian": {
        "facade_color": "smooth bright white render",
        "accent_color": "dark charcoal",
        "wood_tone": "light blonde natural oak",
        "roof": "dark charcoal low-pitched standing-seam metal roof",
        "windows": "large black-framed floor-to-ceiling glass windows",
        "door": "dark charcoal pivot door with vertical glass sidelights",
        "flooring": "light natural blonde oak wide-plank hardwood",
        "walls_int": "smooth matte white interior walls",
        "ceiling": "smooth flat white ceiling",
        "furniture": "light grey linen sofa, oak coffee table, sheepskin rug, wicker wishbone chair",
        "lighting": "soft abundant natural daylight, dome pendant lamp, warm ambient floor lamp",
        "materials_ext": ["smooth white render", "natural oak timber", "clear glass"],
        "materials_int": ["natural oak wood", "linen fabric", "wool", "glass"],
        "landscape": "manicured lawn with mature pine and birch trees",
        "atmosphere": "calm, airy, hygge warmth with abundant natural light",
    },
    "Modern Luxury": {
        "facade_color": "warm off-white smooth plaster",
        "accent_color": "polished dark steel",
        "wood_tone": "dark walnut",
        "roof": "ultra-flat minimal roof with thin shadow-gap parapet",
        "windows": "large floor-to-ceiling frameless glass walls",
        "door": "wide pivot door in brushed black steel with flush handle",
        "flooring": "large-format Italian porcelain marble 120x120cm",
        "walls_int": "smooth white plaster with subtle texture",
        "ceiling": "architectural coffered ceiling with warm 2700K LED cove lighting",
        "furniture": "Italian leather sectional sofa, Carrara marble coffee table, designer accent chairs",
        "lighting": "warm 2700K recessed LED cove lighting, dramatic pendant above dining, natural light",
        "materials_ext": ["smooth plaster render", "black anodized aluminium", "structural glass"],
        "materials_int": ["Carrara marble", "dark walnut", "brushed stainless steel", "Italian leather"],
        "landscape": "manicured rectangular lawn with infinity pool and stone pathway",
        "atmosphere": "refined elegance, dramatic lighting, premium finishes",
    },
    "Modern Industrial": {
        "facade_color": "raw architectural concrete grey",
        "accent_color": "weathered Corten steel",
        "wood_tone": "dark reclaimed timber",
        "roof": "flat concrete roof with exposed edge beam",
        "windows": "oversized steel-framed factory-style windows",
        "door": "heavy steel sliding barn door with industrial hardware",
        "flooring": "polished concrete with visible aggregate",
        "walls_int": "raw exposed brick and smooth concrete",
        "ceiling": "exposed steel beam ceiling with industrial pendant lamps",
        "furniture": "black leather sofa, reclaimed wood coffee table, steel shelving",
        "lighting": "industrial Edison bulb pendant clusters, exposed conduit track lighting",
        "materials_ext": ["architectural concrete", "Corten weathering steel", "dark glass"],
        "materials_int": ["exposed brick", "raw concrete", "reclaimed timber", "steel"],
        "landscape": "urban courtyard with gravel ground, steel planters, and olive trees",
        "atmosphere": "raw, urban, edgy with warm reclaimed timber contrasts",
    },
    "Classic Luxury": {
        "facade_color": "warm ivory limestone",
        "accent_color": "polished gold and wrought iron",
        "wood_tone": "rich mahogany",
        "roof": "classical pitched hip roof with terracotta or slate tiles",
        "windows": "symmetrical arched sash windows with gold trim",
        "door": "grand double mahogany door with ornate brass hardware and pilasters",
        "flooring": "herringbone pattern dark oak parquet or Calacatta marble",
        "walls_int": "warm ivory painted walls with crown moulding and wainscoting",
        "ceiling": "decorative coffered ceiling with gold leaf chandelier",
        "furniture": "Chesterfield velvet sofa, antique mahogany side tables, Persian rug",
        "lighting": "gold crystal chandelier, gilded wall sconces, warm 2700K ambient",
        "materials_ext": ["limestone cladding", "polished stone", "ornate ironwork"],
        "materials_int": ["mahogany wood", "Calacatta marble", "velvet", "gold leaf", "brass"],
        "landscape": "formal symmetrical garden with clipped hedges, fountain, and gravel path",
        "atmosphere": "grandeur, opulence, timeless elegance",
    },
    "Traditional Indian": {
        "facade_color": "warm ochre yellow or terracotta",
        "accent_color": "carved wood brown and deep red",
        "wood_tone": "solid teak",
        "roof": "sloping Mangalore terracotta tile roof with extended eaves",
        "windows": "carved wooden jali lattice windows with shutters",
        "door": "hand-carved ornate solid teak double door with brass fittings",
        "flooring": "polished red oxide or handmade terracotta tiles",
        "walls_int": "warm ochre painted walls with carved wood details",
        "ceiling": "wooden beam and plank ceiling with brass lamp pendants",
        "furniture": "handcrafted teak settee, jute dhurrie rug, brass accent pieces",
        "lighting": "warm brass hanging oil-lamp pendants and natural daylight through jali",
        "materials_ext": ["terracotta clay", "solid teak wood", "hand-cut stone"],
        "materials_int": ["teak wood", "red oxide", "brass", "jute", "handwoven textiles"],
        "landscape": "shaded courtyard with banana and neem trees, tulsi plant, stone water feature",
        "atmosphere": "heritage warmth, artisanal craft, earthy tones, natural ventilation",
    },
    "Mediterranean Villa": {
        "facade_color": "warm sun-bleached white render",
        "accent_color": "terracotta orange and cobalt blue",
        "wood_tone": "reclaimed olive wood",
        "roof": "terracotta barrel tile roof with wide overhanging eaves",
        "windows": "arched openings with dark iron grilles and shutters",
        "door": "arched heavy timber double door with wrought iron detailing",
        "flooring": "handmade terracotta floor tiles or patterned Zellige mosaic",
        "walls_int": "textured lime plaster in warm white with arched doorways",
        "ceiling": "exposed terracotta tile ceiling with reclaimed wood beams",
        "furniture": "linen sofa in warm sand tones, mosaic side tables, ceramic decorative vases",
        "lighting": "wrought iron lantern pendants, candlelight, natural light through arched openings",
        "materials_ext": ["lime render", "terracotta", "reclaimed timber", "wrought iron"],
        "materials_int": ["terracotta", "lime plaster", "zellige tile", "linen", "wrought iron"],
        "landscape": "terraced garden with olive and citrus trees, pergola with climbing vines, pool",
        "atmosphere": "sun-drenched, relaxed, Mediterranean warmth and texture",
    },
    "Cyberpunk Futuristic": {
        "facade_color": "matte dark graphite with neon-lit panels",
        "accent_color": "electric blue and purple neon",
        "wood_tone": "none — carbon fibre and metal",
        "roof": "asymmetric angular blade roof with LED edge lighting",
        "windows": "smart electrochromic tinted glass panels",
        "door": "automated sliding titanium door with biometric panel",
        "flooring": "polished black resin with embedded LED grid lines",
        "walls_int": "dark matte panels with neon accent lighting strips",
        "ceiling": "suspended dark ceiling with blue-purple LED matrix lighting",
        "furniture": "modular pod seating, acrylic and carbon fibre tables, holographic displays",
        "lighting": "neon blue-purple ambient, LED matrix ceiling, dramatic underlighting",
        "materials_ext": ["dark anodized titanium panels", "smart glass", "carbon composite"],
        "materials_int": ["carbon fibre", "polished resin", "acrylic", "dark matte metal"],
        "landscape": "urban dystopian setting with neon signs, rain-slicked surface, elevated walkways",
        "atmosphere": "dramatic, cinematic, high-tech futurism with neon mood lighting",
    },
    "Rustic Farmhouse": {
        "facade_color": "white board-and-batten timber cladding",
        "accent_color": "aged black iron",
        "wood_tone": "rough-sawn barnwood",
        "roof": "steep gabled metal standing-seam roof in aged black or galvanized",
        "windows": "six-pane divided light farmhouse windows with black frames",
        "door": "classic dutch barn door in weathered timber with black hardware",
        "flooring": "wide-plank distressed pine or whitewashed oak",
        "walls_int": "shiplap white painted wood panels",
        "ceiling": "exposed rough timber beam ceiling with vintage Edison bulb pendants",
        "furniture": "overstuffed linen sofa, farm table with bench seating, rocking chair",
        "lighting": "Edison bulb vintage pendants, candlestick sconces, natural light",
        "materials_ext": ["board-and-batten timber", "corrugated metal roofing", "fieldstone"],
        "materials_int": ["reclaimed barnwood", "shiplap", "galvanized metal", "linen"],
        "landscape": "open countryside with split-rail fence, wildflower meadow, barn",
        "atmosphere": "warm country charm, rustic warmth, relaxed farmhouse living",
    },
}

def _get_style_dna(style: str) -> Dict[str, Any]:
    """Returns the style DNA for a given style, with fallback to Modern Luxury."""
    for key in STYLE_DNA:
        if key.lower() in style.lower() or style.lower() in key.lower():
            return STYLE_DNA[key]
    return STYLE_DNA["Modern Luxury"]


def parse_master_design_specification(
    prompt: str,
    selected_style: str = "Modern Luxury",
    budget: int = 150000,
    plot_size: int = 2500
) -> Dict[str, Any]:
    """
    INTELLIGENT ARCHITECT ENGINE:
    Analyzes the user prompt, applies professional design intelligence,
    and produces a complete immutable Master House Specification.

    Every architectural decision made here is reflected identically
    across the Exterior, Interior, and 3D Floor Plan views.
    """
    p = prompt.lower()

    # --------------------------------------------------------------------------
    # 1. FLOORS — Strict adherence to user requirement
    # --------------------------------------------------------------------------
    floors = 2  # Professional default for most residential designs
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

    # --------------------------------------------------------------------------
    # 2. ARCHITECTURAL STYLE — Detect from prompt, override selected_style if explicit
    # --------------------------------------------------------------------------
    style = selected_style
    house_type = "Modern Residential Home"

    if any(kw in p for kw in ["traditional indian", "kerala style", "chettinad", "haveli", "courtyard house", "indian style", "aangan", "pooja room", "mangalore", "terracotta roof"]):
        style = "Traditional Indian"
        house_type = "Traditional Indian Heritage Residence"
    elif any(kw in p for kw in ["classic luxury", "classical", "neoclassical", "mansion", "palace", "colonial", "georgian", "victorian", "estate", "grand"]):
        style = "Classic Luxury"
        house_type = "Luxury Neoclassical Estate"
    elif any(kw in p for kw in ["industrial", "loft", "urban loft", "concrete and steel", "exposed brick", "corten"]):
        style = "Modern Industrial"
        house_type = "Modern Industrial Loft Residence"
    elif any(kw in p for kw in ["scandinavian", "nordic", "scandi", "hygge"]):
        style = "Minimalist Scandinavian"
        house_type = "Scandinavian Minimalist Home"
    elif any(kw in p for kw in ["cyberpunk", "futuristic", "sci-fi", "ultra modern", "neon"]):
        style = "Cyberpunk Futuristic"
        house_type = "Futuristic High-Tech Residence"
    elif any(kw in p for kw in ["farmhouse", "rustic", "cabin", "barn"]):
        style = "Rustic Farmhouse"
        house_type = "Rustic Farmhouse Residence"
    elif any(kw in p for kw in ["mediterranean", "spanish revival", "tuscan", "villa", "greek"]):
        style = "Mediterranean Villa"
        house_type = "Mediterranean Luxury Villa"
    elif any(kw in p for kw in ["minimalist", "minimal", "clean lines"]):
        style = "Minimalist Scandinavian"
        house_type = "Minimalist Contemporary Home"
    elif any(kw in p for kw in ["modern", "luxury", "contemporary", "premium"]):
        style = "Modern Luxury"
        house_type = "Modern Luxury Residence"

    # Load professional style DNA
    dna = _get_style_dna(style)

    # --------------------------------------------------------------------------
    # 3. BEDROOMS & BATHROOMS
    # --------------------------------------------------------------------------
    bedrooms = 3
    bhk_match = re.search(r'(\d+)\s*(?:bhk|bedroom|bed\s*room|bed)', p)
    if bhk_match:
        bedrooms = int(bhk_match.group(1))
    else:
        word_to_num = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6}
        for word, val in word_to_num.items():
            if f"{word} bedroom" in p or f"{word} bed" in p or f"{word} bhk" in p:
                bedrooms = val
                break

    bathrooms = max(1, min(bedrooms, 3))
    bath_match = re.search(r'(\d+)\s*(?:bathroom|bath\s*room|bath)', p)
    if bath_match:
        bathrooms = int(bath_match.group(1))
    else:
        word_to_num = {"one": 1, "two": 2, "three": 3, "four": 4}
        for word, val in word_to_num.items():
            if f"{word} bathroom" in p or f"{word} bath" in p:
                bathrooms = val
                break

    # --------------------------------------------------------------------------
    # 4. ENVIRONMENT & SITE SETTING — User's location must physically appear
    # --------------------------------------------------------------------------
    # Detect explicit environment from prompt (these MUST appear in the final render)
    if any(kw in p for kw in ["private island", "on an island", "tropical island", "surrounded by ocean", "island home"]):
        environment = "private tropical island completely surrounded by turquoise ocean water, white sandy beach, and palm trees"
        env_tag = "island"
    elif any(kw in p for kw in ["lake", "lakeside", "lakefront", "near lake", "beside lake", "on the lake", "lake view"]):
        environment = "peaceful lakefront property directly beside a calm reflective blue lake with forested shores in the distance"
        env_tag = "lake"
    elif any(kw in p for kw in ["ocean", "beach", "coastal", "seaside", "sea view", "oceanfront", "near ocean", "beside ocean"]):
        environment = "oceanfront coastal property on a sandy beach with the blue ocean waves visible immediately beside the house"
        env_tag = "ocean"
    elif any(kw in p for kw in ["mountain", "cliff", "hillside", "hilltop", "mountain view"]):
        environment = "dramatic mountain hillside with sweeping panoramic valley views and pine forest below"
        env_tag = "mountain"
    elif any(kw in p for kw in ["forest", "pine forest", "woodland", "surrounded by trees", "in the woods"]):
        environment = "serene forest clearing with tall pine and birch trees surrounding the property on all sides"
        env_tag = "forest"
    elif any(kw in p for kw in ["desert", "arid", "sand dunes"]):
        environment = "dramatic desert landscape with red sand dunes and clear blue sky"
        env_tag = "desert"
    elif any(kw in p for kw in ["urban", "city", "downtown", "rooftop"]):
        environment = "modern urban city setting with city skyline visible in the background"
        env_tag = "urban"
    else:
        environment = dna["landscape"]
        env_tag = "suburban"

    # --------------------------------------------------------------------------
    # 5. COLORS — User overrides take priority, style DNA fills gaps
    # --------------------------------------------------------------------------
    exterior_colors: List[str] = []
    color_map = {
        "white": "bright white", "off-white": "warm off-white", "cream": "warm cream",
        "beige": "warm beige", "grey": "slate grey", "gray": "slate grey",
        "charcoal": "dark charcoal", "black": "matte black", "terracotta": "terracotta",
        "red": "warm brick red", "brown": "earthy brown", "yellow": "warm ochre yellow",
        "blue": "deep coastal blue", "green": "sage green", "lavender": "soft lavender",
        "gold": "warm gold", "copper": "warm copper", "bronze": "dark bronze",
    }
    for kw, val in color_map.items():
        if re.search(rf'\b{kw}\b', p) and val not in exterior_colors:
            exterior_colors.append(val)
    if not exterior_colors:
        # Use style DNA default colors
        exterior_colors = [dna["facade_color"], dna["accent_color"]]

    primary_color = exterior_colors[0]
    secondary_color = exterior_colors[1] if len(exterior_colors) > 1 else dna["accent_color"]

    # --------------------------------------------------------------------------
    # 6. MATERIALS — User overrides, style DNA fills gaps
    # --------------------------------------------------------------------------
    exterior_materials: List[str] = []
    material_map = {
        "wood": "natural wood cladding", "walnut": "walnut timber", "oak": "natural oak timber",
        "teak": "solid teak wood", "timber": "engineered timber cladding",
        "stone": "natural stone cladding", "brick": "exposed handmade brickwork",
        "concrete": "smooth architectural concrete", "glass": "high-performance structural glass",
        "steel": "weathered Corten steel", "slate": "dark natural slate", "copper": "patinated copper",
        "terracotta": "handmade terracotta clay tiles", "marble": "natural marble stone panels",
        "render": "smooth hand-applied stucco render",
    }
    for kw, val in material_map.items():
        if kw in p and val not in exterior_materials:
            exterior_materials.append(val)
    if not exterior_materials:
        exterior_materials = dna["materials_ext"]

    # --------------------------------------------------------------------------
    # 7. ARCHITECTURAL ELEMENTS — Windows, Doors, Roof
    # --------------------------------------------------------------------------
    # Windows
    if "floor-to-ceiling" in p or "floor to ceiling" in p:
        windows = "large black-framed floor-to-ceiling glass windows"
    elif "arched" in p or "arch" in p:
        windows = "elegant arched architectural windows with detailed frames"
    elif "jali" in p or "lattice" in p:
        windows = "carved wooden jali lattice windows with shutters"
    elif "skylight" in p:
        windows = "panoramic skylights and large glass windows"
    else:
        windows = dna["windows"]

    # Doors
    if "carved" in p:
        doors = "hand-carved ornate solid teak double entrance door"
    elif "glass door" in p or "pivot" in p:
        doors = "architectural pivot door with full-height glass panel"
    elif "double door" in p:
        doors = "grand double entrance door with sidelights"
    else:
        doors = dna["door"]

    # Roof
    if any(kw in p for kw in ["terracotta roof", "clay roof", "mangalore tile", "sloping roof", "tiled roof"]):
        roof = "sloping Mangalore terracotta tile roof with wide overhanging eaves"
    elif any(kw in p for kw in ["pitched roof", "gable roof", "peaked roof"]):
        roof = "steeply pitched gable roof"
    elif any(kw in p for kw in ["flat roof", "rooftop terrace", "rooftop pool"]):
        roof = "flat contemporary roof with accessible rooftop terrace"
    elif any(kw in p for kw in ["metal roof", "standing seam"]):
        roof = "dark metal standing-seam roof"
    else:
        roof = dna["roof"]

    # --------------------------------------------------------------------------
    # 8. EXTERIOR FEATURES
    # --------------------------------------------------------------------------
    has_pool = ("pool" in p or "swimming pool" in p) and "no pool" not in p
    has_balcony = ("balcony" in p or "terrace" in p) and "no balcony" not in p
    has_garden = "garden" in p or "lawn" in p or "landscap" in p or "yard" in p
    has_parking = "parking" in p or "garage" in p or "carport" in p
    has_courtyard = "courtyard" in p or "aangan" in p or "inner court" in p
    has_porch = "porch" in p or "verandah" in p or "patio" in p or "deck" in p

    # --------------------------------------------------------------------------
    # 9. INTERIOR FINISHES — User overrides, style DNA fills gaps
    # --------------------------------------------------------------------------
    if "red oxide" in p:
        flooring = "traditional polished red oxide flooring"
    elif "marble" in p and "floor" in p:
        flooring = "large-format polished Italian Calacatta marble 120x120cm tiles"
    elif "herringbone" in p:
        flooring = "herringbone-pattern natural oak parquet hardwood flooring"
    elif "hardwood" in p or "wood floor" in p or "oak floor" in p:
        flooring = "wide-plank natural oak hardwood flooring"
    elif "concrete floor" in p or "polished concrete" in p:
        flooring = "polished architectural concrete flooring with visible aggregate"
    elif "terracotta" in p and "floor" in p:
        flooring = "handmade terracotta floor tiles"
    else:
        flooring = dna["flooring"]

    lighting = dna["lighting"]
    if "brass" in p:
        lighting = "warm brass pendant lamps and soft natural daylight"
    elif "neon" in p:
        lighting = "electric blue-purple neon LED ambient lighting"
    elif "chandelier" in p:
        lighting = "grand crystal chandelier with warm 2700K ambient lighting"

    furniture = dna["furniture"]
    if "teak" in p and "furniture" in p:
        furniture = "handcrafted solid teak wood furniture with artisanal finishes"
    elif "rattan" in p or "wicker" in p:
        furniture = "natural rattan and wicker furniture with linen cushions"

    interior_materials = dna["materials_int"]

    ceiling_design = dna["ceiling"]
    if "beam" in p or "exposed beam" in p:
        ceiling_design = "exposed solid timber beam ceiling with recessed spot lighting"
    elif "coffered" in p:
        ceiling_design = "decorative coffered ceiling with warm LED lighting"

    # --------------------------------------------------------------------------
    # 10. SPATIAL BLUEPRINT — Room layout and connections
    # --------------------------------------------------------------------------
    staircase = (
        f"central open floating staircase along the interior side wall connecting ground to upper floor"
        if floors > 1 else "single level — no staircase"
    )
    entrance = f"front-center entrance with {doors}"
    living_room = "open-plan living room at the front facing the main view"
    kitchen = "open-concept kitchen with central island connected to the dining area"

    rooms_list = [f"{bedrooms} Bedrooms", f"{bathrooms} Bathrooms", "Living Room", "Kitchen & Dining"]
    if has_courtyard: rooms_list.append("Central Open Courtyard")
    if "pooja" in p or "prayer" in p: rooms_list.append("Pooja / Prayer Room")
    if "office" in p or "study" in p: rooms_list.append("Home Office / Study Room")
    if has_porch: rooms_list.append("Covered Porch / Verandah")
    if has_balcony: rooms_list.append("Balcony / Terrace")

    spatial_layout = {
        "entrance": entrance,
        "staircase": staircase,
        "living_room": living_room,
        "kitchen": kitchen,
        "floors_count": floors,
        "ceiling_design": ceiling_design,
        "window_system": windows,
        "door_system": doors,
    }

    special_requirements: List[str] = []
    if has_pool: special_requirements.append("Swimming Pool")
    if has_garden: special_requirements.append("Landscaped Garden")
    if has_parking: special_requirements.append("Parking / Garage")
    if has_courtyard: special_requirements.append("Central Courtyard")
    if has_balcony: special_requirements.append("Balcony / Terrace")
    if env_tag in ["lake", "ocean", "island"]: special_requirements.append(f"{env_tag.capitalize()} View")

    # --------------------------------------------------------------------------
    # 11. ASSEMBLE IMMUTABLE MASTER SPECIFICATION
    # --------------------------------------------------------------------------
    return {
        "house_type": house_type,
        "architectural_style": style,
        "style_dna": dna,
        "floors": floors,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "plot_size_sqft": plot_size,
        "budget_usd": budget,
        "environment": environment,
        "env_tag": env_tag,
        "spatial_layout": spatial_layout,
        "exterior": {
            "primary_color": primary_color,
            "secondary_color": secondary_color,
            "colors": exterior_colors,
            "materials": exterior_materials,
            "windows": windows,
            "doors": doors,
            "roof": roof,
            "environment": environment,
            "balcony": has_balcony,
            "pool": has_pool,
            "garden": has_garden,
            "parking": has_parking,
            "courtyard": has_courtyard,
            "porch": has_porch,
        },
        "interior": {
            "style": style,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "flooring": flooring,
            "lighting": lighting,
            "ceiling": ceiling_design,
            "furniture": furniture,
            "materials": interior_materials,
            "walls_int": dna["walls_int"],
            "windows_int": windows,
        },
        "house": {
            "architectural_style": style,
            "floors": floors,
            "house_type": house_type,
        },
        "rooms": rooms_list,
        "special_requirements": special_requirements,
        "original_prompt": prompt,
    }
