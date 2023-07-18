from enum import Enum
from datetime import datetime

from pydantic import BaseModel, ConfigDict, UUID4, constr


class DiscountType(str, Enum):
    PERCENTAGE = 'percentage'
    FIXED_GENERAL_PUBLIC = 'fixed_general_public'
    FIXED_FIRST_PURCHASE = 'fixed_first_purchase'


class CouponBaseSchema(BaseModel):
    coupon_code: constr(min_length=6, max_length=6)
    expiration_date: datetime
    max_utilizations: int
    min_purchase_value: float
    discount_type: DiscountType
    discount_amount: float
    is_general_public: bool
    valid_first_purchase: bool

    model_config = ConfigDict(
        use_enum_values=True
    )


class CouponCreateSchema(CouponBaseSchema):
    pass


class CouponOutputSchema(CouponBaseSchema):
    id: UUID4

    model_config = ConfigDict(
        from_attributes=True
    )


class CouponConsumeSchema(BaseModel):
    coupon_code: constr(min_length=6, max_length=6)
    total_purchase_value: float
    is_first_purchase: bool


class CouponConsumeOutputSchema(BaseModel):
    discount_value: float
    coupon_code: str

    model_config = ConfigDict(
        from_attributes=True
    )
