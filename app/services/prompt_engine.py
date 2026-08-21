"""
Intelligent Prompt Engine — Exact 1:1 Reference Archetype v4
============================================================
Derives Exterior, Interior, and 3D Layout 100% matched to the user's uploaded reference image (media_1787337986379.png):

1. EXTERIOR: Two-storey modern cubic luxury residence with soft lilac/lavender smooth render walls,
   black-framed floor-to-ceiling glass wall on ground floor, upper glass balcony terrace, and lavender flower bushes.

2. INTERIOR: Living room inside the SAME house with soft lilac/lavender walls, light blonde oak wide-plank wood flooring,
   cream white modular sofa, white coffee table, framed wall art, and floor-to-ceiling glass window showing lavender bushes.

3. 3D LAYOUT (EXACT REFERENCE REPRODUCTION):
   - 90-degree straight top-down overhead architectural cutaway of the ENTIRE square floor plan with NO roof.
   - Thick solid black outer boundary walls framing the square layout on all 4 sides.
   - Vertical blonde wood plank flooring running continuously across all living and bedroom areas.
   - Purple/lavender fabric bedsheets on the left-side bedroom beds and purple central accent floor rug.
   - Office desk with black office chair in top center section.
   - Tiled bathrooms with glass showers in top-right corner.
   - Warm golden sunlight streaming diagonally across the wood floor from top-right.
   - Dense green tree foliage bordering the black exterior walls on left, right, and top edges.
"""

from typing import Dict, Any


def build_exterior_prompt(spec: Dict[str, Any]) -> str:
    """
    A. EXTERIOR CONCEPT — Matched to reference image 1.
    """
    plot_size = spec.get("plot_size_sqft", 2500)

    prompt = (
        f"Ultra-HD 8K photorealistic architectural exterior photograph of a modern two-storey cubic luxury house, {plot_size} sqft. "
        f"Perspective: eye-level full front symmetric view of the two-storey modern cubic building, centered in frame, complete house visible from ground to flat roofline, no cropping. "
        f"Facade Architecture: smooth matte soft lilac lavender tinted plaster render walls, "
        f"ground floor features expansive floor-to-ceiling black-framed glass wall revealing warm glowing interior lighting inside, "
        f"upper floor features a glass-railed balcony terrace with black-framed glass sliding doors, "
        f"flat roofline with clean shadow gap. "
        f"Landscaping: low purple lavender flower bushes and green shrubs along front foundation, manicured lawn, evergreen trees in background, soft evening sky. "
        f"Quality: Hasselblad H6D-100c medium format camera, sharp architectural focus, soft realistic illumination, 8K resolution. "
        f"Negative: cropped building, dark moody cave, rustic brick, old traditional house, cartoon, sketch, watermark, text, blurry, low quality"
    )
    return prompt


def build_interior_prompt(spec: Dict[str, Any]) -> str:
    """
    B. INTERIOR CONCEPT — Matched to reference image 2.
    """
    prompt = (
        "Ultra-HD 8K photorealistic interior architectural photograph inside the main living room of the SAME modern luxury residence. "
        "Camera: wide-angle interior photograph at eye level, straight vertical lines, realistic room scale. "
        "Walls & Ceiling: smooth matte soft lilac lavender tinted interior walls, smooth flat white ceiling. "
        "Flooring: light natural blonde oak wide-plank hardwood flooring throughout. "
        "Windows: floor-to-ceiling black-framed glass window on the right wall looking out to lavender bushes and green trees outside, warm natural sunlight streaming across the floor. "
        "Furniture: cream white modular low-profile sofa, white rectangular coffee table, cream floor ottoman, "
        "large framed minimalist artwork hanging on the lilac center wall, potted tall lavender plant in ceramic pot beside the window. "
        "Lighting: soft bright natural daylight flooding the space, warm ambient glow. "
        "Quality: Architectural Digest photography, sharp photorealistic focus, 8K resolution. "
        "Negative: dark room, exterior photo, yellow brick, rustic wood cabin, generic hotel, fisheye distortion, cartoon, sketch, watermark, text, blurry"
    )
    return prompt


def build_3d_prompt(spec: Dict[str, Any]) -> str:
    """
    C. PHOTOREALISTIC 3D LAYOUT — Exact reproduction of reference image media_1787337986379.png.
    """
    plot_size = spec.get("plot_size_sqft", 2500)

    prompt = (
        f"Ultra-HD 8K photorealistic 3D architectural floor plan cutaway of the ENTIRE square house layout, {plot_size} sqft, exact 1:1 match to reference render. "
        f"Perspective: 90-degree straight top-down overhead bird's-eye architectural view looking directly down inside the entire square floor plan with roof completely removed. "
        f"Outer Boundary & Perimeter: thick solid black exterior boundary walls enclosing the square house footprint on all four sides. "
        f"Flooring: vertical light blonde oak wood plank flooring running continuously across all room spaces. "
        f"Specific Furnishings & Room Elements: "
        f"LEFT SIDE — two bedrooms featuring purple lavender fabric bed sheets on beds, with a white tiled bathroom between them; "
        f"CENTER — large purple floor area rug on the blonde wood floor, with central living room and wooden coffee table; "
        f"TOP CENTER — home office workstation desk with a black swivel office chair; "
        f"TOP RIGHT — tiled bathroom suite with glass walk-in shower and white sanitary fixtures; "
        f"BOTTOM CENTER — entry foyer wooden floor porch with indoor potted green plants. "
        f"Lighting & Shadows: warm golden sunlight streaming diagonally across the wood floor from the top right, casting long directional soft shadows. "
        f"Exterior Surroundings: dense green tree foliage bordering the black exterior walls on the left, right, and top edges against a soft grey backdrop. "
        f"Quality: professional 3D architectural rendering, crisp wood plank textures, soft ambient occlusion, 8K resolution. "
        f"Negative: eye-level view, angled isometric perspective, exterior facade photo, roof on, flat 2D blueprint lines, wireframe, low quality, blurry, watermark, text"
    )
    return prompt


def generate_all_specialized_prompts(spec: Dict[str, Any]) -> Dict[str, str]:
    """
    Main Entry Point — Converts Master Specification into 3 synchronized prompts
    matched to the user's reference images.
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
