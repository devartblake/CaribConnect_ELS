import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.models import Theme
from app.schemas.themeSchema import ThemeCreate, ThemeUpdate, ThemeRead
from app.api.deps import get_db

router = APIRouter()

# Create a new theme
@router.post("/", response_model=ThemeRead)
async def create_theme(theme: ThemeCreate, db: Session = Depends(get_db)):
    db_theme = Theme(**theme.dict())
    db.add(db_theme)
    db.commit()
    db.refresh(db_theme)
    return db_theme

# Get all themes
@router.get("/", response_model=list[ThemeRead])
async def get_all_themes(session: Session = Depends(get_db)):
    themes = session.query(Theme).all()
    return themes

# Get theme by ID
@router.get("/{theme_id}", response_model=ThemeRead)
async def get_theme(theme_id: uuid.UUID, db: Session = Depends(get_db)):
    db_theme = db.query(Theme).filter(Theme.id == theme_id).first()
    if db_theme is None:
        raise HTTPException(status_code=404, detail="Theme not found")
    return db_theme

# Update theme by ID
@router.put("/{theme_id}", response_model=ThemeRead)
async def update_theme(theme_id: uuid.UUID, theme: ThemeUpdate, db: Session = Depends(get_db)):
    db_theme = db.query(Theme).filter(Theme.id == theme_id).first()
    if db_theme is None:
        raise HTTPException(status_code=404, detail="Theme not found")
    for key, value in theme.dict(exclude_unset=True).items():
        setattr(db_theme, key, value)
    db.commit()
    db.refresh(db_theme)
    return db_theme

# Delete theme by ID
@router.delete("/{theme_id}")
async def delete_theme(theme_id: uuid.UUID, db: Session = Depends(get_db)):
    db_theme = db.query(Theme).filter(Theme.id == theme_id).first()
    if db_theme is None:
        raise HTTPException(status_code=404, detail="Theme not found")
    db.delete(db_theme)
    db.commit()
    return {"detail": "Theme deleted"}
