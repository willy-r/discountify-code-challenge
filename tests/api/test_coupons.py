from fastapi import status

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
