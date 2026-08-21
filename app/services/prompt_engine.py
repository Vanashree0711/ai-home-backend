"""
Specialized Architectural Image Prompt Engine (Master Blueprint Driven - HD Enhanced)
=====================================================================================
Derives Exterior, Interior, and 3D Interior Floor Plan representations directly from
the immutable Master House Design Specification with Ultra-HD 8K photographic fidelity.

PRIMARY REFERENCE HOUSE (Locked Visual DNA):
════════════════════════════════════════════
EXTERIOR:
  - Single-storey, wide low-profile symmetrical building volume
  - Smooth bright white stucco/render facade — no texture, no pattern
  - Dark charcoal standing-seam metal roof (flat-pitched, barely visible above parapet)
  - 3 identical large black-framed multi-pane casement window bays flanking a centered dark entry door
  - Centered dark charcoal pivot front door with full-height vertical glass sidelights
  - Low concrete step leading to covered entry porch (shallow canopy overhang)
  - Single potted plant beside front door
  - Manicured lawn with tall mature trees behind the building

FLOOR PLAN (Left-to-Right, Front-to-Rear):
  - Front: Entry porch → central open Living Room (sofa, armchair, TV wall, coffee table)
  - Centre: Open Dining (round/oval table + chairs) connected to Kitchen
  - Left wing: Kitchen with island counter + rear Terrace deck
  - Left rear: Master Bedroom (king bed, walk-in wardrobe/closet)
  - Right wing: Bedroom 2 (with en-suite bath/WC) + Bedroom 3
  - Shared Bathroom between Bedrooms 2 and 3
  - Laundry/utility room at the right rear
  - All rooms open plan or connected via wide doorways

INTERIOR:
  - Bright white smooth matte walls throughout
  - Light blonde/natural oak wide-plank hardwood flooring in all rooms
  - Floor-to-ceiling full-width black-framed glass window wall on left side of living room
  - View through windows: tall pine/birch trees and water/lake in distance
  - Furniture: light grey linen sofa with olive/sage throw blanket, rectangular wooden coffee table,
    sheepskin rug, natural wicker wishbone chair, small round side table
  - Open dining area behind sofa: round wooden table + bentwood chairs
  - Tall fiddle leaf fig (Ficus lyrata) plant in terracotta pot beside windows
  - Multiple green potted houseplants along window sill
  - Wooden open bookshelf/sideboard along rear wall
  - Framed art print above bookshelf
  - Pendant lamp over dining table (dome/arc style)
  - Soft abundant natural daylight as primary lighting
"""

from typing import Dict, Any, List


# ══════════════════════════════════════════════════════════════════════════════
# LOCKED REFERENCE HOUSE VISUAL DNA
# Extracted from the 3 user-provided reference images.
# All 3 generated views MUST match this specification exactly.
# ══════════════════════════════════════════════════════════════════════════════
REFERENCE_HOUSE = {
    # Architecture
    "floors": 1,
    "floors_label": "single-storey",
    "style": "Minimalist Scandinavian",
    "house_type": "Scandinavian Minimalist Residence",

    # Exterior
    "facade_color": "smooth bright white stucco render",
    "roof": "dark charcoal standing-seam metal roof with low flat pitch",
    "windows_ext": "three sets of large black-framed multi-pane casement windows with black metal trim",
    "door_ext": "centered dark charcoal full-height pivot front door with vertical glass sidelights",
    "entry": "shallow covered concrete entry porch with low step",
    "grounds": "manicured green lawn with mature tall evergreen trees behind",

    # Interior & Spatial
    "flooring": "light natural blonde oak wide-plank hardwood flooring",
    "walls_int": "smooth bright white matte interior walls",
    "windows_int": "floor-to-ceiling full-width black-framed glass window wall on the left side of the living room",
    "window_view": "tall green pine and birch trees with a glimmering lake/water visible in the distance",
    "furniture": (
        "light grey linen sofa with an olive throw blanket, "
        "rectangular solid oak coffee table with a candle, "
        "sheepskin rug beneath the coffee table, "
        "natural rattan wicker wishbone chair, "
        "round wooden side table"
    ),
    "plants": (
        "tall fiddle leaf fig tree (Ficus lyrata) in a terracotta pot beside the windows, "
        "multiple small green houseplants arranged along the window sill"
    ),
    "dining": "open dining area behind the sofa with a round wooden dining table and bentwood chairs",
    "bookshelf": "wooden open sideboard / bookshelf along the rear wall with framed art print above",
    "lighting": (
        "abundant soft natural daylight streaming through the floor-to-ceiling glass wall, "
        "a minimalist dome pendant lamp over the dining table, "
        "warm ambient floor lamp in the corner"
    ),
    "ceiling": "smooth flat white ceiling",

    # Floor Plan
    "room_layout": (
        "central living room at the front with sofa and TV wall, "
        "open dining connected to an open-plan kitchen with island counter, "
        "rear outdoor terrace deck with dining furniture on the left, "
        "master bedroom suite on the left-rear with king bed and walk-in wardrobe, "
        "bedroom 2 on the right side with en-suite, "
        "bedroom 3 on the right side, "
        "shared bathroom between bedrooms 2 and 3, "
        "laundry room at the right rear"
    ),
    "bedrooms": 3,
    "bathrooms": 2,
    "plot_size": 2500,
}


def synthesize_design_identity(spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synthesizes the shared visual DNA for the house.
    Merges user prompt spec with REFERENCE_HOUSE defaults.
    The Reference House DNA takes precedence for visual consistency.
    """
    p = spec.get("original_prompt", "").lower()

    # Determine if this is a Scandinavian / Reference style house
    use_reference = any(kw in p for kw in [
        "scandinavian", "nordic", "scandi", "hygge", "minimalist",
        "white house", "oak floor", "oak flooring", "linen sofa", "black frame"
    ])

    # Extract style from spec
    style = spec.get("architectural_style", REFERENCE_HOUSE["style"])
    floors = spec.get("floors", REFERENCE_HOUSE["floors"])
    bedrooms = spec.get("bedrooms", REFERENCE_HOUSE["bedrooms"])
    bathrooms = spec.get("bathrooms", REFERENCE_HOUSE["bathrooms"])
    plot_size = spec.get("plot_size_sqft", REFERENCE_HOUSE["plot_size"])

    ext = spec.get("exterior", {})
    interior = spec.get("interior", {})
    spatial = spec.get("spatial_layout", {})

    # --------------------------------------------------------------------------
    # If Scandinavian / Minimalist → fully lock to Reference House DNA
    # --------------------------------------------------------------------------
    is_scandi = "scandi" in style.lower() or "nordic" in style.lower() or "minimalist" in style.lower()

    if is_scandi or use_reference:
        return {
            "style": REFERENCE_HOUSE["style"],
            "house_type": REFERENCE_HOUSE["house_type"],
            "floors": REFERENCE_HOUSE["floors"],
            "floors_label": REFERENCE_HOUSE["floors_label"],
            "environment": ext.get("environment", "private landscaped residential property"),
            "primary_color": "bright white",
            "secondary_color": "dark charcoal",
            "color_palette_str": "bright white, dark charcoal, light natural oak",
            "materials_str": REFERENCE_HOUSE["facade_color"],
            "wood_tone": "light natural blonde oak",
            "stone_type": "smooth white stucco",
            "windows": REFERENCE_HOUSE["windows_ext"],
            "doors": REFERENCE_HOUSE["door_ext"],
            "roof": REFERENCE_HOUSE["roof"],
            "entry": REFERENCE_HOUSE["entry"],
            "grounds": REFERENCE_HOUSE["grounds"],
            "flooring": REFERENCE_HOUSE["flooring"],
            "walls_int": REFERENCE_HOUSE["walls_int"],
            "windows_int": REFERENCE_HOUSE["windows_int"],
            "window_view": REFERENCE_HOUSE["window_view"],
            "furniture": REFERENCE_HOUSE["furniture"],
            "plants": REFERENCE_HOUSE["plants"],
            "dining": REFERENCE_HOUSE["dining"],
            "bookshelf": REFERENCE_HOUSE["bookshelf"],
            "lighting": REFERENCE_HOUSE["lighting"],
            "ceiling": REFERENCE_HOUSE["ceiling"],
            "room_layout": REFERENCE_HOUSE["room_layout"],
            "staircase": "",
            "is_scandi": True,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "plot_size": plot_size,
            "original_prompt": spec.get("original_prompt", ""),
            "features_str": REFERENCE_HOUSE["grounds"],
        }

    # --------------------------------------------------------------------------
    # Non-Scandinavian styles — derive from spec normally
    # --------------------------------------------------------------------------
    ext_colors = ext.get("colors", ["contemporary white", "natural stone"])
    primary_color = ext.get("primary_color") or (ext_colors[0] if ext_colors else "contemporary white")
    secondary_color = ext.get("secondary_color") or (ext_colors[1] if len(ext_colors) > 1 else "natural stone")
    materials = ext.get("materials", ["render", "stone", "glass"])
    materials_str = ", ".join(materials)

    # Wood tone
    if "dark wood" in p or "espresso" in p:
        wood_tone = "dark espresso stained wood"
    elif "walnut" in p:
        wood_tone = "natural walnut wood"
    elif "teak" in p:
        wood_tone = "handcrafted teak wood"
    elif "cedar" in p:
        wood_tone = "rich cedar timber"
    else:
        wood_tone = "natural warm wood"

    stone_type = "natural stone"
    for mat in materials:
        if "brick" in mat: stone_type = "exposed brick"
        elif "slate" in mat: stone_type = "dark slate"
        elif "granite" in mat: stone_type = "dark granite"
        elif "marble" in mat: stone_type = "polished marble"

    flooring = interior.get("flooring") or "large-format polished marble and hardwood"
    lighting = interior.get("lighting") or "warm 3000K architectural LED cove lighting"
    furniture = interior.get("furniture") or f"contemporary {style} designer furniture"
    staircase = spatial.get("staircase", "central architectural open staircase along the interior side wall")
    ceiling = spatial.get("ceiling_design", "smooth architectural ceiling with LED cove lighting")
    roof = ext.get("roof", "flat contemporary roof")
    windows = ext.get("windows", "large black-framed floor-to-ceiling glass windows")
    doors = ext.get("doors", "grand solid wooden entrance door")

    features_list = []
    if ext.get("pool"): features_list.append("rectangular swimming pool with wooden deck")
    if ext.get("garden"): features_list.append("landscaped garden with stone pathway")
    if ext.get("balcony"): features_list.append("glass railing balcony")
    if ext.get("parking"): features_list.append("two-car carport")
    features_str = ", ".join(features_list) if features_list else "landscaped grounds"

    return {
        "style": style,
        "house_type": spec.get("house_type", "Modern Residence"),
        "floors": floors,
        "floors_label": f"{floors}-storey" if floors > 1 else "single-storey",
        "environment": ext.get("environment", "residential grounds"),
        "primary_color": primary_color,
        "secondary_color": secondary_color,
        "color_palette_str": ", ".join(ext_colors),
        "materials_str": materials_str,
        "wood_tone": wood_tone,
        "stone_type": stone_type,
        "windows": windows,
        "doors": doors,
        "roof": roof,
        "entry": spatial.get("entrance", "front-center entrance"),
        "grounds": features_str,
        "flooring": flooring,
        "walls_int": "smooth painted interior walls",
        "windows_int": "large glass windows",
        "window_view": "outdoor greenery",
        "furniture": furniture,
        "plants": "indoor potted plants",
        "dining": "dining area with table and chairs",
        "bookshelf": "sideboard along the wall",
        "lighting": lighting,
        "ceiling": ceiling,
        "room_layout": "open-plan living, dining, kitchen, bedrooms, and bathrooms",
        "staircase": staircase if floors > 1 else "",
        "is_scandi": False,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "plot_size": plot_size,
        "features_str": features_str,
        "original_prompt": spec.get("original_prompt", ""),
    }


# ══════════════════════════════════════════════════════════════════════════════
# A. EXTERIOR VIEW
# ══════════════════════════════════════════════════════════════════════════════
def build_exterior_prompt(spec: Dict[str, Any]) -> str:
    """
    A. EXTERIOR VIEW (Ultra HD photorealistic):
    Full front-facing architectural photograph of the exact reference house exterior.
    """
    dna = synthesize_design_identity(spec)

    if dna["is_scandi"]:
        prompt = (
            "Ultra-HD photorealistic 8K architectural photograph of the EXTERIOR of a single-storey Minimalist Scandinavian residence. "
            "Perspective: full property symmetric front-facing eye-level view, building fully visible from foundation to roofline, centered in frame with generous margins, no cropping. "
            "Facade: wide low-profile symmetrical building form with smooth bright white stucco render walls, "
            "dark charcoal standing-seam metal roof with low flat pitch visible above white parapet, "
            "three identical large black-framed multi-pane casement windows symmetrically arranged on each side of the entrance, sheer white curtains visible inside, "
            "centered dark charcoal full-height pivot front door with vertical glass sidelights, "
            "low concrete steps leading to shallow covered entry porch, "
            "single potted plant beside front door. "
            "Site: manicured green lawn in foreground, tall mature evergreen pine trees behind the building, soft blue sky. "
            "Quality: Hasselblad H6D-100c medium format, sharp architectural focus, soft natural daylight, realistic shadows, photorealistic textures, 8K resolution. "
            "Negative: cropped building, aerial view, close-up, multiple storeys, cartoon, sketch, watermark, text, extra buildings, night shot, dark moody"
        )
    else:
        prompt = (
            f"Ultra-HD 8K architectural photograph of the exterior of a {dna['floors_label']} {dna['style']} {dna['house_type']}, {dna['plot_size']} sqft. "
            f"Perspective: full property wide three-quarter front view, complete building visible from ground to roof, centered in frame, generous margins, no cropping. "
            f"Facade: {dna['materials_str']}, {dna['windows']}, {dna['doors']}, {dna['roof']}. "
            f"Site: {dna['grounds']}, natural daylight. "
            f"Quality: Hasselblad H6D-100c medium format, sharp crisp focus, ultra-detailed architectural textures, photorealistic, 8K resolution. "
            f"Negative: low quality, blurry, cropped, cartoon, sketch, watermark, text"
        )

    return prompt


# ══════════════════════════════════════════════════════════════════════════════
# B. INTERIOR VIEW
# ══════════════════════════════════════════════════════════════════════════════
def build_interior_prompt(spec: Dict[str, Any]) -> str:
    """
    B. INTERIOR VIEW (Ultra HD photorealistic):
    Eye-level wide-angle photograph inside the exact living room of the reference house.
    """
    dna = synthesize_design_identity(spec)

    if dna["is_scandi"]:
        prompt = (
            "Ultra-HD 8K photorealistic interior photograph inside the main living room and open dining area of a single-storey Minimalist Scandinavian residence. "
            "Camera: wide-angle architectural interior photography, straight vertical walls, natural room proportions, eye-level perspective. "
            "Walls & Ceiling: smooth bright white matte walls throughout, smooth flat white ceiling. "
            "Flooring: light natural blonde oak wide-plank hardwood flooring running through the entire space. "
            "Windows: floor-to-ceiling full-width black-framed glass window wall running the full length of the left side wall, "
            "looking out to tall green pine and birch trees with a glimmering lake visible in the distance, soft natural daylight flooding the room. "
            "Furniture: light grey linen sofa with an olive throw blanket facing the room, "
            "rectangular solid oak wooden coffee table with a candle on top, "
            "sheepskin fluffy rug beneath the coffee table, "
            "natural rattan wicker wishbone chair beside the window, "
            "round small wooden side table. "
            "Plants: tall fiddle leaf fig tree in a terracotta pot beside the windows, "
            "multiple small green potted houseplants arranged along the window sill. "
            "Dining area: open dining area visible behind the sofa with a round wooden dining table and bentwood wooden chairs. "
            "Background: wooden open sideboard bookshelf along the rear wall with framed art print above. "
            "Lighting: abundant soft natural daylight as the primary source, warm ambient floor lamp in corner, minimalist dome pendant over dining table. "
            "Quality: Architectural Digest photography, sharp realistic focus, 8K resolution, photorealistic materials, no distortion. "
            "Negative: dark moody room, night shot, exterior of building, outdoor, close-up furniture only, fisheye lens distortion, low quality, blurry, pixelated, watermark, text"
        )
    else:
        staircase_clause = f", {dna['staircase']}" if dna["floors"] > 1 else ""
        prompt = (
            f"Ultra-HD 8K interior architectural photograph inside the main living room of a {dna['floors_label']} {dna['style']} {dna['house_type']}. "
            f"Spatial: {dna['walls_int']}, {dna['flooring']}{staircase_clause}. "
            f"Windows: {dna['windows_int']} with view of {dna['window_view']}. "
            f"Furniture: {dna['furniture']}. "
            f"Lighting: {dna['lighting']}. "
            f"Quality: Architectural Digest photography, 8K resolution, sharp photorealistic detail. "
            f"Negative: exterior, outdoor, watermark, text, low quality, blurry"
        )

    return prompt


# ══════════════════════════════════════════════════════════════════════════════
# C. 3D ISOMETRIC DOLLHOUSE FLOOR PLAN / CUTAWAY
# ══════════════════════════════════════════════════════════════════════════════
def build_3d_prompt(spec: Dict[str, Any]) -> str:
    """
    C. 3D ISOMETRIC DOLLHOUSE FLOOR PLAN (Ultra HD photorealistic):
    45-degree elevated isometric cutaway view with standing 3D walls,
    roof removed, all rooms furnished and labeled, warm golden wood flooring,
    outdoor greenery surrounding the building.
    Matches the "3D Isometric Dollhouse Floor Plan" architectural visualization style.
    """
    dna = synthesize_design_identity(spec)

    if dna["is_scandi"]:
        prompt = (
            "Ultra-HD 8K photorealistic 3D isometric dollhouse floor plan architectural visualization of a complete single-storey Minimalist Scandinavian home. "
            "Perspective: 45-degree elevated isometric bird's-eye angled view — NOT straight top-down, NOT eye-level — the classic dollhouse cutaway angle showing the interior rooms from above at a diagonal. "
            "Structure: roof completely removed so all interior rooms are visible, thick 3D standing white walls with visible depth and thickness at all edges, doorway openings cut through walls, window openings with black frames in exterior walls. "
            "Interior Room Layout with room name labels and dimension text: "
            "FRONT PORCH — covered entrance porch at the bottom front center; "
            "LIVING ROOM — central living room with grey sofa set, wooden coffee table, and sheepskin rug; "
            "KITCHEN/DINING — open kitchen with white cabinets and island counter connected to dining area with round wooden table and bentwood chairs; "
            "PRIMARY BEDROOM — master bedroom on the right rear with a king-size double bed, two nightstands, and an ensuite bathroom with glass shower; "
            "ENSUITE — modern ensuite bathroom with glass walk-in shower, toilet, and vanity sink; "
            "BEDROOM 2 — secondary bedroom with a double bed, nightstand, and built-in wardrobe; "
            "BEDROOM 3 — third bedroom with a single bed and desk; "
            "BATH — shared bathroom with bathtub/shower, toilet, and vanity sink; "
            "LAUNDRY/MUD — laundry room with washing machine and utility shelving at the rear. "
            "Flooring: warm golden honey-toned oak wood plank flooring with visible plank lines running throughout all living, dining, and bedroom areas. "
            "Lighting: warm golden afternoon sunlight streaming diagonally across the interior floor from the exterior windows, casting soft realistic shadows on the furniture and floors. "
            "Exterior surroundings: the building sits on a green grass lawn with trees and shrubs visible around the edges of the house. "
            "Style: photorealistic 3D architectural visualization with accurate furniture scale, crisp material textures, soft shadows, and professional render quality, 8K resolution. "
            "Negative: straight top-down 2D floor plan, eye-level interior photograph, exterior facade photograph, roof covering the rooms, ceiling blocking view, flat 2D blueprint, black and white CAD drawing, wireframe only, low quality, blurry, pixelated, watermark, text overlays"
        )
    else:
        staircase_clause = f"{dna['staircase']} visible between floors, " if dna["floors"] > 1 else ""
        floors_desc = f"all {dna['floors']} floors simultaneously shown in cross-section" if dna["floors"] > 1 else "the entire single floor"
        prompt = (
            f"Ultra-HD 8K photorealistic 3D isometric dollhouse floor plan architectural visualization of a complete {dna['floors_label']} {dna['style']} {dna['house_type']}, {dna['plot_size']} sqft. "
            f"Perspective: 45-degree elevated isometric angled dollhouse cutaway view — not straight top-down, not eye-level — showing {floors_desc} from an angled bird's-eye perspective. "
            f"Structure: roof completely removed, thick 3D standing walls with visible depth and thickness, doorway and window openings clearly cut through the walls. {staircase_clause}"
            f"Interior Layout with room labels: {dna['room_layout']}. "
            f"Flooring: {dna['flooring']} with visible plank lines throughout all living and bedroom areas, tiled surfaces in bathrooms and kitchen. "
            f"Lighting: warm golden sunlight streaming across the interior from exterior windows, casting soft directional shadows on furniture and floors, warm ambient indoor lighting. "
            f"Surroundings: green garden lawn and trees visible around the exterior walls of the building. "
            f"Quality: ultra-detailed photorealistic 3D architectural dollhouse visualization, accurate furniture scale, crisp material textures, 8K resolution. "
            f"Negative: straight top-down 2D floor plan, eye-level interior photograph, exterior facade photo, roof on, ceiling blocking rooms, flat 2D blueprint, wireframe, low quality, blurry, watermark, text"
        )

    return prompt



# ══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════
def generate_all_specialized_prompts(spec: Dict[str, Any]) -> Dict[str, str]:
    """
    Converts a single Master Design Specification into 3 synchronized specialized prompts.
    All 3 are derived from the same locked house DNA.
    """
    return {
        "exterior_prompt": build_exterior_prompt(spec),
        "interior_prompt": build_interior_prompt(spec),
        "floorplan_prompt": build_3d_prompt(spec)
    }
