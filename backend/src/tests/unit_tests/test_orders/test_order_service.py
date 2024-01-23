import pytest

from src.orders.models import OrderModel
from src.orders.service import OrderService


class TestOrder:
    
    # @pytest.mark.skip("Very long test")
    @pytest.mark.parametrize('user_id, promocode', [
        # ("a5d70116-9caa-4628-a4fd-d859c5f1f5be", "qwerty"),
        ("a5d70116-9caa-4628-a4fd-d859c5f1f5be", None),
        ]
    )
    async def test_create_new_order(self, user_id, promocode):
        test_order = await OrderService.create_new_order(
            user_id=user_id,
            promocode=promocode
        )

        assert isinstance(test_order[0], OrderModel) == True
        self.order_id = test_order[0].id


    @pytest.mark.parametrize('order_id', [
        # ("a5d70116-9caa-4628-a4fd-d859c5f1f5be", "qwerty"),
        ("2bb7165b-76c5-4417-bdf4-c71dd75a31a0"),
        ]
    )
    async def test_add_products_in_order(self, order_id):
        test_order = await OrderService.add_products_in_order(
            product_dict={
                'f38788b8-af6e-444e-a81f-ac6309b6b182': 1, 
                'b01ff2d4-7c4d-4205-9adc-762ff5df38cf': 1
                },
            order_id=order_id

        )

        assert test_order["status"] == 200
        