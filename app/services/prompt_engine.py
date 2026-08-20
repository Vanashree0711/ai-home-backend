"""
Specialized Architectural Image Prompt Engine (Stage 2)
======================================================
Transforms a Master Design Specification into synchronized, specialized prompts
for Exterior, Interior, and 3D Architectural Visualizations.

Enforces cross-image visual consistency via a centralized Design Identity (DNA).
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

    style = spec.get("architectural_style") or house.get("architectural_style", "Modern Luxury")
    floors = spec.get("floors") or house.get("floors", 2)
    house_type = spec.get("house_type") or house.get("house_type", "Luxury Residence")

    # Colors
    ext_colors = ext.get("colors", ["warm white", "natural wood"])
    primary_color = ext.get("primary_color") or (ext_colors[0] if ext_colors else "warm white")
    secondary_color = ext.get("secondary_color") or (ext_colors[1] if len(ext_colors) > 1 else "natural wood")
    color_palette_str = ", ".join(ext_colors)

    # Materials
    materials = ext.get("materials", ["smooth concrete", "natural timber", "clear glass"])
    materials_str = ", ".join(materials)

    # Wood & Stone specific identification
    wood_tone = "natural walnut timber"
    for mat in materials + ext_colors:
        if "oak" in mat: wood_tone = "natural light oak timber"
        elif "teak" in mat: wood_tone = "handcrafted teak wood"
        elif "cedar" in mat: wood_tone = "rich cedar timber"
        elif "walnut" in mat: wood_tone = "natural walnut wood"

    stone_type = "natural stone cladding"
    for mat in materials:
        if "brick" in mat: stone_type = "exposed brickwork"
        elif "slate" in mat: stone_type = "dark slate stone"
        elif "travertine" in mat: stone_type = "warm travertine stone"
        elif "granite" in mat: stone_type = "charcoal granite"
        elif "marble" in mat: stone_type = "polished marble"

    windows = ext.get("windows", "large black-framed floor-to-ceiling glass windows")
    roof = ext.get("roof", "flat contemporary roof")
    doors = ext.get("doors", "grand pivot wooden entrance door")
    flooring = interior.get("flooring", "large-format porcelain tiles and hardwood")
    lighting = interior.get("lighting", "warm indirect 3000K architectural lighting")
    furniture = interior.get("furniture", f"contemporary {style} designer furniture")

    # Landscape & Features
    features_list = []
    if ext.get("pool"): features_list.append("crystal-clear swimming pool")
    if ext.get("garden"): features_list.append("landscaped garden with manicured lawn")
    if ext.get("balcony"): features_list.append("upper-level glass balcony")
    if ext.get("parking"): features_list.append("covered parking carport")
    if ext.get("courtyard"): features_list.append("central open-air courtyard")
    if ext.get("porch"): features_list.append("covered entrance verandah")
    features_str = ", ".join(features_list) if features_list else "landscaped outdoor grounds"

    return {
        "style": style,
        "house_type": house_type,
        "floors": floors,
        "floors_label": f"{floors}-storey" if floors > 1 else "single-storey",
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
        "furniture": furniture,
        "features_str": features_str,
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
    Builds a specialized exterior architectural prompt derived directly from the Master Design Specification.
    Strictly preserves floors, facade palette, materials, roof, and landscape amenities.
    """
    id_dna = synthesize_design_identity(spec)

    prompt = (
        f"A masterwork photorealistic architectural photograph of a {id_dna['floors_label']} {id_dna['style']} {id_dna['house_type']}, {id_dna['plot_size']} sqft. "
        f"Facade design: finished in {id_dna['primary_color']} with {id_dna['wood_tone']} and {id_dna['stone_type']}. "
        f"Architecture details: exact {id_dna['floors_label']} structure, {id_dna['windows']}, {id_dna['doors']}, {id_dna['roof']}. "
        f"Outdoor grounds: {id_dna['features_str']}. "
        f"Requirements: {id_dna['original_prompt']}. "
        f"Visual standard: front elevation eye-level architectural photography, warm natural daylight with realistic soft shadows, crisp clear glass reflections, "
        f"8k resolution, clean geometry, architectural magazine cover, highly detailed photorealistic render. "
        f"Negative: distorted building, extra floors, missing floors, duplicate doors, floating objects, low resolution, blurry, text, watermark, cartoon, sketch"
    )
    return prompt


def build_interior_prompt(spec: Dict[str, Any]) -> str:
    """
    Builds a specialized interior architectural prompt that inherits the EXACT design identity
    (colors, wood tones, stone accents, window trims, lighting language) from the Master Design Specification.
    """
    id_dna = synthesize_design_identity(spec)

    prompt = (
        f"A masterwork photorealistic interior architectural photograph of the expansive main living room inside the SAME {id_dna['floors_label']} {id_dna['style']} residence. "
        f"Synchronized architectural identity: interior walls in {id_dna['primary_color']}, custom millwork and wall paneling in {id_dna['wood_tone']}, {id_dna['stone_type']} accent wall. "
        f"Finishes: {id_dna['flooring']}, {id_dna['windows']} matching exterior facade, {id_dna['lighting']}. "
        f"Furnishing: {id_dna['furniture']}, matching neutral and {id_dna['secondary_color']} color accents. "
        f"Requirements: {id_dna['original_prompt']}. "
        f"Visual standard: wide-angle interior architectural photography, realistic room scale, soft ambient natural daylight streaming through windows, "
        f"8k resolution, photorealistic textures, crisp sharp details, Architectural Digest featured. "
        f"Negative: mismatched architectural style, rustic wooden cabin, generic hotel lobby, empty room, distorted furniture, low quality, blurry, text, watermark"
    )
    return prompt


def build_3d_prompt(spec: Dict[str, Any]) -> str:
    """
    Builds a specialized 3D architectural floorplan / cutaway prompt that inherits the SAME
    Master Design Specification (floors, room count, wood tones, roof-removed cutaway, pool, outdoor deck).
    """
    id_dna = synthesize_design_identity(spec)

    rooms_breakdown = f"{id_dna['bedrooms']} bedrooms, {id_dna['bathrooms']} bathrooms, open living room, kitchen and dining"
    if id_dna['has_courtyard']: rooms_breakdown += ", central open courtyard"
    if id_dna['has_balcony']: rooms_breakdown += ", terrace balcony"

    prompt = (
        f"A masterwork photorealistic 3D architectural top-down floor plan visualization of the SAME {id_dna['floors_label']} {id_dna['style']} residence, {id_dna['plot_size']} sqft. "
        f"Full house cutaway layout from directly above with roof removed: displaying {rooms_breakdown}. "
        f"Architectural palette: solid structural partition walls with dark charcoal top fill, {id_dna['flooring']}, {id_dna['wood_tone']} interior doors and cabinetry. "
        f"Exterior integration: {id_dna['features_str']}. "
        f"Requirements: {id_dna['original_prompt']}. "
        f"Visual standard: 90-degree orthographic bird's-eye architectural blueprint render, full layout fully furnished with beds, sofas, kitchen island, and bathroom fixtures, "
        f"soft studio ambient lighting, crisp sharp architectural lines, 8k resolution, professional 3D CAD visualization. "
        f"Negative: perspective eye-level room view, ceiling present, single empty room, blurry geometry, distorted walls, low resolution, text, watermark"
    )
    return prompt


def generate_all_specialized_prompts(spec: Dict[str, Any]) -> Dict[str, str]:
    """
    Main entry point for Stage 2 Prompt Engine.
    Converts a single Master Design Specification into 3 synchronized specialized prompts.
    """
    return {
        "exterior_prompt": build_exterior_prompt(spec),
        "interior_prompt": build_interior_prompt(spec),
        "floorplan_prompt": build_3d_prompt(spec)
    }
