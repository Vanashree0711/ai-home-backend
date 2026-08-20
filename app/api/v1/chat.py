import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio

router = APIRouter()


def get_architectural_response(prompt: str) -> str:
    """
    Expert AI Architect response system with comprehensive architectural knowledge.
    Covers all major home design topics with professional, detailed answers.
    """
    p = prompt.lower()

    # Flooring
    if any(w in p for w in ['floor', 'flooring', 'tile', 'marble', 'hardwood', 'parquet', 'terrazzo', 'carpet']):
        return """For luxury home flooring, here are the top professional recommendations:

**1. Marble (Premium Choice)**
Calacatta Gold and Carrara White marble are the pinnacle of luxury. Ideal for entrance halls, bathrooms, and formal reception rooms. Polished finish reflects light beautifully. Cost: $50–$200/sqft installed. Requires annual sealing.

**2. Wide-Plank Engineered Hardwood**
European White Oak (200mm+ wide planks) in a matte wire-brushed finish is the most popular choice for contemporary luxury homes. More dimensionally stable than solid wood — resists humidity-induced warping. Cost: $20–$60/sqft installed.

**3. Large Format Porcelain Tiles (120x120cm or larger)**
Near-invisible grout lines create a seamless, contemporary floor plane. Available in concrete, stone, and wood-look finishes. Extremely durable and easy to maintain. Cost: $25–$90/sqft installed.

**4. Travertine Stone**
Warm, natural, earthy tones. Perfect for Mediterranean, classic, or biophilic design styles. Filled and polished or tumbled finishes available. Cost: $30–$80/sqft.

**5. Polished Concrete with Aggregate**
The ultimate industrial-luxury choice. Can be ground and polished to a mirror finish or left with a matte texture. Radiant floor heating works beautifully with concrete. Cost: $15–$40/sqft.

**My Recommendation:** Use Calacatta marble in the entrance hall and bathrooms, wide-plank White Oak in living and bedroom areas, and large-format porcelain in the kitchen. This layering of materials creates visual interest and defines zones naturally."""

    # Exterior and materials
    elif any(w in p for w in ['exterior', 'facade', 'cladding', 'material', 'wall', 'brick', 'stone', 'concrete', 'steel', 'timber', 'wood']):
        return """The best exterior materials for a luxury home — ranked by prestige and durability:

**1. Natural Limestone Ashlar (Most Prestigious)**
Hand-cut Portland or Jura limestone is used in the world's finest estates and government buildings. Extremely durable (1000+ year lifespan), ages beautifully, and commands immediate visual authority. Cost: $80–$250/sqft.

**2. Board-Formed Architectural Concrete**
Smooth, contemporary, and timeless. The formwork texture (wood grain, horizontal boards) is captured in the concrete surface permanently. Used by the world's leading architects. Cost: $50–$120/sqft.

**3. Corten Weathering Steel Panels**
Develops a natural rust-red patina that stabilises after 2–3 years and actually protects the steel underneath. The changing colours with seasons are architecturally dramatic. Cost: $60–$150/sqft.

**4. Zinc or Titanium Cladding**
Used extensively in high-end European architecture. Develops a beautiful blue-grey patina over decades. Extremely low maintenance, 80+ year lifespan. Cost: $80–$200/sqft.

**5. Accoya Modified Timber**
Thermally or acetylation-modified wood that resists rot, insects, and dimensional movement. Can be left to silver naturally or painted. Used in premium Scandinavian and contemporary architecture. Cost: $40–$90/sqft.

**Combination Strategy:** The most sophisticated contemporary homes combine 2–3 materials — for example, a base of board-formed concrete with Corten steel upper panels and Accoya timber window surrounds. Material transitions at floor-plate levels create a natural and logical composition."""

    # Cost and budget
    elif any(w in p for w in ['cost', 'budget', 'price', 'expensive', 'cheap', 'afford', 'estimate', 'sqft', 'per square']):
        return """Here is a professional construction cost breakdown for luxury residential projects:

**Cost Per Square Foot — Luxury Grade:**
• Standard construction: $200–$350/sqft
• High-end luxury: $350–$600/sqft
• Ultra-luxury / custom: $600–$1,500+/sqft

**Budget Allocation (Recommended Split):**
• Foundation & Structure: 25–30% of total budget
• Exterior envelope (walls, roof, windows): 20–25%
• Interior finishes: 25–30%
• MEP (Mechanical, Electrical, Plumbing): 15–20%
• Landscaping & Site Works: 10–15%
• Contingency (always include): 10–15%

**Realistic Total Cost Estimates:**
• 1,500 sqft luxury home: $500K – $900K
• 2,500 sqft luxury home: $900K – $1.5M
• 4,000 sqft luxury home: $1.4M – $2.4M
• 6,000 sqft ultra-luxury: $2.5M – $5M+

**Key Cost Drivers:**
1. Site conditions (rock, slope, soil type)
2. Geographic location (labour costs vary significantly)
3. Material specification level
4. Complexity of architectural form (curves, cantilevers cost more)
5. Smart home and AV integration

**Cost-Saving Tips Without Compromising Quality:**
• Invest in a simple building form — complex geometries add 15–25% to structural costs
• Splurge on entry hall, kitchen, and primary bathroom — these have the highest ROI
• Use premium materials selectively in high-visibility areas only"""

    # Safety near water
    elif any(w in p for w in ['safe', 'lake', 'flood', 'water', 'river', 'coastal', 'ocean', 'beach', 'monsoon', 'rain', 'drainage']):
        return """Building near water requires careful engineering. Here is a professional assessment:

**✅ Structural Safety Measures:**

**1. Foundation System**
Never use a shallow pad or strip foundation near water. Use deep driven concrete piles (12–18m depth) or a reinforced concrete raft foundation with waterproof membrane. This transfers loads below the seasonal water table fluctuation zone.

**2. Flood Elevation**
Check your local FEMA or equivalent flood zone maps. If in a flood risk zone, your finished floor level must be elevated minimum 600mm above the 1-in-100-year flood level. Design the ground floor as a parking/utility level if flood risk is significant.

**3. Setback Requirements**
Most jurisdictions require 15–50m setback from the water's edge. Check with your local planning authority before proceeding with any design.

**4. Moisture Protection**
• All exterior materials must be rated for high-humidity environments
• Use marine-grade 316 stainless steel for all fixings and hardware
• Install a comprehensive waterproof membrane on all below-grade walls
• Pressure-treated lumber for all structural timber

**5. Site Drainage**
Grade the entire site to slope AWAY from the building at minimum 2% gradient. Install a French drain perimeter system at foundation level. Consider a sump pump system in the basement if applicable.

**6. Vegetation Buffer**
Plant native vegetation between the building and the water's edge. This stabilises the bank, filters runoff, and provides a natural barrier.

**✅ Conclusion:** With proper engineering, a lakeside or waterfront home is absolutely safe — and the lifestyle and views are incomparable. The key is engaging a structural engineer with waterfront experience from day one."""

    # Sustainability and eco
    elif any(w in p for w in ['sustainable', 'eco', 'green', 'energy', 'solar', 'environment', 'efficient', 'passive', 'carbon', 'heat pump']):
        return """Here are the most impactful sustainable design strategies, ranked by cost-effectiveness:

**Tier 1 — Passive Design (Highest ROI, Zero Running Cost):**

**1. Building Orientation**
Orient the long axis East-West. Place primary living spaces and large windows on the south-facing facade (northern hemisphere) to maximise winter solar gain. Deep overhangs (600–900mm) block the high summer sun while admitting low winter sun.

**2. Super-Insulation**
Walls: Mineral wool insulation to achieve U-value < 0.15 W/m²K
Roof: R-60 insulation equivalent
Windows: Triple-glazed, argon-filled, thermally broken frames (U-value < 0.8 W/m²K)

**3. Airtightness + HRV**
Target air permeability < 1.0 m³/hr/m² at 50Pa pressure. Install a Heat Recovery Ventilation (HRV) system to provide continuous fresh air while recovering 80–90% of the heat from exhaust air.

**Tier 2 — Active Systems:**

**4. Heat Pump System**
Air-source or ground-source heat pumps provide 300–400% efficiency vs gas boilers. Provide both heating and cooling from a single system. Pair with underfloor heating for maximum comfort.

**5. Rooftop Solar PV**
A 10kW system (approximately 28 panels, 70m²) generates 10,000–14,000 kWh/year. At current electricity prices, payback period is 6–9 years. Battery storage (10–15kWh) enables full self-sufficiency.

**6. Rainwater Harvesting**
10,000-litre underground cistern collects roof runoff for garden irrigation and toilet flushing — reducing mains water consumption by 40–50%.

**Target Certification:** Design to Passive House (Passivhaus) standard for maximum energy performance. A certified Passive House uses 90% less heating energy than a standard building."""

    # Rooms and layout
    elif any(w in p for w in ['bedroom', 'bathroom', 'kitchen', 'living', 'layout', 'plan', 'room', 'space', 'open plan', 'floor plan', 'design']):
        return """Here are professional standards for luxury home room design and spatial layout:

**Spatial Hierarchy Principles:**
Design a clear sequence from public → semi-public → private zones. The emotional journey through a home is as important as the individual rooms themselves.

**Entrance Hall:**
• Minimum 15–20sqm for a luxury home
• Ceiling height: minimum 4m to create a grand impression
• Visual axis should extend through to the garden or a feature element

**Living Room:**
• Open-plan living/dining/kitchen is the contemporary luxury standard
• Minimum 50sqm for the combined zone in a 4-bedroom home
• Multiple seating zones within the open plan (conversation area, TV area, library nook)
• Double-height ceiling or large skylights where possible

**Primary Bedroom Suite:**
• Minimum 40sqm including ensuite and walk-in wardrobe
• Ensuite: minimum 12sqm with freestanding bath, double vanity, large shower
• Walk-in wardrobe: minimum 8sqm, ideally with island display unit
• Direct access to private terrace or balcony

**Guest Bedrooms:**
• Minimum 18–22sqm per room
• Every bedroom should have an ensuite bathroom in a luxury home
• Natural daylight from minimum one external window

**Kitchen Design:**
• The 'work triangle' (fridge–sink–cooktop) perimeter: maximum 6m
• Kitchen island minimum 1.2m × 2.4m with seating
• Separate butler's pantry/prep kitchen for homes over 4,000sqft
• Walk-in pantry with shelving and worksurface

**General Rules:**
• Every primary room must have access to natural daylight
• Circulation corridors: minimum 1.2m wide, ideally 1.5m+
• Provide visual connection between indoors and garden from key living spaces"""

    # Roof types
    elif any(w in p for w in ['roof', 'roofing', 'flat roof', 'pitched', 'gable', 'hip roof', 'slate', 'metal roof']):
        return """A professional guide to roof types for luxury homes:

**1. Flat Roof (Low-Pitch ≤5°)**
The contemporary luxury standard. Clean horizontal lines, enables rooftop terraces, green roofs, and solar panels. Requires high-quality waterproofing membrane (EPDM, TPO, or liquid-applied systems). Minimum falls of 1:80 for drainage. Lifespan: 25–40 years.

**2. Mono-Pitched Roof (Single Slope)**
One continuous slope — architecturally bold and sculptural. Excellent for contemporary and Scandinavian styles. The high wall created by the slope can accommodate clerestory windows for dramatic natural light. Standing seam zinc or Corten steel cladding suits this form beautifully.

**3. Hipped Roof**
Slopes down on all four sides. Classic, elegant, and aerodynamically efficient — excellent for hurricane or high-wind zones. Traditional materials: clay tiles, slate, or zinc. Used extensively in classic luxury residential architecture.

**4. Gabled Roof**
Simple triangular form with two slopes. The most structurally efficient pitched roof. Excellent for Scandinavian, colonial, and traditional styles. Natural ventilation through gable ends prevents moisture build-up in the roof space.

**Premium Roofing Materials:**
• Natural Welsh Slate: 150+ year lifespan, deeply prestigious. Cost: $50–$100/sqft
• Zinc Standing Seam: Develops beautiful blue-grey patina. Lifespan 80+ years. Cost: $40–$80/sqft
• Copper: Ultimate luxury, turns verdigris green over decades. Cost: $70–$120/sqft
• Terracotta Clay Tiles: Mediterranean and classical styles. Cost: $25–$60/sqft"""

    # Columns and classical
    elif any(w in p for w in ['column', 'pillar', 'classical', 'neoclassical', 'greek', 'roman', 'corinthian', 'ionic', 'doric', 'portico', 'mansion', 'rotunda', 'dome']):
        return """Expert guidance on classical architectural elements for luxury homes:

**The Five Classical Orders:**

**1. Doric (Simplest, Most Masculine)**
No base. Simple circular capital. Used for ground-floor colonnades and porticos where strength and solidity are desired. Appropriate for grand entrance gates and exterior colonnades.

**2. Ionic (Refined, Elegant)**
Scroll-shaped volute capitals. Slightly more slender than Doric. Ideal for secondary facades, interior pilasters, and library columns. The most versatile classical order.

**3. Corinthian (Most Elaborate, Most Prestigious)**
Acanthus leaf capital with extreme decorative richness. The order of choice for the grandest spaces — entrance halls, rotundas, and formal reception rooms. Columns typically 10 diameters in height.

**Rotunda Design:**
• Circular plan with a colonnaded ring of columns supporting a domed ceiling
• Dome can be coffered (like the Pantheon) or smooth with an oculus for dramatic natural light
• Marble or stone flooring in a radial or geometric pattern complements the circular plan
• A central chandelier or skylight at the apex creates a focal point

**Structural Considerations:**
Modern classical architecture uses reinforced concrete or steel structural frames with stone or GRC (Glass Reinforced Concrete) cladding for the classical details. This provides the visual richness of traditional masonry at a fraction of the weight and cost.

**Material Recommendations:**
• Columns: Solid limestone, polished granite, or GRC (Glass Reinforced Concrete) replicas
• Entablature: Cast stone or GRC
• Flooring: Book-matched Calacatta marble in geometric patterns
• Walls: Venetian plaster with stone pilasters"""

    # Smart home and technology
    elif any(w in p for w in ['smart', 'technology', 'automation', 'lighting', 'control', 'system', 'tech', 'home automation', 'av', 'security', 'camera']):
        return """A professional guide to smart home technology for luxury residences:

**Core Systems to Integrate:**

**1. Central Control Platform**
Crestron, Control4, or Lutron are the three industry-standard platforms for luxury homes. All lighting, AV, climate, security, and blinds are controlled from a single interface — iPad, wall panel, or voice.

**2. Lighting Control (Lutron RadioRA or Caseta)**
Scene-based lighting is transformative. Pre-programmed scenes for 'Morning', 'Dinner', 'Movie', 'Night' modes. Circadian rhythm lighting that automatically adjusts colour temperature throughout the day supports sleep health.

**3. Climate Control**
Zoned HVAC with individual room temperature control. Underfloor heating with smart thermostats (Nest or KNX-based). Schedule-based and occupancy-triggered operation reduces energy consumption by 30–40%.

**4. Security System**
• High-resolution IP cameras (4K) at all entry points and perimeter
• Facial recognition doorbell (Verkada or similar)
• Smart locks with PIN, card, and remote access
• Motion sensors with pet immunity
• 24/7 cloud-recorded footage with 30-day retention

**5. Audio-Visual**
Distributed audio to all rooms (Sonos or Control4 Audio). Hidden in-ceiling or in-wall speakers. Dedicated home cinema room with Dolby Atmos 7.1.4 surround sound.

**6. Window Treatment Automation**
Motorised roller blinds or curtains integrated with lighting scenes. Automated to close at sunset, open at sunrise.

**Budget Guideline:**
• Entry-level smart home: $25,000–$50,000
• Mid-range integrated system: $50,000–$150,000
• Full Crestron/Control4 luxury integration: $150,000–$500,000+"""

    # General / default
    else:
        return f"""As your expert AI Architect, here is my professional assessment regarding: "{prompt}"

**Foundational Design Principles:**

**1. Site Analysis First**
Before designing a single wall, conduct a thorough site analysis. Study:
• Sun path and shadow analysis (solar angles at summer and winter solstice)
• Prevailing wind direction and speed
• Views — both desirable (to preserve and frame) and undesirable (to screen)
• Topography and natural drainage patterns
• Soil conditions and bearing capacity

Architecture that responds intelligently to its site will always perform better thermally, look more natural, and feel more appropriate than a design that ignores its context.

**2. Hierarchy of Spaces**
Every successful luxury home has a clear spatial hierarchy:
• **Primary spaces** (living, dining, primary bedroom) — maximum light, best views, highest ceilings
• **Secondary spaces** (guest bedrooms, studies) — good light, comfortable scale
• **Service spaces** (utility, storage, plant rooms) — efficient and accessible but not prime real estate

**3. Material Integrity**
The most enduring architecture uses materials honestly and consistently. If concrete is structural, express it. If timber is load-bearing, let it show. Authentic material use creates timeless architecture that ages with dignity rather than looking dated.

**4. The 1% Rule for Details**
Spend 1% of your total construction budget on high-quality hardware — door handles, hinges, taps, light switches. These are the elements touched daily and form a lasting impression of quality. Premium hardware from Valli & Valli, FSB, or Dornbracht transforms the experience of every room.

**5. Future-Proofing**
Design for adaptability. Install conduit in walls for future technology upgrades. Design the primary bedroom suite to be accessible (wide doorways, accessible bathroom) from the beginning — it costs almost nothing now but is enormously expensive to retrofit later.

I would recommend consulting with a licensed architect in your region who can evaluate your specific site conditions, local planning regulations, and climate requirements for the most accurate and personalised recommendations."""


async def stream_ai_architect(prompt: str):
    """Stream the architectural response word by word for a realistic typing effect."""
    response_text = get_architectural_response(prompt)
    words = response_text.split(' ')
    for i, word in enumerate(words):
        text = word + (' ' if i < len(words) - 1 else '')
        yield f"data: {json.dumps({'text': text})}\n\n"
        # Small delay for natural streaming effect
        await asyncio.sleep(0.02)
    yield "data: [DONE]\n\n"


@router.get("/stream")
async def chat_stream(prompt: str):
    return StreamingResponse(
        stream_ai_architect(prompt),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
