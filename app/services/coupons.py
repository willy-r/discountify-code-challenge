from sqlalchemy.orm import Session

from app.api.schemas.coupons import CouponCreateSchema
from app.models.coupons import Coupon


def create_coupon(session: Session, create_coupon_schema: CouponCreateSchema) -> Coupon:
    new_coupon = Coupon(**create_coupon_schema.model_dump())
    session.add(new_coupon)
    session.commit()
    session.refresh(new_coupon)
    return new_coupon
