"""
Specialized Architectural Image Prompt Engine (Stage 3 Calibrated)
=================================================================
Transforms a Master Design Specification into synchronized, specialized prompts
for Exterior, Interior, and Photorealistic 3D Layout Visualizations.

Calibrated specifically for Minimalist Scandinavian, Modern Luxury, Traditional,
and other architectural styles with strict photographic and visual standards.
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

    style = spec.get("architectural_style") or house.get("architectural_style", "Minimalist Scandinavian")
    floors = spec.get("floors") or house.get("floors", 2)
    house_type = spec.get("house_type") or house.get("house_type", "Scandinavian Minimalist Home" if "scandinavian" in style.lower() else "Luxury Residence")
    environment = spec.get("environment") or ext.get("environment", "landscaped residential grounds")

    # Colors
    ext_colors = ext.get("colors", ["warm off-white", "light natural oak"])
    primary_color = ext.get("primary_color") or (ext_colors[0] if ext_colors else "warm off-white")
    secondary_color = ext.get("secondary_color") or (ext_colors[1] if len(ext_colors) > 1 else "light natural oak")
    color_palette_str = ", ".join(ext_colors)

    # Materials
    materials = ext.get("materials", ["smooth off-white plaster render", "blonde oak timber", "clear glass"])
    materials_str = ", ".join(materials)

    # Wood & Stone specific identification
    is_scandi = "scandinavian" in style.lower() or "nordic" in style.lower() or "minimalist" in style.lower()

    if is_scandi:
        wood_tone = "blonde natural light oak timber"
        stone_type = "smooth limestone and plaster accents"
        flooring = "light blonde oak herringbone hardwood flooring"
        lighting = "soft diffused Nordic daylight, sculptural woven pendant lamp, and warm ambient floor lamps"
        furniture = "tailored Scandinavian linen sofa, round light oak nested coffee tables, and curved wooden chairs"
        doors = "blonde light oak natural wood pivot door"
        windows = "minimalist black-framed floor-to-ceiling glass sliding doors and recessed windows"
    else:
        wood_tone = "natural walnut timber"
        for mat in materials + ext_colors:
            if "oak" in mat: wood_tone = "natural light oak timber"
            elif "teak" in mat: wood_tone = "handcrafted teak wood"
            elif "cedar" in mat: wood_tone = "rich cedar timber"
            elif "walnut" in mat: wood_tone = "natural walnut wood accents"

        stone_type = "natural stone cladding"
        for mat in materials:
            if "brick" in mat: stone_type = "exposed brickwork"
            elif "slate" in mat: stone_type = "dark grey slate stone"
            elif "travertine" in mat: stone_type = "warm travertine stone"
            elif "granite" in mat: stone_type = "dark charcoal stone"
            elif "marble" in mat: stone_type = "polished marble"
            elif "grey" in mat or "gray" in mat or "dark" in mat: stone_type = "dark grey natural stone"

        windows = ext.get("windows", "large black-framed floor-to-ceiling glass windows")
        doors = ext.get("doors", "grand pivot wooden entrance door")
        flooring = interior.get("flooring", "large-format polished Italian marble")
        lighting = interior.get("lighting", "warm indirect 3000K architectural LED lighting")
        furniture = interior.get("furniture", f"contemporary {style} designer furniture")

    roof = ext.get("roof", "flat contemporary roof")

    # Landscape & Features
    features_list = []
    if ext.get("pool"): features_list.append("rectangular swimming pool with wooden sun deck")
    if ext.get("garden"): features_list.append("landscaped garden with white birch trees and ornamental grasses" if is_scandi else "landscaped garden with green lawn")
    if ext.get("balcony"): features_list.append("upper-level glass railing balcony")
    if ext.get("parking"): features_list.append("gravel driveway and covered carport")
    if ext.get("courtyard"): features_list.append("central open-air courtyard")
    if ext.get("porch"): features_list.append("covered entrance veranda")
    features_str = ", ".join(features_list) if features_list else "landscaped outdoor grounds"

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
        "furniture": furniture,
        "features_str": features_str,
        "is_scandi": is_scandi,
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
    Wide three-quarter front architectural view from a distance with generous margins on all sides.
    Ensures the complete house is visible without close cropping.
    """
    id_dna = synthesize_design_identity(spec)

    prompt = (
        f"Wide-angle architectural photograph of a {id_dna['floors_label']} {id_dna['style']} {id_dna['house_type']}, {id_dna['plot_size']} sqft. "
        f"Perspective: full property wide three-quarter front view from a distance with generous space on all sides, complete building fully visible from ground to roof, centered in frame, green lawn and gravel pathway in foreground, open sky above, never cropped, no close-ups. "
        f"Facade: clean geometric cubic volumes finished in {id_dna['primary_color']} with {id_dna['wood_tone']} and {id_dna['stone_type']}, {id_dna['windows']}, clearly visible entrance with {id_dna['doors']}, {id_dna['roof']}. "
        f"Grounds: {id_dna['features_str']}, situated on {id_dna['environment']}. "
        f"Visual standard: high resolution, HD, luxury real-estate photography, natural bright daytime sunlight, crisp reflections, realistic shadows, 8k resolution. "
        f"Negative: close-up, cropped house, tight shot, cut off edges, cartoon, sketch, painting, fantasy building, distorted architecture, extra floors, blurry, text, watermark"
    )
    return prompt


def build_interior_prompt(spec: Dict[str, Any]) -> str:
    """
    2. INTERIOR CONCEPT:
    Eye-level interior architectural photography (24mm wide angle, straight verticals).
    Inherits the exact design identity (colors, wood tones, stone accents, window trims, lighting language) from the Master Design Specification.
    """
    id_dna = synthesize_design_identity(spec)

    prompt = (
        f"Eye-level architectural photograph of the expansive main living room and open dining area inside the SAME {id_dna['floors_label']} {id_dna['style']} residence. "
        f"Camera: 24mm wide-angle interior architectural photography, straight vertical lines, realistic room scale and proportions. "
        f"Synchronized identity: interior walls in {id_dna['primary_color']} and soft greige, custom {id_dna['wood_tone']} credenza and wall accents, {id_dna['stone_type']}. "
        f"Finishes: {id_dna['flooring']}, {id_dna['windows']} with sheer linen curtains and views of the surrounding garden, {id_dna['lighting']}. "
        f"Furnishing: {id_dna['furniture']}, soft textured throw pillows, cozy area rug, indoor potted fiddle leaf fig plants. "
        f"Visual standard: high resolution, HD, luxurious Scandinavian aesthetic, clean, serene, airy, realistic, soft ambient natural daylight, 8k resolution, Architectural Digest photography. "
        f"Negative: dark moody cave, cartoon, sketch, mismatched architecture, rustic wooden log cabin, generic hotel lobby, distorted furniture, fisheye distortion, low quality, blurry, text, watermark"
    )
    return prompt


def build_3d_prompt(spec: Dict[str, Any]) -> str:
    """
    3. PHOTOREALISTIC 3D LAYOUT:
    Straight 90-degree overhead bird's-eye architectural 3D floor plan visualization with roof removed.
    Matches the exact benchmark format: dark thick boundary walls, light natural wood plank flooring,
    furnished bedrooms, tiled bathrooms with glass showers, living room, dining, warm directional sunlight rays,
    and surrounding green trees around the perimeter.
    """
    id_dna = synthesize_design_identity(spec)

    rooms_breakdown = (
        f"furnished {id_dna['bedrooms']} bedrooms with {id_dna['wood_tone']} beds and side tables, "
        f"{id_dna['bathrooms']} modern bathrooms with glass walk-in showers and ceramic vanities, "
        f"spacious Scandinavian living room area with comfortable sofa set, open dining space, and wooden interior doors"
    )

    prompt = (
        f"Stunning photorealistic 3D architectural floor plan layout of the SAME {id_dna['floors_label']} {id_dna['style']} house, {id_dna['plot_size']} sqft. "
        f"Perspective: 90-degree straight overhead bird's-eye top-down view with entire roof sliced away to reveal the full interior room layout. "
        f"Walls & Flooring: thick solid dark charcoal boundary walls, {id_dna['flooring']} throughout all rooms. "
        f"Furnished layout: {rooms_breakdown}, indoor potted green plants. "
        f"Lighting & Environment: warm directional sunlight casting soft realistic shadows across the wooden floorboards, lush green trees and foliage surrounding the exterior perimeter walls. "
        f"Visual standard: ultra-detailed 3D architectural rendering, high resolution, HD quality, realistic materials, photorealistic interior layout presentation. "
        f"Negative: ceiling on, eye-level perspective, blank white model, grey CAD wireframe, low detail, blurry, distorted walls, text, watermark"
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
