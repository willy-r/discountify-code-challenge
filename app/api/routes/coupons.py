from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_session
from app.api.schemas.coupons import CouponOutputSchema, CouponCreateSchema
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
    return coupons.create_coupon(session, coupon_create_schema)
