from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.dependencies import get_db
from app.review.repository import ReviewRepository
from app.review.service import ReviewService


async def get_review_repository(
    session: AsyncSession = Depends(
        get_db,
    ),
) -> ReviewRepository:
    return ReviewRepository(
        session,
    )


async def get_review_service(
    repository: ReviewRepository = Depends(
        get_review_repository,
    ),
    session: AsyncSession = Depends(
        get_db,
    ),
) -> ReviewService:
    return ReviewService(
        repository=repository,
        session=session,
    )
