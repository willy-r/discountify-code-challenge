from datetime import datetime, timedelta
from decimal import Decimal

from app.models.coupons import Coupon, CouponUtilization


def test_create_coupon_on_database(test_session):
    new_coupon = Coupon(
        coupon_code='HFKL4Y',
        expiration_date=datetime.utcnow() + timedelta(days=7),
        max_utilizations=500,
        min_purchase_value=Decimal(100),
        discount_type='percentage',
        discount_amount=Decimal(5),
        is_general_public=True,
        valid_first_purchase=False
    )
    test_session.add(new_coupon)
    test_session.commit()
    test_session.refresh(new_coupon)
    
    coupon = test_session.query(
        Coupon
    ).filter_by(
        coupon_code=new_coupon.coupon_code
    ).first()

    assert coupon.coupon_code == 'HFKL4Y'


def test_create_coupon_utilization_on_database(test_session):
    new_coupon = Coupon(
        coupon_code='HFKL4Y',
        expiration_date=datetime.utcnow() + timedelta(days=7),
        max_utilizations=500,
        min_purchase_value=Decimal(100),
        discount_type='percentage',
        discount_amount=Decimal(5),
        is_general_public=True,
        valid_first_purchase=False
    )
    test_session.add(new_coupon)
    test_session.commit()
    test_session.refresh(new_coupon)
    new_coupon_utilization = CouponUtilization(
        coupon_id=new_coupon.id,
    )
    test_session.add(new_coupon_utilization)
    test_session.commit()
    test_session.refresh(new_coupon_utilization)
    
    coupon_utilization = test_session.query(
        CouponUtilization
    ).filter_by(
        id=new_coupon_utilization.id
    ).first()

    assert coupon_utilization.coupon_id == new_coupon.id
    assert coupon_utilization.coupon.coupon_code == 'HFKL4Y'
