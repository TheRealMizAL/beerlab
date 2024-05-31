from typing import Annotated

from core.schemas.reviews import ReviewFullModel, ReviewMinModel
from fastapi import APIRouter, Path, Response, HTTPException, status
from tortoise.transactions import in_transaction
from core.db.models import Review
from core.schemas.errors import BadReviewError

review_router = APIRouter(prefix='/review',
                          tags=['Review'])


@review_router.get('/{review_id}',
                   responses={200: {'model': ReviewFullModel},
                              404: {'model': BadReviewError}})
async def get_review(review_id: Annotated[int, Path()]) -> ReviewFullModel:
    async with in_transaction() as connection:
        if review := await Review.get_or_none(id=review_id, using_db=connection):
            return review
        raise HTTPException(status.HTTP_404_NOT_FOUND, BadReviewError)


@review_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_review(response: Response, review: ReviewMinModel) -> ReviewFullModel:
    async with in_transaction() as connection:
        review = review.dict(exclude_unset=True)
        review_db = await Review.create(**review, using_db=connection)
    response.status_code = status.HTTP_201_CREATED
    return review_db


@review_router.put('/{review_id}',
                   responses={200: {'model': ReviewFullModel},
                              201: {'model': ReviewFullModel}})
async def change_review(response: Response, review_id: Annotated[int, Path()], review: ReviewMinModel):
    async with in_transaction() as connection:
        review_created = await Review.update_or_create(defaults=review.dict(), id=review_id, using_db=connection)
        if review_created[1]:
            response.status_code = status.HTTP_201_CREATED
        else:
            response.status_code = status.HTTP_200_OK
        return review_created[0]


@review_router.patch('/{review_id}',
                     responses={200: {'model': ReviewFullModel},
                                404: {'model': BadReviewError}})
async def edit_review(response: Response, review_id: Annotated[int, Path()], review: ReviewMinModel):
    async with in_transaction() as connection:
        if review_db := await Review.get_or_none(id=review_id, using_db=connection):
            await review_db.update_from_dict(review.dict(exclude_unset=True))
            await review_db.save(using_db=connection)
            response.status_code = status.HTTP_200_OK
            return review_db
        raise HTTPException(status.HTTP_404_NOT_FOUND, BadReviewError)


@review_router.delete('/{review_id}',
                      responses={204: {'model': None},
                                 404: {'model': BadReviewError}})
async def delete_review(response: Response, review_id: Annotated[int, Path()]):
    async with in_transaction() as connection:
        if review := await Review.get_or_none(id=review_id, using_db=connection):
            await review.delete(using_db=connection)
            response.status_code = status.HTTP_204_NO_CONTENT
            return
        raise HTTPException(status.HTTP_404_NOT_FOUND, BadReviewError)
