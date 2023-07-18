from sqlalchemy.orm import Session

from app.api.schemas.coupons import CouponCreateSchema
from app.models.coupons import Coupon
from app.exceptions.custom_exceptions import CouponAlreadyExistsException


def create_coupon(session: Session, create_coupon_schema: CouponCreateSchema) -> Coupon:
    db_coupon = session.query(Coupon).filter_by(coupon_code=create_coupon_schema.coupon_code).first()

    if db_coupon is not None:
        raise CouponAlreadyExistsException(
            f'Coupon {create_coupon_schema.coupon_code} already exists'
        )

    new_coupon = Coupon(**create_coupon_schema.model_dump())
    session.add(new_coupon)
    session.commit()
    session.refresh(new_coupon)
    return new_coupon
