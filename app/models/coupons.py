from uuid import uuid4 as uuid
from datetime import datetime

from sqlalchemy import (
    Column, Uuid, String, DateTime, SmallInteger, Numeric, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class Coupon(Base):
    __tablename__ = 'coupons'

    id = Column(Uuid, primary_key=True, default=uuid)
    coupon_code = Column(String(6), unique=True, nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    max_utilizations = Column(SmallInteger, nullable=False)
    min_purchase_value = Column(Numeric(10, 2), nullable=False)
    discount_type = Column(String(20), nullable=False)
    discount_amount = Column(Numeric(10, 2), nullable=False)
    is_general_public = Column(Boolean, nullable=False)
    valid_first_purchase = Column(Boolean, nullable=False)

    coupons_utilizations = relationship('CouponUtilization', back_populates='coupon')


class CouponUtilization(Base):
    __tablename__ = 'coupons_utilizations'
    
    id = Column(Uuid, primary_key=True, default=uuid)
    utilization_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    coupon_id = Column(Uuid, ForeignKey('coupons.id', ondelete='CASCADE'), nullable=False)

    coupon = relationship('Coupon', back_populates='coupons_utilizations')
