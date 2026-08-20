from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from app.services.ai_service import AIEngineService
from app.services.storage import StorageService
from app.services.pdf_generator import PDFGenerator

router = APIRouter()

class GenerationRequest(BaseModel):
    plot_size: int = Field(..., gt=0, description="Plot size must be greater than 0 sq ft")
    budget: int = Field(..., gt=0, description="Budget must be greater than 0")
    style: str = Field(..., min_length=1, description="Style cannot be empty")
    prompt: str = Field(..., min_length=1, description="Prompt cannot be empty")

@router.post("/generate")
async def generate_project(req: GenerationRequest, background_tasks: BackgroundTasks):
    """
    Core generation endpoint — no login required.
    Generates images and cost estimate and returns results.
    Projects are saved on the client device via localStorage.
    """
    try:
        # 1. Generate Images from user prompt using free Pollinations API
        image_urls = await AIEngineService.generate_images(req.prompt, req.style, req.budget, req.plot_size)

        # 2. Generate Cost & Material Analysis
        analysis_text = await AIEngineService.generate_cost_estimate(req.plot_size, req.budget, req.style, req.prompt)

        import json
        try:
            clean_text = analysis_text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.startswith("```"):
                clean_text = clean_text[3:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            analysis_data = json.loads(clean_text.strip())
        except Exception:
            analysis_data = {
                "total_estimated_cost": f"${req.budget:,}",
                "cost_breakdown": "Foundation & Structure: 30%, Exterior & Roofing: 20%, Interior Finishes: 25%, MEP: 15%, Landscaping: 10%",
                "recommended_materials": ["Reinforced Concrete", "Low-E Double Glazed Glass", "Recycled Steel Beams", "Sustainable Hardwood Timber", "Natural Stone Cladding"],
                "sustainability_score": 85,
                "sustainability_tips": ["Install rooftop solar panels", "Use low-E glass windows", "Integrate rainwater harvesting"]
            }

        # 3. Storage (Cloudinary or raw URL fallback)
        safe_exterior_url = StorageService.upload_image_from_url(image_urls["exterior_url"])
        safe_interior_url = StorageService.upload_image_from_url(image_urls["interior_url"])
        safe_floorplan_url = StorageService.upload_image_from_url(image_urls.get("floorplan_url", ""))

        # 4. Generate PDF in background
        import time
        unique_id = int(time.time())
        pdf_filename = f"report_{req.plot_size}_{unique_id}.pdf"
        pdf_data = {
            "style": req.style,
            "plot_size": req.plot_size,
            "budget": req.budget,
            "estimated_cost": analysis_data.get("total_estimated_cost", f"${req.budget:,}"),
            "sustainability_score": analysis_data.get("sustainability_score", 85),
            "cost_breakdown": analysis_data.get("cost_breakdown", ""),
            "materials": analysis_data.get("recommended_materials", []),
            "sustainability_tips": analysis_data.get("sustainability_tips", []),
            "exterior_image": safe_exterior_url,
            "interior_image": safe_interior_url,
            "floorplan_image": safe_floorplan_url
        }
        background_tasks.add_task(PDFGenerator.generate_report, "proj_" + str(req.plot_size), pdf_data, pdf_filename)

        return {
            "status": "success",
            "exterior_image": safe_exterior_url,
            "interior_image": safe_interior_url,
            "floorplan_image": safe_floorplan_url,
            "analysis": analysis_data,
            "pdf_report": pdf_filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation Engine Error: {str(e)}")
