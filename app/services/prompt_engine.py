"""
Intelligent Prompt Engine — AI Architect + 3D Visualizer v2
============================================================
Transforms the Master House Specification into 3 photorealistic HD prompts
that describe the EXACT SAME HOUSE from 3 different viewpoints.

Pipeline:
  MASTER SPECIFICATION → [EXTERIOR PROMPT + INTERIOR PROMPT + 3D DOLLHOUSE PROMPT]

Guarantees:
  - All 3 prompts share identical architecture, colors, materials, floors, and style
  - Environment (lake, ocean, mountain) appears in Exterior and Interior view
  - 3D Floor Plan shows all furnished rooms from 45° isometric dollhouse view
  - Style DNA drives every material, color, and atmosphere decision
"""

from typing import Dict, Any


def build_exterior_prompt(spec: Dict[str, Any]) -> str:
    """
    A. EXTERIOR VIEW — Full architectural photograph of the house outside.
    The building, its surroundings, and the environment must all be visible.
    """
    dna = spec.get("style_dna", {})
    ext = spec.get("exterior", {})
    style = spec.get("architectural_style", "Modern Luxury")
    floors_label = f"{spec['floors']}-storey" if spec["floors"] > 1 else "single-storey"
    house_type = spec.get("house_type", "Luxury Residence")
    environment = spec.get("environment", "landscaped residential grounds")
    primary = ext.get("primary_color", dna.get("facade_color", "warm white"))
    secondary = ext.get("secondary_color", dna.get("accent_color", "natural wood"))
    materials = ", ".join(ext.get("materials", dna.get("materials_ext", ["render", "glass"])))
    windows = ext.get("windows", dna.get("windows", "large glass windows"))
    doors = ext.get("doors", dna.get("door", "entrance door"))
    roof = ext.get("roof", dna.get("roof", "flat contemporary roof"))
    plot_size = spec.get("plot_size_sqft", 2500)
    atmosphere = dna.get("atmosphere", "premium residential")
    landscape = dna.get("landscape", "manicured grounds")
    env_tag = spec.get("env_tag", "suburban")

    # Build feature list
    features = []
    if ext.get("pool"): features.append("a sparkling rectangular swimming pool with timber deck")
    if ext.get("garden") or env_tag == "suburban": features.append(landscape)
    if ext.get("balcony"): features.append("upper-level glass-railed balcony")
    if ext.get("parking"): features.append("double covered carport or garage")
    if ext.get("courtyard"): features.append("central open-air courtyard")
    if ext.get("porch"): features.append("covered entrance verandah")
    features_str = ", ".join(features) if features else landscape

    # Environment clause — must appear beside/around the house
    env_clause = f"The house is situated on {environment}."

    prompt = (
        f"Ultra-HD 8K photorealistic professional architectural exterior photograph of a {floors_label} {style} {house_type}, {plot_size} sqft. "
        f"Perspective: full-property symmetric front or three-quarter view from ground level, complete building visible from foundation to roofline, generous sky above and grounds below, never cropped. "
        f"Architecture: {primary} facade with {secondary} accents, {materials}, {windows}, {doors}, {roof}. "
        f"{env_clause} "
        f"Grounds and landscape: {features_str}. "
        f"Atmosphere: {atmosphere}, soft natural daylight with realistic shadows and reflections. "
        f"Quality: Hasselblad H6D-100c medium format camera, sharp crisp focus, 8K resolution, photorealistic textures and materials, architectural photography. "
        f"Negative: cropped building, aerial drone view, close-up detail only, interior visible, multiple buildings, cartoon, sketch, watermark, text, blurry, low quality"
    )
    return prompt


def build_interior_prompt(spec: Dict[str, Any]) -> str:
    """
    B. INTERIOR VIEW — Eye-level photograph inside the main living space of this exact house.
    Must reflect the same materials, colors, architecture, and environment as the exterior.
    """
    dna = spec.get("style_dna", {})
    interior = spec.get("interior", {})
    ext = spec.get("exterior", {})
    style = spec.get("architectural_style", "Modern Luxury")
    floors_label = f"{spec['floors']}-storey" if spec["floors"] > 1 else "single-storey"
    house_type = spec.get("house_type", "Luxury Residence")
    environment = spec.get("environment", "landscaped grounds")
    env_tag = spec.get("env_tag", "suburban")

    flooring = interior.get("flooring", dna.get("flooring", "natural hardwood"))
    walls_int = interior.get("walls_int", dna.get("walls_int", "smooth painted walls"))
    ceiling = interior.get("ceiling", dna.get("ceiling", "smooth ceiling"))
    furniture = interior.get("furniture", dna.get("furniture", "contemporary designer furniture"))
    lighting = interior.get("lighting", dna.get("lighting", "warm natural daylight"))
    windows_int = interior.get("windows_int", dna.get("windows", "large glass windows"))
    materials_int = ", ".join(interior.get("materials", dna.get("materials_int", ["natural materials"])))
    atmosphere = dna.get("atmosphere", "premium residential")
    floors = spec.get("floors", 2)

    # Staircase clause for multi-storey homes
    staircase_clause = ""
    spatial = spec.get("spatial_layout", {})
    if floors > 1:
        staircase_clause = f", with {spatial.get('staircase', 'an open floating staircase')} visible in the background"

    # Environment view through windows — MUST match the exterior environment
    env_view_map = {
        "lake": "a serene reflective lake with forested shores visible through the windows",
        "ocean": "the blue ocean and sandy beach directly outside the floor-to-ceiling glass",
        "island": "turquoise ocean water and tropical palm trees visible through the windows",
        "mountain": "dramatic mountain peaks and pine valley visible through the panoramic windows",
        "forest": "tall pine and birch trees in a forest directly outside the glass wall",
        "desert": "vast red sand dunes and clear sky visible through the windows",
        "urban": "the glittering city skyline visible through the floor-to-ceiling glass",
        "suburban": "a manicured garden and greenery visible through the windows",
    }
    window_view = env_view_map.get(env_tag, "outdoor greenery visible through the windows")

    prompt = (
        f"Ultra-HD 8K photorealistic interior architectural photograph inside the main living room and open dining area of the SAME {floors_label} {style} {house_type}. "
        f"Camera: wide-angle interior photography at eye level, straight vertical walls, accurate room proportions, no fisheye distortion. "
        f"Architecture: {walls_int}, {ceiling}{staircase_clause}. "
        f"Flooring: {flooring} running throughout the entire space. "
        f"Windows: {windows_int} — through which {window_view}. "
        f"Furniture & Decor: {furniture}, with {materials_int} finishes throughout. "
        f"Lighting: {lighting}, soft realistic shadows, warm and inviting atmosphere. "
        f"Atmosphere: {atmosphere}, Architectural Digest photography quality. "
        f"Quality: 8K resolution, sharp photorealistic focus, accurate material textures, realistic natural lighting. "
        f"Negative: exterior facade view, outdoor scene only, mismatched architecture, dark cave-like room, generic hotel lobby, fisheye distortion, cartoon, sketch, watermark, text, blurry, low quality"
    )
    return prompt


def build_3d_prompt(spec: Dict[str, Any]) -> str:
    """
    C. 3D ISOMETRIC DOLLHOUSE FLOOR PLAN — 45-degree angled cutaway view showing ALL rooms.
    Roof removed. Standing 3D walls visible. All rooms furnished simultaneously.
    Must match the same house layout as the Exterior and Interior views.
    """
    dna = spec.get("style_dna", {})
    interior = spec.get("interior", {})
    style = spec.get("architectural_style", "Modern Luxury")
    floors_label = f"{spec['floors']}-storey" if spec["floors"] > 1 else "single-storey"
    house_type = spec.get("house_type", "Luxury Residence")
    floors = spec.get("floors", 2)
    bedrooms = spec.get("bedrooms", 3)
    bathrooms = spec.get("bathrooms", 2)
    plot_size = spec.get("plot_size_sqft", 2500)
    flooring = interior.get("flooring", dna.get("flooring", "warm hardwood flooring"))
    furniture = interior.get("furniture", dna.get("furniture", "designer furniture"))
    environment = spec.get("environment", "landscaped grounds")
    ext = spec.get("exterior", {})

    spatial = spec.get("spatial_layout", {})
    staircase_clause = (
        f"{spatial.get('staircase', 'a central open floating staircase connecting the floors')} visible between the floors, "
        if floors > 1 else ""
    )

    # Secondary bedrooms description
    sec_beds = bedrooms - 1
    sec_bed_str = f"{sec_beds} secondary bedroom{'s' if sec_beds > 1 else ''} each with {'beds and wardrobes' if sec_beds > 1 else 'a bed and wardrobe'}"

    # Extra rooms
    extra_rooms = []
    rooms_list = spec.get("rooms", [])
    for room in rooms_list:
        if "Pooja" in room: extra_rooms.append("a small pooja/prayer room")
        if "Office" in room or "Study" in room: extra_rooms.append("a home office with desk and shelving")
        if "Courtyard" in room: extra_rooms.append("a central open-air courtyard with a water feature")
    extra_str = ", ".join(extra_rooms) + ", " if extra_rooms else ""

    # Landscape around the dollhouse
    landscape_str = f"The house sits on {environment} visible around the exterior walls."

    prompt = (
        f"Ultra-HD 8K photorealistic 3D isometric dollhouse floor plan architectural visualization of a complete {floors_label} {style} {house_type}, {plot_size} sqft. "
        f"Perspective: 45-degree elevated isometric angled bird's-eye view — NOT straight top-down, NOT eye-level — the classic architectural dollhouse cutaway angle looking diagonally into the interior. "
        f"Structure: roof completely removed so all interior rooms are fully visible, thick 3D standing walls with visible depth and thickness at edges, doorway openings and window cutouts clearly cut through the walls. "
        f"{staircase_clause}"
        f"Room Layout with labels: "
        f"ENTRY PORCH — covered entrance at the front center; "
        f"LIVING ROOM — main living space with {furniture}, wooden coffee table, and area rug; "
        f"DINING AREA — open dining with a dining table and chairs; "
        f"KITCHEN — open kitchen with island counter, cabinetry, and appliances; "
        f"MASTER BEDROOM — with a king-size bed, two nightstands, walk-in wardrobe, and en-suite bathroom; "
        f"{sec_bed_str}; "
        f"{bathrooms} modern bathroom{'s' if bathrooms > 1 else ''} with glass shower, vanity sink, and toilet; "
        f"{extra_str}"
        f"Rear terrace/deck with outdoor seating if applicable. "
        f"Interior Finishes: {flooring} across all living and bedroom areas, tiled surfaces in kitchen and bathrooms, bright white interior walls. "
        f"Lighting: warm golden sunlight streaming diagonally through windows casting soft realistic shadows across the interior floors and furniture. "
        f"Surroundings: {landscape_str} Green grass and trees visible around the exterior of the building. "
        f"Quality: ultra-detailed photorealistic 3D architectural dollhouse visualization, accurate furniture scale, crisp material textures, 8K resolution. "
        f"Negative: straight top-down 2D blueprint view, eye-level interior photo, exterior facade photo only, roof covering the interior, ceiling blocking rooms, flat black-and-white CAD drawing, wireframe, low quality, blurry, pixelated, watermark, text"
    )
    return prompt


def generate_all_specialized_prompts(spec: Dict[str, Any]) -> Dict[str, str]:
    """
    Main Entry Point — Converts one Master Specification into 3 synchronized HD prompts.
    All 3 describe the SAME house from different viewpoints.
    """
    return {
        "exterior_prompt": build_exterior_prompt(spec),
        "interior_prompt": build_interior_prompt(spec),
        "floorplan_prompt": build_3d_prompt(spec),
    }


def synthesize_design_identity(spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compatibility shim — returns a flat identity dict for the consistency validator.
    """
    dna = spec.get("style_dna", {})
    ext = spec.get("exterior", {})
    interior = spec.get("interior", {})
    spatial = spec.get("spatial_layout", {})
    floors = spec.get("floors", 2)

    return {
        "style": spec.get("architectural_style", "Modern Luxury"),
        "house_type": spec.get("house_type", "Luxury Residence"),
        "floors": floors,
        "floors_label": f"{floors}-storey" if floors > 1 else "single-storey",
        "environment": spec.get("environment", "landscaped grounds"),
        "primary_color": ext.get("primary_color", dna.get("facade_color", "warm white")),
        "secondary_color": ext.get("secondary_color", dna.get("accent_color", "natural wood")),
        "color_palette_str": ", ".join(ext.get("colors", [])),
        "materials_str": ", ".join(ext.get("materials", [])),
        "wood_tone": dna.get("wood_tone", "natural wood"),
        "stone_type": "natural stone",
        "windows": ext.get("windows", dna.get("windows", "large glass windows")),
        "doors": ext.get("doors", dna.get("door", "entrance door")),
        "roof": ext.get("roof", dna.get("roof", "flat roof")),
        "entry": spatial.get("entrance", "front entrance"),
        "grounds": dna.get("landscape", "manicured grounds"),
        "flooring": interior.get("flooring", dna.get("flooring", "natural hardwood")),
        "walls_int": interior.get("walls_int", dna.get("walls_int", "white walls")),
        "windows_int": interior.get("windows_int", dna.get("windows", "large windows")),
        "window_view": spec.get("environment", "garden view"),
        "furniture": interior.get("furniture", dna.get("furniture", "designer furniture")),
        "plants": "indoor potted plants",
        "dining": "open dining area with table and chairs",
        "bookshelf": "sideboard along the wall",
        "lighting": interior.get("lighting", dna.get("lighting", "warm ambient lighting")),
        "ceiling": interior.get("ceiling", dna.get("ceiling", "smooth ceiling")),
        "room_layout": "open-plan living, dining, kitchen, bedrooms, bathrooms",
        "staircase": spatial.get("staircase", "central staircase") if floors > 1 else "",
        "is_scandi": "scandi" in spec.get("architectural_style", "").lower() or "nordic" in spec.get("architectural_style", "").lower(),
        "bedrooms": spec.get("bedrooms", 3),
        "bathrooms": spec.get("bathrooms", 2),
        "plot_size": spec.get("plot_size_sqft", 2500),
        "features_str": dna.get("landscape", "landscaped grounds"),
        "original_prompt": spec.get("original_prompt", ""),
    }
