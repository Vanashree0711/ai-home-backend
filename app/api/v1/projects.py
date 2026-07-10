from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.session import get_db
from app.models.schema import Project, GeneratedImage, User
from app.core.security import decode_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/")
def get_user_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    projects = db.query(Project).filter(Project.user_id == current_user.id).order_by(desc(Project.created_at)).all()
    
    results = []
    for p in projects:
        images = db.query(GeneratedImage).filter(GeneratedImage.project_id == p.id).all()
        exterior = next((img.generated_url for img in images if "exterior" in img.style_prompt.lower()), None)
        interior = next((img.generated_url for img in images if "interior" in img.style_prompt.lower()), None)
        floorplan = next((img.generated_url for img in images if "floor plan" in img.style_prompt.lower()), None)
        
        from app.models.schema import PdfReport
        pdf = db.query(PdfReport).filter(PdfReport.project_id == p.id).first()
        pdf_path = pdf.report_url if pdf else None
        
        results.append({
            "id": str(p.id),
            "name": p.name,
            "description": p.description,
            "created_at": p.created_at,
            "exterior_image": exterior,
            "interior_image": interior,
            "floorplan_image": floorplan,
            "pdf_report": pdf_path
        })
        
    return results

@router.delete("/{project_id}")
def delete_project(project_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}
