"""
Specialized Architectural Image Prompt Engine (Stage 3 Refined)
==============================================================
Transforms a Master Design Specification into synchronized, specialized prompts
for Exterior, Interior, and Photorealistic 3D Layout Visualizations.

Guarantees that all 3 views represent the EXACT SAME HOUSE.
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
    flooring = interior.get("flooring", "large-format polished Italian marble")
    lighting = interior.get("lighting", "warm indirect 3000K architectural LED cove lighting")
    furniture = interior.get("furniture", f"contemporary {style} designer furniture")

    # Landscape & Features
    features_list = []
    if ext.get("pool"): features_list.append("crystal-clear swimming pool with sun deck")
    if ext.get("garden"): features_list.append("landscaped garden with manicured lawn and ornamental trees")
    if ext.get("balcony"): features_list.append("upper-level glass railing balcony")
    if ext.get("parking"): features_list.append("two-car covered parking carport")
    if ext.get("courtyard"): features_list.append("central open-air courtyard")
    if ext.get("porch"): features_list.append("covered entrance veranda")
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
        "bedrooms": spec.get("bedrooms", 4),
        "bathrooms": spec.get("bathrooms", 3),
        "plot_size": spec.get("plot_size_sqft", 2500),
        "budget": spec.get("budget_usd", 150000),
        "original_prompt": spec.get("original_prompt", "")
    }


def build_exterior_prompt(spec: Dict[str, Any]) -> str:
    """
    1. EXTERIOR CONCEPT:
    Front / three-quarter front perspective, eye-level architectural photography of the complete house.
    Strictly preserves floors, facade palette, materials, roof, entrance, windows, balcony, and landscape amenities.
    """
    id_dna = synthesize_design_identity(spec)

    prompt = (
        f"A masterwork photorealistic architectural photograph of a {id_dna['floors_label']} {id_dna['style']} {id_dna['house_type']}, {id_dna['plot_size']} sqft. "
        f"Perspective: three-quarter front eye-level architectural photography, complete building visible with realistic architectural proportions. "
        f"Facade design: finished in {id_dna['primary_color']} with {id_dna['wood_tone']} and {id_dna['stone_type']}. "
        f"Structure & Details: exact {id_dna['floors_label']} home, clearly visible entrance with {id_dna['doors']}, {id_dna['windows']}, {id_dna['roof']}. "
        f"Grounds & Environment: {id_dna['features_str']}. "
        f"Requirements: {id_dna['original_prompt']}. "
        f"Visual standard: high resolution, HD quality, realistic materials, realistic glass reflections, realistic lighting and soft shadows, natural daytime environment, luxury real-estate photography, 8k resolution. "
        f"Negative: cartoon, sketch, painting, fantasy building, distorted architecture, extra floors, random windows, random balconies, unrealistic proportions, floating objects, blurry image, text, watermark"
    )
    return prompt


def build_interior_prompt(spec: Dict[str, Any]) -> str:
    """
    2. INTERIOR CONCEPT:
    Eye-level interior architectural photography (24-28mm wide-angle feel, straight vertical lines, no extreme fisheye).
    Inherits the exact design identity (colors, wood tones, stone accents, window trims, lighting language) from the Master Design Specification.
    """
    id_dna = synthesize_design_identity(spec)

    prompt = (
        f"A masterwork photorealistic interior architectural photograph of the main living room and modular kitchen inside the SAME {id_dna['floors_label']} {id_dna['style']} residence. "
        f"Camera: eye-level interior architectural photography, 24-28mm realistic wide-angle lens feel, straight vertical lines, realistic room scale and proportions. "
        f"Synchronized identity: interior walls in {id_dna['primary_color']}, custom millwork and wall paneling in {id_dna['wood_tone']}, {id_dna['stone_type']} feature accent wall. "
        f"Finishes: {id_dna['flooring']}, {id_dna['windows']} matching exterior facade with views of the garden, {id_dna['lighting']}. "
        f"Furnishing: {id_dna['furniture']}, matching neutral and {id_dna['secondary_color']} accents. "
        f"Requirements: {id_dna['original_prompt']}. "
        f"Visual standard: high resolution, HD, luxurious, clean, realistic, architecturally believable, soft ambient natural daylight, 8k resolution, Architectural Digest photography. "
        f"Negative: cartoon, sketch, mismatched architectural style, rustic wooden cabin, generic hotel lobby, distorted furniture, fisheye distortion, low quality, blurry, text, watermark"
    )
    return prompt


def build_3d_prompt(spec: Dict[str, Any]) -> str:
    """
    3. PHOTOREALISTIC 3D LAYOUT:
    Top-down isometric cutaway 3D architectural floor plan with roof removed.
    Shows walls, rooms, bedrooms, living room, kitchen, bathrooms, dining area, corridors, doors, windows, furniture, and surrounding grounds.
    """
    id_dna = synthesize_design_identity(spec)

    rooms_breakdown = f"{id_dna['bedrooms']} bedrooms with beds, {id_dna['bathrooms']} bathrooms with fixtures, spacious living room with sofa set, modular kitchen with dining area and island, corridors and doors"
    if id_dna['has_courtyard']: rooms_breakdown += ", central open courtyard"
    if id_dna['has_balcony']: rooms_breakdown += ", upper terrace balcony"

    prompt = (
        f"A masterwork photorealistic 3D architectural top-down isometric cutaway floor plan visualization of the SAME {id_dna['floors_label']} {id_dna['style']} residence, {id_dna['plot_size']} sqft. "
        f"Perspective: top-down isometric elevated cutaway with roof removed to clearly reveal the complete interior layout from above: displaying {rooms_breakdown}. "
        f"Architectural palette: exterior walls in {id_dna['primary_color']}, solid structural partition walls with dark charcoal top fill, {id_dna['flooring']}, {id_dna['wood_tone']} interior doors and cabinetry. "
        f"Furnishing & Detail: fully furnished with beds, sofas, dining table, kitchen counters, bathroom tub and sink, indoor plants, and surrounding {id_dna['features_str']}. "
        f"Requirements: {id_dna['original_prompt']}. "
        f"Visual standard: premium 3D architectural rendering, photorealistic materials, realistic lighting and soft ambient shadows, clean CAD geometry, high detail, HD resolution, professional architectural visualization. "
        f"Negative: eye-level perspective room view, ceiling on, single empty room, technical 2D wireframe drawing, blurry geometry, distorted walls, low resolution, cartoon, text, watermark"
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
