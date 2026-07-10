from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from app.db.session import get_db
from app.services.ai_service import AIEngineService
from app.services.storage import StorageService
from app.services.pdf_generator import PDFGenerator
from app.models.schema import Project, GeneratedImage, PdfReport, User
from app.api.v1.projects import get_current_user

from pydantic import BaseModel, Field

router = APIRouter()

class GenerationRequest(BaseModel):
    user_id: Optional[str] = None
    plot_size: int = Field(..., gt=0, description="Plot size must be greater than 0 sq ft")
    budget: int = Field(..., gt=0, description="Budget must be greater than 0")
    style: str = Field(..., min_length=1, description="Style cannot be empty")
    prompt: str = Field(..., min_length=1, description="Prompt cannot be empty")

@router.post("/generate")
async def generate_project(req: GenerationRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    The core autonomous endpoint.
    1. Generates Exterior/Interior concepts via OpenAI DALL-E.
    2. Generates Text Analysis via OpenAI GPT-4.
    3. Uploads temporary DALL-E URLs to Cloudinary for permanent storage.
    4. Generates PDF Report.
    5. Saves everything to DB.
    """
    try:
        # 1. Trigger Image Generation (Exterior, Interior, Floor Plan)
        image_urls = await AIEngineService.generate_images(req.prompt, req.style, req.budget, req.plot_size)
        
        # 2. Trigger Cost & Material Analysis (JSON)
        analysis_text = await AIEngineService.generate_cost_estimate(req.plot_size, req.budget, req.style, req.prompt)
        
        import json
        try:
            # The AI might wrap the JSON in markdown code blocks like ```json ... ```
            clean_text = analysis_text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.startswith("```"):
                clean_text = clean_text[3:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            analysis_data = json.loads(clean_text.strip())
        except Exception as e:
            # Fallback if the AI returned invalid JSON
            analysis_data = {
                "total_estimated_cost": f"${req.budget}",
                "cost_breakdown": analysis_text[:200] + "...",
                "recommended_materials": ["Concrete", "Glass", "Steel"],
                "sustainability_score": 85,
                "sustainability_tips": ["Install solar panels", "Use low-E glass windows"]
            }
        
        # 3. Permanent Storage (Mocked out if Cloudinary fails, it returns the raw url)
        safe_exterior_url = StorageService.upload_image_from_url(image_urls["exterior_url"])
        safe_interior_url = StorageService.upload_image_from_url(image_urls["interior_url"])
        safe_floorplan_url = StorageService.upload_image_from_url(image_urls.get("floorplan_url", ""))
        
        # 4. Generate PDF Report locally
        import time
        unique_id = int(time.time())
        pdf_filename = f"report_{req.plot_size}_{unique_id}.pdf"
        
        pdf_data = {
            "style": req.style,
            "plot_size": req.plot_size,
            "budget": req.budget,
            "estimated_cost": analysis_data.get("total_estimated_cost", f"${req.budget}"),
            "sustainability_score": analysis_data.get("sustainability_score", 85),
            "cost_breakdown": analysis_data.get("cost_breakdown", ""),
            "materials": analysis_data.get("recommended_materials", []),
            "sustainability_tips": analysis_data.get("sustainability_tips", []),
            "exterior_image": safe_exterior_url,
            "interior_image": safe_interior_url,
            "floorplan_image": safe_floorplan_url
        }
        # 4. Generate PDF Report synchronously so it's ready before returning response
        PDFGenerator.generate_report("proj_" + str(req.plot_size), pdf_data, pdf_filename)
        
        # 5. Save to Database
        new_project = Project(
            user_id=current_user.id,
            name=f"{req.style} Home - {req.plot_size} sqft",
            description=req.prompt
        )
        db.add(new_project)
        db.commit()
        db.refresh(new_project)

        img1 = GeneratedImage(project_id=new_project.id, generated_url=safe_exterior_url, style_prompt="exterior")
        img2 = GeneratedImage(project_id=new_project.id, generated_url=safe_interior_url, style_prompt="interior")
        img3 = GeneratedImage(project_id=new_project.id, generated_url=safe_floorplan_url, style_prompt="floor plan")
        db.add_all([img1, img2, img3])

        new_pdf = PdfReport(project_id=new_project.id, report_url=pdf_filename)
        db.add(new_pdf)
        
        db.commit()

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
