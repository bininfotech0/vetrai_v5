"""
API routes for Themes Service
"""
import sys
from pathlib import Path
from typing import List

sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from shared.utils import get_db
from shared.middleware import CurrentUser, get_current_user, require_org_admin
from shared.config import get_settings

from models import Theme, PublicPage
from schemas import (
    ThemeCreate,
    ThemeUpdate,
    ThemeResponse,
    PublicPageCreate,
    PublicPageUpdate,
    PublicPageResponse,
    MessageResponse,
)

router = APIRouter()
settings = get_settings()


@router.post("/", response_model=ThemeResponse, status_code=status.HTTP_201_CREATED)
async def create_theme(
    theme_data: ThemeCreate,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """Create or update organization theme"""
    
    # Check if theme already exists
    existing = db.query(Theme).filter(
        Theme.organization_id == current_user.organization_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Theme already exists. Use PUT to update."
        )
    
    theme = Theme(
        organization_id=current_user.organization_id,
        name=theme_data.name,
        primary_color=theme_data.primary_color,
        secondary_color=theme_data.secondary_color,
        accent_color=theme_data.accent_color,
        custom_css=theme_data.custom_css,
        settings=theme_data.settings
    )
    
    db.add(theme)
    db.commit()
    db.refresh(theme)
    
    return theme


@router.get("/", response_model=ThemeResponse)
async def get_theme(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get organization theme"""
    
    theme = db.query(Theme).filter(
        Theme.organization_id == current_user.organization_id
    ).first()
    
    if not theme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Theme not found"
        )
    
    return theme


@router.put("/", response_model=ThemeResponse)
async def update_theme(
    theme_update: ThemeUpdate,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """Update organization theme"""
    
    theme = db.query(Theme).filter(
        Theme.organization_id == current_user.organization_id
    ).first()
    
    if not theme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Theme not found"
        )
    
    # Update fields
    if theme_update.name is not None:
        theme.name = theme_update.name
    if theme_update.primary_color is not None:
        theme.primary_color = theme_update.primary_color
    if theme_update.secondary_color is not None:
        theme.secondary_color = theme_update.secondary_color
    if theme_update.accent_color is not None:
        theme.accent_color = theme_update.accent_color
    if theme_update.logo_url is not None:
        theme.logo_url = theme_update.logo_url
    if theme_update.favicon_url is not None:
        theme.favicon_url = theme_update.favicon_url
    if theme_update.custom_css is not None:
        theme.custom_css = theme_update.custom_css
    if theme_update.settings is not None:
        theme.settings = theme_update.settings
    if theme_update.is_active is not None:
        theme.is_active = theme_update.is_active
    
    db.commit()
    db.refresh(theme)
    
    return theme


@router.post("/pages", response_model=PublicPageResponse, status_code=status.HTTP_201_CREATED)
async def create_page(
    page_data: PublicPageCreate,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """Create a public page"""
    
    # Check if slug already exists for this organization
    existing = db.query(PublicPage).filter(
        PublicPage.organization_id == current_user.organization_id,
        PublicPage.slug == page_data.slug
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page with this slug already exists"
        )
    
    page = PublicPage(
        organization_id=current_user.organization_id,
        slug=page_data.slug,
        title=page_data.title,
        content=page_data.content
    )
    
    db.add(page)
    db.commit()
    db.refresh(page)
    
    return page


@router.get("/pages", response_model=List[PublicPageResponse])
async def list_pages(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List public pages for organization"""
    
    pages = db.query(PublicPage).filter(
        PublicPage.organization_id == current_user.organization_id
    ).all()
    
    return pages


@router.get("/pages/{slug}", response_model=PublicPageResponse)
async def get_page(
    slug: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get public page by slug"""
    
    page = db.query(PublicPage).filter(
        PublicPage.organization_id == current_user.organization_id,
        PublicPage.slug == slug
    ).first()
    
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found"
        )
    
    return page


@router.put("/pages/{slug}", response_model=PublicPageResponse)
async def update_page(
    slug: str,
    page_update: PublicPageUpdate,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """Update public page"""
    
    page = db.query(PublicPage).filter(
        PublicPage.organization_id == current_user.organization_id,
        PublicPage.slug == slug
    ).first()
    
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found"
        )
    
    # Update fields
    if page_update.title is not None:
        page.title = page_update.title
    if page_update.content is not None:
        page.content = page_update.content
    if page_update.is_published is not None:
        page.is_published = page_update.is_published
    
    db.commit()
    db.refresh(page)
    
    return page


@router.delete("/pages/{slug}", response_model=MessageResponse)
async def delete_page(
    slug: str,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """Delete public page"""
    
    page = db.query(PublicPage).filter(
        PublicPage.organization_id == current_user.organization_id,
        PublicPage.slug == slug
    ).first()
    
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found"
        )
    
    db.delete(page)
    db.commit()
    
    return {"message": "Page deleted successfully"}
