"""
Specialized Architectural Image Prompt Engine (Master Blueprint Driven - HD Enhanced)
=====================================================================================
Derives Exterior, Interior, and 3D Interior Floor Plan representations directly from
the immutable Master House Design Specification with Ultra-HD 8K photographic fidelity.

Guarantees:
1. Exterior View = Professional architectural photograph of the house exterior.
2. Interior View = Eye-level interior photograph inside the main living room.
3. 3D Interior Plan = Top-down 3D photorealistic interior cutaway showing ONLY the inside furnished rooms.
"""

from typing import Dict, Any, List


def synthesize_design_identity(spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synthesizes the shared visual DNA that binds Exterior, Interior, and 3D views.
    Ensures that colors, materials, wood tones, window trims, and styles are identical across all views.
    """
    ext = spec.get("exterior", {})
    interior = spec.get("interior", {})
    house = spec.get("house", {})
    spatial = spec.get("spatial_layout", {})
    p = spec.get("original_prompt", "").lower()

    style = spec.get("architectural_style") or house.get("architectural_style", "Minimalist Scandinavian")
    floors = spec.get("floors") or house.get("floors", 1 if ("single" in p or "bungalow" in p) else 2)
    house_type = spec.get("house_type") or house.get("house_type", "Scandinavian Minimalist Home" if "scandi" in style.lower() else "Luxury Residence")
    environment = spec.get("environment") or ext.get("environment", "landscaped residential grounds")

    # Colors
    ext_colors = ext.get("colors", ["clean bright white", "light natural oak"])
    primary_color = ext.get("primary_color") or (ext_colors[0] if ext_colors else "clean bright white")
    secondary_color = ext.get("secondary_color") or (ext_colors[1] if len(ext_colors) > 1 else "light natural oak")
    color_palette_str = ", ".join(ext_colors)

    # Materials
    materials = ext.get("materials", ["smooth white vertical siding", "blonde oak timber", "clear glass"])
    materials_str = ", ".join(materials)

    is_scandi = "scandi" in style.lower() or "nordic" in style.lower()

    if is_scandi:
        wood_tone = "blonde natural oak timber"
        stone_type = "clean white architectural trim"
        flooring = "light blonde oak wide-plank hardwood flooring"
        lighting = "abundant natural daylight through panoramic windows, minimalist dome pendant light, and warm ambient floor lamps"
        furniture = "light grey linen sofa with throw blankets, blonde oak coffee table, wishbone dining chairs, and oak dining table"
        doors = "modern dark charcoal entry door with glass vertical panels"
        windows = "large black-framed multi-pane floor-to-ceiling glass windows"
        roof = "dark charcoal metal standing-seam roof"
    else:
        # Wood Tone parsing
        if "dark wood" in p or "dark wooden" in p or "dark espresso" in p:
            wood_tone = "dark espresso stained wood accents"
        elif "walnut" in p:
            wood_tone = "natural walnut wood accents"
        elif "teak" in p:
            wood_tone = "handcrafted teak wood"
        elif "cedar" in p:
            wood_tone = "rich cedar timber"
        elif "oak" in p or "blonde" in p:
            wood_tone = "blonde natural light oak timber"
        else:
            wood_tone = "natural warm wood accents"

        stone_type = "natural stone cladding"
        for mat in materials:
            if "brick" in mat: stone_type = "exposed brickwork"
            elif "slate" in mat: stone_type = "dark grey slate stone"
            elif "travertine" in mat: stone_type = "warm travertine stone"
            elif "granite" in mat: stone_type = "dark charcoal stone"
            elif "marble" in mat: stone_type = "polished marble"
            elif "grey" in mat or "gray" in mat or "dark" in mat: stone_type = "dark grey natural stone"

        windows = ext.get("windows", "large black-framed floor-to-ceiling glass windows")
        doors = ext.get("doors", "grand solid wooden entrance door")
        flooring = interior.get("flooring") or "large-format polished Italian marble and hardwood"
        lighting = interior.get("lighting") or "warm indirect 3000K architectural LED lighting"
        furniture = interior.get("furniture") or f"contemporary {style} designer furniture"
        roof = ext.get("roof", "flat contemporary roof")

    ceiling = spatial.get("ceiling_design", "smooth architectural ceiling with concealed warm 3000K LED cove lighting")
    staircase = spatial.get("staircase", "central architectural open staircase along the interior side wall connecting levels")
    entrance = spatial.get("entrance", "front-center covered entry porch with dark door")

    # Landscape & Features
    features_list = []
    if ext.get("pool"): features_list.append("rectangular swimming pool with wooden sun deck")
    if ext.get("garden"): features_list.append("landscaped garden with green lawn, front steps, and evergreen trees")
    if ext.get("balcony"): features_list.append("upper-level glass railing balcony")
    if ext.get("parking"): features_list.append("two-car covered parking carport")
    if ext.get("courtyard"): features_list.append("central open-air courtyard")
    if ext.get("porch"): features_list.append("covered entrance veranda")
    features_str = ", ".join(features_list) if features_list else "landscaped outdoor grounds with green lawn"

    return {
        "style": style,
        "house_type": house_type,
        "floors": floors,
        "floors_label": f"{floors}-storey" if floors > 1 else "single-storey",
        "environment": environment,
        "primary_color": primary_color,
        "secondary_color": secondary_color,
        "color_palette_str": color_palette_str,
        "materials_str": materials_str,
        "wood_tone": wood_tone,
        "stone_type": stone_type,
        "windows": windows,
        "doors": doors,
        "roof": roof,
        "flooring": flooring,
        "lighting": lighting,
        "ceiling": ceiling,
        "staircase": staircase,
        "entrance": entrance,
        "furniture": furniture,
        "features_str": features_str,
        "is_scandi": is_scandi,
        "has_pool": ext.get("pool", False),
        "has_garden": ext.get("garden", False),
        "has_balcony": ext.get("balcony", False),
        "has_parking": ext.get("parking", False),
        "has_courtyard": ext.get("courtyard", False),
        "bedrooms": spec.get("bedrooms", 3),
        "bathrooms": spec.get("bathrooms", 2),
        "plot_size": spec.get("plot_size_sqft", 2500),
        "budget": spec.get("budget_usd", 150000),
        "original_prompt": spec.get("original_prompt", "")
    }


def build_exterior_prompt(spec: Dict[str, Any]) -> str:
    """
    A. EXTERIOR VIEW (Ultra HD 8K):
    Front symmetrical architectural perspective of the exact house.
    White vertical panel facade, black-framed multi-pane windows, dark charcoal roof, covered entry porch.
    """
    id_dna = synthesize_design_identity(spec)

    prompt = (
        f"Ultra-HD 8k architectural photograph of the exterior of a {id_dna['floors_label']} {id_dna['style']} {id_dna['house_type']}, {id_dna['plot_size']} sqft. "
        f"Perspective: full property eye-level front perspective from a distance with generous margins on all sides, complete building centered in frame from ground to roof, manicured lawn with low shrubbery in foreground, lush green trees in background, open sky above, never cropped, no close-ups. "
        f"Facade Architecture: symmetrical bright white facade with clean vertical paneling, {id_dna['windows']} with black frames and sheer interior drapes, covered central entry porch with concrete steps and {id_dna['doors']}, {id_dna['roof']}. "
        f"Site & Grounds: {id_dna['features_str']}, situated on {id_dna['environment']}. "
        f"Quality standard: Hasselblad H6D-100c medium format, sharp crisp focus, ultra-detailed architectural textures, realistic soft daylight shadows, 8k resolution. "
        f"Negative: low quality, blurry, pixelated, jpeg artifacts, compression noise, close-up, cropped house, tight shot, cut off edges, cartoon, sketch, painting, fantasy building, distorted architecture, extra floors, text, watermark"
    )
    return prompt


def build_interior_prompt(spec: Dict[str, Any]) -> str:
    """
    B. INTERIOR VIEW (Ultra HD 8K):
    Staged in the main living and dining room of the SAME house, looking through large floor-to-ceiling windows.
    """
    id_dna = synthesize_design_identity(spec)

    staircase_clause = f", featuring {id_dna['staircase']}" if id_dna['floors'] > 1 else ""

    prompt = (
        f"Ultra-HD 8k interior architectural photograph inside the main living room and open dining area of the SAME {id_dna['floors_label']} {id_dna['style']} residence. "
        f"Camera: wide-angle interior architectural photography, straight vertical lines, realistic room scale and proportions. "
        f"Spatial Architecture: clean white interior walls, floor-to-ceiling glass wall on the left with black window frames looking out to lush green pine trees, {id_dna['flooring']}{staircase_clause}. "
        f"Furnishing: {id_dna['furniture']}, potted fiddle leaf fig tree and houseplants on window sill, sheepskin rug, light wood bookshelf in background. "
        f"Lighting & Ambiance: {id_dna['lighting']}, soft bright natural daylight flooding the space, warm and airy Scandinavian aesthetic, 8k resolution, Architectural Digest photography. "
        f"Negative: dark moody cave, low quality, blurry, pixelated, compression artifacts, cartoon, sketch, mismatched architecture, rustic wooden log cabin, generic hotel lobby, distorted furniture, fisheye distortion, text, watermark"
    )
    return prompt


def build_3d_prompt(spec: Dict[str, Any]) -> str:
    """
    C. 3D INTERIOR FLOOR PLAN / CUTAWAY (Ultra HD 8K):
    Photorealistic 3D interior floor cutaway looking STRICTLY inside the furnished rooms from above with NO ROOF.
    Shows the interior rooms, furniture, beds, sofas, kitchen island, dining table, and bathrooms.
    """
    id_dna = synthesize_design_identity(spec)

    staircase_spatial = f"and {id_dna['staircase']}, " if id_dna['floors'] > 1 else ""

    prompt = (
        f"Ultra-HD 8k photorealistic 3D interior cutaway floor plan of the SAME {id_dna['floors_label']} {id_dna['style']} residence interior layout, {id_dna['plot_size']} sqft. "
        f"Perspective: top-down elevated isometric view looking directly inside the furnished interior rooms with roof completely removed, no ceiling. "
        f"Interior Room Arrangement: central living room with sofa set and wooden coffee table, open dining area with wooden dining table and chairs, open kitchen with marble countertop and island counter, "
        f"master bedroom with double bed and nightstands, {id_dna['bedrooms'] - 1} secondary bedrooms with made beds, and {id_dna['bathrooms']} modern bathrooms with glass shower, toilet, and vanity sink. {staircase_spatial}"
        f"Interior Materials & Finishes: {id_dna['flooring']} across all living and bedroom areas, clean white interior partition walls with doorway openings, and indoor potted plants. "
        f"Lighting & Rendering: warm soft indoor lighting and natural daylight illuminating the room interiors from above, ultra-detailed 3D architectural interior visualization, 8k resolution. "
        f"Negative: exterior building, outside facade of house, roof present, ceiling on, outdoor yard, sky, street, low quality, blurry, pixelated, 2D black and white blueprint, wireframe, text, watermark"
    )
    return prompt


def generate_all_specialized_prompts(spec: Dict[str, Any]) -> Dict[str, str]:
    """
    Main entry point for Specialized Prompt Engine.
    Converts a single Master Design Specification into 3 synchronized specialized prompts.
    """
    return {
        "exterior_prompt": build_exterior_prompt(spec),
        "interior_prompt": build_interior_prompt(spec),
        "floorplan_prompt": build_3d_prompt(spec)
    }
