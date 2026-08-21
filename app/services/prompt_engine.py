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
  - 3D Floor Plan shows all furnished rooms from top-down architectural cutaway view matching the user reference
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
    C. 3D ARCHITECTURAL FLOOR PLAN CUTAWAY — Top-down 3D bird's-eye layout view showing ALL rooms.
    Roof removed. Dark standing exterior walls visible. Warm wood flooring & ambient indoor lights.
    Matches the exact layout style in user's uploaded reference picture.
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
    flooring = interior.get("flooring", dna.get("flooring", "warm light oak wood plank flooring"))
    furniture = interior.get("furniture", dna.get("furniture", "designer furniture"))

    spatial = spec.get("spatial_layout", {})
    staircase_clause = (
        f"{spatial.get('staircase', 'a central wooden staircase')} connecting levels, "
        if floors > 1 else ""
    )

    sec_beds = bedrooms - 1
    sec_bed_str = f"{sec_beds} secondary furnished bedrooms with double beds and nightstands"

    prompt = (
        f"Ultra-HD 8K photorealistic 3D architectural floor plan cutaway render of a complete {floors_label} {style} {house_type}, {plot_size} sqft layout. "
        f"Perspective: top-down 90-degree bird's-eye architectural cutaway view looking straight down inside all furnished rooms with the roof completely removed. "
        f"Perimeter & Walls: dark charcoal thick exterior boundary walls enclosing the square house layout, clean white interior room partition walls with doorway openings. "
        f"Room Layout: "
        f"central spacious living room with plush sofa set, coffee table, and television wall; "
        f"open dining area with wooden table; "
        f"modern kitchen with island counter and cabinets; "
        f"master bedroom suite with king bed and nightstands; "
        f"{sec_bed_str}; "
        f"{bathrooms} modern tiled bathrooms with vanity sink, glass shower, and toilet; {staircase_clause}"
        f"Flooring & Lighting: {flooring} running throughout all living and bedroom spaces, warm cozy interior ambient lighting casting soft golden glows and directional shadows across the wood floors. "
        f"Surroundings: lush green trees and foliage framing the dark exterior perimeter walls. "
        f"Quality: professional 3D architectural rendering, crisp realistic textures, soft ambient occlusion shadows, 8K resolution. "
        f"Negative: eye-level view, facade photo, roof covering rooms, ceiling blocking view, flat 2D blueprint lines, wireframe, low quality, blurry, watermark, text"
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
