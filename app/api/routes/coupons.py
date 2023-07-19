from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_session
from app.exceptions.custom_exceptions import (
    CouponAlreadyExistsException, CouponNotFoundException,
    CouponRulesException
)
from app.api.schemas.coupons import (
    CouponOutputSchema, CouponCreateSchema,
    CouponConsumeSchema, CouponConsumeOutputSchema
)
from app.services import coupons

router = APIRouter(prefix='/coupons', tags=['coupons'])


@router.post(
    '/',
    response_model=CouponOutputSchema,
    status_code=status.HTTP_201_CREATED
)
def create_coupon(
    coupon_create_schema: CouponCreateSchema,
    session: Session = Depends(get_session)
):
    try:
        return coupons.create_coupon(session, coupon_create_schema)
    except CouponAlreadyExistsException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )


@router.post(
    '/consume',
    response_model=CouponConsumeOutputSchema,
    status_code=status.HTTP_201_CREATED,
)
def consume_coupon(
    coupon_consume_schema: CouponConsumeSchema,
    session: Session = Depends(get_session)
):
    try:
        return coupons.consume_coupon(session, coupon_consume_schema)
    except CouponNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except Exception as exc:
        if isinstance(exc, CouponRulesException):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc)
            )
