from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from app.api.deps import get_db
from app.models import PageView

router = APIRouter()

@router.post("/track-page-view/")
async def track_page_view(page_url: str, request: Request, db: Session = Depends(get_db)):
    user_agent = request.headers.get('user-agent')
    ip_address = request.client.host
    user_id = request.state.user_id  # Assuming user_id is extracted from a token

    # Create a new PageView record
    page_view = PageView(
        user_id=user_id,
        page_url=page_url,
        user_agent=user_agent,
        ip_address=ip_address
    )

    db.add(page_view)
    db.commit()

    return {"message": "Page view tracked successfully"}
