"""
Intelligent Prompt Engine — Master Quality 8K Ultra-HD Pipeline v5
===================================================================
Injects master-level photography and 3D archviz quality directives across all 3 prompts:

1. EXTERIOR: Hasselblad H6D-100c medium format camera, 100-megapixel raw architectural photo,
   8K UHD resolution, razor-sharp focus, crisp photorealistic textures.

2. INTERIOR: Architectural Digest cover photography, 8K UHD raw photograph, sharp crisp focus,
   hyperrealistic daylight and shadows.

3. 3D LAYOUT: Octane Render 8K, V-Ray 3D architectural visualization, Unreal Engine 5 archviz quality,
   ray-traced global illumination, razor-sharp wood plank grain and tile textures.
"""

from typing import Dict, Any


def build_exterior_prompt(spec: Dict[str, Any]) -> str:
    """
    A. EXTERIOR CONCEPT — Master 8K Ultra-HD Architectural Quality.
    """
    plot_size = spec.get("plot_size_sqft", 2500)

    prompt = (
        f"Masterpiece 8K UHD photorealistic architectural exterior photograph of a modern two-storey cubic luxury house, {plot_size} sqft. "
        f"Perspective: eye-level full front symmetric view of the two-storey modern cubic building, centered in frame, complete house visible from ground to flat roofline, no cropping. "
        f"Facade Architecture: smooth matte soft lilac lavender tinted plaster render walls, "
        f"ground floor features expansive floor-to-ceiling black-framed glass wall revealing warm glowing interior lighting inside, "
        f"upper floor features a glass-railed balcony terrace with black-framed glass sliding doors, "
        f"flat roofline with clean shadow gap. "
        f"Landscaping: low purple lavender flower bushes and green shrubs along front foundation, manicured lawn, evergreen trees in background, soft evening sky. "
        f"Camera & Quality Standard: Hasselblad H6D-100c medium format camera, 100-megapixel raw photo, razor-sharp architectural focus, hyperrealistic lighting and realistic shadows, crisp material textures, 8k resolution, master quality. "
        f"Negative: cropped building, dark moody cave, rustic brick, old traditional house, cartoon, sketch, watermark, text, blurry, low quality, noise, artifacts, lowres"
    )
    return prompt


def build_interior_prompt(spec: Dict[str, Any]) -> str:
    """
    B. INTERIOR CONCEPT — Master 8K Ultra-HD Architectural Digest Quality.
    """
    prompt = (
        "Masterpiece 8K UHD photorealistic interior architectural photograph inside the main living room of the SAME modern luxury residence. "
        "Camera: Architectural Digest cover photography, wide-angle interior photograph at eye level, straight vertical lines, realistic room scale, 100-megapixel raw photo. "
        "Walls & Ceiling: smooth matte soft lilac lavender tinted interior walls, smooth flat white ceiling. "
        "Flooring: light natural blonde oak wide-plank hardwood flooring throughout with crisp wood grain detail. "
        "Windows: floor-to-ceiling black-framed glass window on the right wall looking out to lavender bushes and green trees outside, warm natural sunlight streaming across the floor. "
        "Furniture: cream white modular low-profile sofa, white rectangular coffee table, cream floor ottoman, "
        "large framed minimalist artwork hanging on the lilac center wall, potted tall lavender plant in ceramic pot beside the window. "
        "Lighting & Ambiance: soft bright natural daylight flooding the space, warm ambient glow, hyperrealistic shadows. "
        "Quality: 8K resolution, razor-sharp photorealistic focus, master architectural interior quality. "
        "Negative: dark room, exterior photo, yellow brick, rustic wood cabin, generic hotel, fisheye distortion, cartoon, sketch, watermark, text, blurry, noise, lowres"
    )
    return prompt


def build_3d_prompt(spec: Dict[str, Any]) -> str:
    """
    C. PHOTOREALISTIC 3D LAYOUT — Master 8K Octane & V-Ray Ultra-Sharp 3D ArchViz Quality.
    """
    plot_size = spec.get("plot_size_sqft", 2500)

    prompt = (
        f"Masterpiece 8K UHD photorealistic 3D architectural floor plan cutaway render of the ENTIRE square house layout, {plot_size} sqft. "
        f"Perspective: exact 90-degree straight top-down overhead bird's-eye architectural view looking directly down inside the entire square floor plan with roof completely removed. "
        f"Outer Boundary & Perimeter: thick solid matte black exterior boundary walls enclosing the square house footprint on all four sides. "
        f"Flooring: vertical light blonde oak wood plank flooring with ultra-sharp high-definition wood grain texture running continuously across all room spaces. "
        f"Specific Furnishings & Room Elements: "
        f"LEFT SIDE — two bedrooms featuring purple lavender fabric bed sheets on beds, with a white tiled bathroom between them; "
        f"CENTER — large purple floor area rug on the blonde wood floor, with central living room and wooden coffee table; "
        f"TOP CENTER — home office workstation desk with a black swivel office chair; "
        f"TOP RIGHT — tiled bathroom suite with glass walk-in shower and white sanitary fixtures; "
        f"BOTTOM CENTER — entry foyer wooden floor porch with indoor potted green plants. "
        f"Rendering Engine & Quality Standard: Octane Render 8K ultra-sharp details, V-Ray 3D architectural visualization, Unreal Engine 5 archviz photorealism, ray-traced global illumination, warm golden sunlight streaming diagonally across the wood floor from the top right, casting realistic long directional soft shadows. "
        f"Exterior Surroundings: dense green tree foliage bordering the black exterior walls on the left, right, and top edges against a soft grey backdrop. "
        f"Quality: 8K resolution, razor-sharp wood plank textures, crystal clear wall boundaries, master architectural 3D rendering. "
        f"Negative: eye-level view, angled isometric perspective, exterior facade photo, roof on, flat 2D blueprint lines, wireframe, low quality, blurry, pixelated, noise, watermark, text"
    )
    return prompt


def generate_all_specialized_prompts(spec: Dict[str, Any]) -> Dict[str, str]:
    """
    Main Entry Point — Converts Master Specification into 3 synchronized prompts
    matched to the user's reference images with Master 8K Quality.
    """
    return {
        "exterior_prompt": build_exterior_prompt(spec),
        "interior_prompt": build_interior_prompt(spec),
        "floorplan_prompt": build_3d_prompt(spec),
    }


def synthesize_design_identity(spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compatibility shim for consistency validator.
    """
    return {
        "style": spec.get("architectural_style", "Modern Luxury"),
        "house_type": "Modern Cubic Residence",
        "floors": 2,
        "floors_label": "2-storey",
        "environment": "landscaped residential grounds",
        "primary_color": "soft lilac lavender",
        "secondary_color": "dark metal trim",
        "color_palette_str": "soft lilac lavender, bright white, light blonde oak",
        "materials_str": "smooth plaster render, structural glass, blonde oak timber",
        "wood_tone": "light blonde oak",
        "stone_type": "smooth render",
        "windows": "floor-to-ceiling glass windows",
        "doors": "black-framed glass sliding doors",
        "roof": "flat modern roofline",
        "entry": "front glass entrance",
        "grounds": "lavender flower bushes and green shrubs",
        "flooring": "light natural blonde oak hardwood flooring",
        "walls_int": "smooth matte soft lilac lavender interior walls",
        "windows_int": "floor-to-ceiling black-framed glass window",
        "window_view": "lavender bushes and green trees",
        "furniture": "cream white modular sofa and white coffee table",
        "plants": "potted lavender plant",
        "dining": "dining area",
        "bookshelf": "credenza along wall",
        "lighting": "soft natural daylight with warm ambient glow",
        "ceiling": "smooth flat ceiling",
        "room_layout": "central living, master bedroom, guest bedrooms, tiled bathrooms",
        "staircase": "open interior staircase",
        "is_scandi": False,
        "bedrooms": spec.get("bedrooms", 3),
        "bathrooms": spec.get("bathrooms", 2),
        "plot_size": spec.get("plot_size_sqft", 2500),
        "features_str": "lavender landscaping and green trees",
        "original_prompt": spec.get("original_prompt", ""),
    }
