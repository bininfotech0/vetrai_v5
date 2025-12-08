"""
API routes for Themes Service
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from shared.utils import get_db
from shared.middleware import CurrentUser, get_current_user, require_org_admin
from shared.config import get_settings

from .models import Theme
from .schemas import ThemeUpdate, ThemeResponse, MessageResponse

router = APIRouter()
settings = get_settings()


@router.get("/themes/{org_id}", response_model=ThemeResponse)
async def get_theme(
    org_id: int,
    db: Session = Depends(get_db)
):
    """Get organization theme (public endpoint)"""
    theme = db.query(Theme).filter(
        Theme.organization_id == org_id,
        Theme.is_active == True
    ).first()
    
    if not theme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Theme not found"
        )
    
    return theme


@router.put("/themes/{org_id}", response_model=ThemeResponse)
async def update_theme(
    org_id: int,
    theme_update: ThemeUpdate,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """Update theme settings"""
    if current_user.organization_id != org_id and not current_user.is_super_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    theme = db.query(Theme).filter(Theme.organization_id == org_id).first()
    
    if not theme:
        # Create new theme
        theme = Theme(
            organization_id=org_id,
            name=theme_update.name or "Default Theme"
        )
        db.add(theme)
    
    # Update fields
    if theme_update.name is not None:
        theme.name = theme_update.name
    if theme_update.primary_color is not None:
        theme.primary_color = theme_update.primary_color
    if theme_update.secondary_color is not None:
        theme.secondary_color = theme_update.secondary_color
    if theme_update.accent_color is not None:
        theme.accent_color = theme_update.accent_color
    if theme_update.custom_css is not None:
        theme.custom_css = theme_update.custom_css
    if theme_update.custom_js is not None:
        theme.custom_js = theme_update.custom_js
    
    db.commit()
    db.refresh(theme)
    
    return theme


@router.post("/themes/{org_id}/logo", response_model=MessageResponse)
async def upload_logo(
    org_id: int,
    file: UploadFile = File(...),
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """Upload organization logo"""
    if current_user.organization_id != org_id and not current_user.is_super_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Placeholder - MinIO upload
    return {"message": f"Logo {file.filename} uploaded successfully"}


@router.get("/themes/{org_id}/css")
async def generate_css(
    org_id: int,
    db: Session = Depends(get_db)
):
    """Generate CSS for theme"""
    theme = db.query(Theme).filter(
        Theme.organization_id == org_id,
        Theme.is_active == True
    ).first()
    
    if not theme:
        return ""
    
    # Generate CSS from theme settings
    css = f"""
    :root {{
        --primary-color: {theme.primary_color or '#3b82f6'};
        --secondary-color: {theme.secondary_color or '#64748b'};
        --accent-color: {theme.accent_color or '#f59e0b'};
    }}
    {theme.custom_css or ''}
    """
    
    return css
