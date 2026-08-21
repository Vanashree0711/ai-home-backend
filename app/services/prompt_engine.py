"""
Intelligent Prompt Engine — Locked 3-View Reference Archetype v3
================================================================
Derives Exterior, Interior, and 3D Floor Plan directly from the user's
uploaded 3 reference images (Lavender-tinged Modern Cubic Residence):

Image 1 (Exterior): Two-storey modern cubic volume with soft lilac/lavender smooth render walls,
  upper glass-balcony terrace, floor-to-ceiling glass sliding doors on ground level showing interior warm glow,
  glass-railed upper windows, dark metal door trims, low lavender shrubbery landscaping in front.

Image 2 (Interior): Modern living room inside the same home with soft lavender/lilac matte walls,
  light oak hardwood floors, cream modular sofa set, white coffee table, large framed artwork on wall,
  large floor-to-ceiling glass window on right looking out to lavender bushes and trees, warm natural sunlight.

Image 3 (3D Floor Plan): 90-degree top-down architectural floor plan cutaway showing the entire layout,
  dark thick perimeter walls, light oak wood plank flooring throughout, purple/lavender accent rug and bedspreads,
  fully furnished living room, master bedroom, guest rooms, tiled bathrooms, surrounded by green trees and foliage.
"""

from typing import Dict, Any


def build_exterior_prompt(spec: Dict[str, Any]) -> str:
    """
    A. EXTERIOR VIEW — Matched 1:1 to Reference Image 1.
    """
    style = spec.get("architectural_style", "Modern Luxury")
    floors = spec.get("floors", 2)
    floors_label = f"{floors}-storey" if floors > 1 else "single-storey"
    plot_size = spec.get("plot_size_sqft", 2500)
    environment = spec.get("environment", "landscaped residential grounds")

    prompt = (
        f"Ultra-HD 8K photorealistic architectural exterior photograph of a modern two-storey cubic luxury house, {plot_size} sqft. "
        f"Perspective: eye-level full front view of the two-storey modern cubic building, centered in frame, complete house visible from ground to roof, no cropping. "
        f"Exterior Architecture: clean modern cubic geometric volume with smooth matte light lilac lavender tinted plaster render walls, "
        f"upper floor features a glass-railed balcony terrace with large black-framed glass sliding doors, "
        f"ground floor features expansive floor-to-ceiling glass wall with black frames revealing warm interior lighting inside, "
        f"flat roofline with clean shadow gap. "
        f"Landscaping: low purple lavender flower bushes and green shrubs planted along the front foundation, manicured lawn, trees in background, soft evening twilight sky. "
        f"Quality: Hasselblad H6D-100c medium format camera, sharp architectural focus, soft realistic illumination, 8K resolution. "
        f"Negative: cropped building, dark moody cave, rustic brick, old traditional house, cartoon, sketch, watermark, text, blurry, low quality"
    )
    return prompt


def build_interior_prompt(spec: Dict[str, Any]) -> str:
    """
    B. INTERIOR VIEW — Matched 1:1 to Reference Image 2.
    """
    style = spec.get("architectural_style", "Modern Luxury")

    prompt = (
        "Ultra-HD 8K photorealistic interior architectural photograph inside the main living room of the SAME modern luxury residence. "
        "Camera: wide-angle interior photograph at eye level, straight vertical lines, realistic room scale. "
        "Walls & Ceiling: smooth matte soft lilac lavender tinted interior walls, smooth flat ceiling. "
        "Flooring: light natural blonde oak hardwood flooring. "
        "Windows: floor-to-ceiling black-framed glass window on the right wall looking out to lavender bushes and green trees, soft warm sunlight streaming across the floor. "
        "Furniture: cream white modular low-profile sofa, white rectangular coffee table, cream floor ottoman, "
        "large framed minimalist artwork hanging on the lilac center wall, potted tall lavender plant in ceramic pot beside the window. "
        "Lighting: soft bright natural daylight flooding the space, warm ambient glow. "
        "Quality: Architectural Digest photography, sharp photorealistic focus, 8K resolution. "
        "Negative: dark room, exterior photo, yellow brick, rustic wood cabin, generic hotel, fisheye distortion, cartoon, sketch, watermark, text, blurry"
    )
    return prompt


def build_3d_prompt(spec: Dict[str, Any]) -> str:
    """
    C. 3D ARCHITECTURAL FLOOR PLAN CUTAWAY — Matched 1:1 to Reference Image 3.
    """
    bedrooms = spec.get("bedrooms", 3)
    bathrooms = spec.get("bathrooms", 2)
    plot_size = spec.get("plot_size_sqft", 2500)

    prompt = (
        f"Ultra-HD 8K photorealistic 3D architectural floor plan cutaway of the complete home layout, {plot_size} sqft. "
        f"Perspective: top-down 90-degree bird's-eye view looking straight down inside all furnished rooms with the roof completely removed. "
        f"Structure: thick dark charcoal exterior perimeter walls enclosing the house layout, clean white interior partition walls with doorway openings. "
        f"Room Layout: central open living room with a purple area rug and sofa, master bedroom with purple bedspread, "
        f"two secondary bedrooms with made beds, two modern tiled bathrooms, home office desk area, and kitchen counter. "
        f"Flooring & Finishes: light natural blonde oak wood plank flooring throughout all living and bedroom spaces, purple lavender accent textiles on beds and rugs. "
        f"Lighting & Grounds: warm interior ambient lights casting directional soft shadows on the wood floors, green trees and foliage framing the dark exterior boundary walls. "
        f"Quality: professional 3D architectural rendering, crisp textures, soft ambient occlusion, 8K resolution. "
        f"Negative: eye-level view, exterior facade, roof covering rooms, flat 2D blueprint, wireframe, low quality, blurry, watermark, text"
    )
    return prompt


def generate_all_specialized_prompts(spec: Dict[str, Any]) -> Dict[str, str]:
    """
    Main Entry Point — Converts Master Specification into 3 synchronized prompts
    matched to the user's 3 reference images.
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
