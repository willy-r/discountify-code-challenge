from typing import Any
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session

from app.api.schemas.coupons import (
    CouponCreateSchema, CouponConsumeSchema,
    DiscountType
)
from app.exceptions.custom_exceptions import (
    CouponAlreadyExistsException, CouponNotFoundException,
    CouponExpiredException, CouponMaxUtilizationsExceededException,
    CouponMinPurchaseValueExceededException, CouponFirstPurchaseException
)
from app.models.coupons import Coupon, CouponUtilization


def create_coupon(session: Session, create_coupon_schema: CouponCreateSchema) -> Coupon:
    db_coupon = session.query(Coupon).filter_by(coupon_code=create_coupon_schema.coupon_code).first()

    if db_coupon is not None:
        raise CouponAlreadyExistsException(
            f'Coupon {db_coupon.coupon_code} already exists'
        )

    new_coupon = Coupon(**create_coupon_schema.model_dump())
    session.add(new_coupon)
    session.commit()
    session.refresh(new_coupon)

    return new_coupon


def consume_coupon(session: Session, coupon_consume_schema: CouponConsumeSchema) -> dict[str, Any]:
    db_coupon = session.query(Coupon).filter_by(coupon_code=coupon_consume_schema.coupon_code).first()

    if db_coupon is None:
        raise CouponNotFoundException(
            f'Coupon {coupon_consume_schema.coupon_code} was not found'
        )

    if not is_coupon_expired(db_coupon.expiration_date):
        raise CouponExpiredException(
            f'Coupon {db_coupon.coupon_code} was expired on {db_coupon.expiration_date}'
        )
    
    if not is_max_utilizations_exceeded(session, db_coupon.id, db_coupon.max_utilizations):
        raise CouponMaxUtilizationsExceededException(
            f'Coupon {db_coupon.coupon_code} max utilizations of {db_coupon.max_utilizations} exceeded'
        )
    
    if not is_min_purchase_value_exceeded(db_coupon.min_purchase_value, coupon_consume_schema.total_purchase_value):
        raise CouponMinPurchaseValueExceededException(
            f'Coupon {db_coupon.coupon_code} accepts only purchase less than {db_coupon.min_purchase_value}'
        )
    
    discount_value = apply_discount(
        discount_type=db_coupon.discount_type,
        discount_amount=float(db_coupon.discount_amount),
        is_first_purchase=coupon_consume_schema.is_first_purchase,
        total_purchase_value=coupon_consume_schema.total_purchase_value,
    )
    new_coupon_utilization = CouponUtilization(
        coupon_id=db_coupon.id,
    )
    session.add(new_coupon_utilization)
    session.commit()
    session.refresh(new_coupon_utilization)

    return {
        'discount_value': discount_value,
        'coupon_code': db_coupon.coupon_code,
    }


def is_coupon_expired(expiration_date: datetime) -> bool:
    utilization_date = datetime.utcnow()
    return utilization_date < expiration_date


def is_max_utilizations_exceeded(session: Session, coupon_id: UUID, max_utilizations: int) -> bool:
    coupons_utilizations = session.query(CouponUtilization).filter_by(coupon_id=coupon_id).count()
    return coupons_utilizations < max_utilizations


def is_min_purchase_value_exceeded(min_purchase_value: float, total_purchase_value: float) -> bool:
    return total_purchase_value < min_purchase_value


def apply_discount(
    discount_type: DiscountType,
    total_purchase_value: float,
    discount_amount: float,
    is_first_purchase: bool,
) -> float:
    if discount_type == DiscountType.PERCENTAGE:
        return total_purchase_value * (1 - (discount_amount / 100))
    elif discount_type == DiscountType.FIXED_GENERAL_PUBLIC:
        return total_purchase_value - discount_amount
    elif discount_type == DiscountType.FIXED_FIRST_PURCHASE:
        if not is_first_purchase:
            raise CouponFirstPurchaseException(
                f'Discount type [{discount_type}] is only for first purchase'
            )
        return total_purchase_value - discount_amount
