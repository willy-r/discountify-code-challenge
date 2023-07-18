import re
from uuid import UUID

from freezegun import freeze_time
from fastapi import status

from app.models.coupons import CouponUtilization

ENDPOINT = '/coupons'


def test_create_coupon_should_return_201(test_client):
    response = test_client.post(
        ENDPOINT,
        json={
            'coupon_code': 'ABCOI1',
            'expiration_date': '2023-07-19T18:39:41.971Z',
            'max_utilizations': 100,
            'min_purchase_value': 100,
            'discount_type': 'percentage',
            'discount_amount': 30,
            'is_general_public': True,
            'valid_first_purchase': False,
        }
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_already_existing_coupon_should_return_409(test_client):
    response = test_client.post(
        ENDPOINT,
        json={
            'coupon_code': 'ABCOI1',
            'expiration_date': '2023-07-19T18:39:41.971Z',
            'max_utilizations': 100,
            'min_purchase_value': 100,
            'discount_type': 'percentage',
            'discount_amount': 30,
            'is_general_public': True,
            'valid_first_purchase': False,
        }
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = test_client.post(
        ENDPOINT,
        json={
            'coupon_code': 'ABCOI1',
            'expiration_date': '2023-07-19T18:39:41.971Z',
            'max_utilizations': 100,
            'min_purchase_value': 100,
            'discount_type': 'percentage',
            'discount_amount': 30,
            'is_general_public': True,
            'valid_first_purchase': False,
        }
    )
    assert response.status_code == status.HTTP_409_CONFLICT


def test_consume_valid_percentage_coupon_should_return_201(test_client):
    response = test_client.post(
        ENDPOINT,
        json={
            'coupon_code': 'ABCOI1',
            'expiration_date': '2023-07-18T18:00:00Z',
            'max_utilizations': 100,
            'min_purchase_value': 100,
            'discount_type': 'percentage',
            'discount_amount': 30,
            'is_general_public': True,
            'valid_first_purchase': False,
        }
    )
    assert response.status_code == status.HTTP_201_CREATED

    with freeze_time('2023-07-18 17:59:59'):
        response = test_client.post(
            f'{ENDPOINT}/consume',
            json={
                'coupon_code': 'ABCOI1',
                'total_purchase_value': 99,
                'is_first_purchase': False,
            }
        )
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'discount_value': 69.3, 'coupon_code': 'ABCOI1'}


def test_consume_valid_fixed_general_public_coupon_should_return_201(test_client):
    response = test_client.post(
        ENDPOINT,
        json={
            'coupon_code': 'ABCOI1',
            'expiration_date': '2023-07-18T18:00:00Z',
            'max_utilizations': 100,
            'min_purchase_value': 100,
            'discount_type': 'fixed_general_public',
            'discount_amount': 10,
            'is_general_public': True,
            'valid_first_purchase': False,
        }
    )
    assert response.status_code == status.HTTP_201_CREATED

    with freeze_time('2023-07-18 17:59:59'):
        response = test_client.post(
            f'{ENDPOINT}/consume',
            json={
                'coupon_code': 'ABCOI1',
                'total_purchase_value': 99,
                'is_first_purchase': False,
            }
        )
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'discount_value': 89, 'coupon_code': 'ABCOI1'}


def test_consume_valid_fixed_first_purchase_coupon_should_return_201(test_client):
    response = test_client.post(
        ENDPOINT,
        json={
            'coupon_code': 'ABCOI1',
            'expiration_date': '2023-07-18T18:00:00Z',
            'max_utilizations': 100,
            'min_purchase_value': 100,
            'discount_type': 'fixed_first_purchase',
            'discount_amount': 10,
            'is_general_public': True,
            'valid_first_purchase': True,
        }
    )
    assert response.status_code == status.HTTP_201_CREATED

    with freeze_time('2023-07-18 17:59:59'):
        response = test_client.post(
            f'{ENDPOINT}/consume',
            json={
                'coupon_code': 'ABCOI1',
                'total_purchase_value': 99,
                'is_first_purchase': True,
            }
        )
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'discount_value': 89, 'coupon_code': 'ABCOI1'}


def test_consume_valid_fixed_first_purchase_coupon_not_first_purchase_should_return_400(test_client):
    response = test_client.post(
        ENDPOINT,
        json={
            'coupon_code': 'ABCOI1',
            'expiration_date': '2023-07-18T18:00:00Z',
            'max_utilizations': 100,
            'min_purchase_value': 100,
            'discount_type': 'fixed_first_purchase',
            'discount_amount': 10,
            'is_general_public': True,
            'valid_first_purchase': True,
        }
    )
    assert response.status_code == status.HTTP_201_CREATED

    with freeze_time('2023-07-18 17:59:59'):
        response = test_client.post(
            f'{ENDPOINT}/consume',
            json={
                'coupon_code': 'ABCOI1',
                'total_purchase_value': 99,
                'is_first_purchase': False,
            }
        )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert re.search(r'only accepted on first purchase', response.json()['detail']) is not None


def test_consume_non_existing_coupon_should_return_404(test_client):
    response = test_client.post(
        f'{ENDPOINT}/consume',
        json={
            'coupon_code': 'ABCOI1',
            'total_purchase_value': 100,
            'is_first_purchase': False,
        }
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_consume_max_utilizations_exceeded_coupon_should_return_400(test_client, test_session):
    response = test_client.post(
        ENDPOINT,
        json={
            'coupon_code': 'ABCOI1',
            'expiration_date': '2023-07-18T18:00:00Z',
            'max_utilizations': 1,
            'min_purchase_value': 100,
            'discount_type': 'percentage',
            'discount_amount': 30,
            'is_general_public': True,
            'valid_first_purchase': False,
        }
    )
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    new_coupon_utilization = CouponUtilization(
        coupon_id=UUID(data['id']),
    )
    test_session.add(new_coupon_utilization)
    test_session.commit()
    test_session.refresh(new_coupon_utilization)

    with freeze_time('2023-07-18 17:59:59'):
        response = test_client.post(
            f'{ENDPOINT}/consume',
            json={
                'coupon_code': 'ABCOI1',
                'total_purchase_value': 99,
                'is_first_purchase': False,
            }
        )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert re.search(r'ABCOI1 max utilizations', response.json()['detail']) is not None


def test_consume_expired_coupon_should_return_400(test_client):
    response = test_client.post(
        ENDPOINT,
        json={
            'coupon_code': 'ABCOI1',
            'expiration_date': '2023-07-18T18:00:00Z',
            'max_utilizations': 100,
            'min_purchase_value': 100,
            'discount_type': 'percentage',
            'discount_amount': 30,
            'is_general_public': True,
            'valid_first_purchase': False,
        }
    )
    assert response.status_code == status.HTTP_201_CREATED

    with freeze_time('2023-07-18 18:01:00'):
        response = test_client.post(
            f'{ENDPOINT}/consume',
            json={
                'coupon_code': 'ABCOI1',
                'total_purchase_value': 99,
                'is_first_purchase': False,
            }
        )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert re.search(r'ABCOI1 expired', response.json()['detail']) is not None


def test_consume_max_utilizations_exceeded_coupon_should_return_400(test_client, test_session):
    response = test_client.post(
        ENDPOINT,
        json={
            'coupon_code': 'ABCOI1',
            'expiration_date': '2023-07-18T18:00:00Z',
            'max_utilizations': 1,
            'min_purchase_value': 100,
            'discount_type': 'percentage',
            'discount_amount': 30,
            'is_general_public': True,
            'valid_first_purchase': False,
        }
    )
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    new_coupon_utilization = CouponUtilization(
        coupon_id=UUID(data['id']),
    )
    test_session.add(new_coupon_utilization)
    test_session.commit()
    test_session.refresh(new_coupon_utilization)

    with freeze_time('2023-07-18 17:59:59'):
        response = test_client.post(
            f'{ENDPOINT}/consume',
            json={
                'coupon_code': 'ABCOI1',
                'total_purchase_value': 99,
                'is_first_purchase': False,
            }
        )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert re.search(r'ABCOI1 max utilizations', response.json()['detail']) is not None


def test_consume_min_purchase_value_coupon_should_return_400(test_client, test_session):
    response = test_client.post(
        ENDPOINT,
        json={
            'coupon_code': 'ABCOI1',
            'expiration_date': '2023-07-18T18:00:00Z',
            'max_utilizations': 100,
            'min_purchase_value': 100,
            'discount_type': 'percentage',
            'discount_amount': 30,
            'is_general_public': True,
            'valid_first_purchase': False,
        }
    )
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    new_coupon_utilization = CouponUtilization(
        coupon_id=UUID(data['id']),
    )
    test_session.add(new_coupon_utilization)
    test_session.commit()
    test_session.refresh(new_coupon_utilization)

    with freeze_time('2023-07-18 17:59:59'):
        response = test_client.post(
            f'{ENDPOINT}/consume',
            json={
                'coupon_code': 'ABCOI1',
                'total_purchase_value': 101,
                'is_first_purchase': False,
            }
        )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert re.search(r'less than 100', response.json()['detail']) is not None
