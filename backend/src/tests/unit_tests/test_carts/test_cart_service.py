import pytest

from src.carts.service import CartService


# @pytest.mark.skip("Very long test")
@pytest.mark.parametrize('user_id, product_id, product_name', [
	("a5d70116-9caa-4628-a4fd-d859c5f1f5be", "f38788b8-af6e-444e-a81f-ac6309b6b182", "string"),
	("a5d70116-9caa-4628-a4fd-d859c5f1f5be", "b01ff2d4-7c4d-4205-9adc-762ff5df38cf", "123"),
    ]
)
async def test_add_product_in_cart(user_id, product_id, product_name):
    test_cart = await CartService.add_product_in_cart(
		user_id=user_id,
        product_id=product_id
    )
    
    assert test_cart["details"].split(" ")[0] == product_name
    

# @pytest.mark.skip("Very long test")
@pytest.mark.parametrize('user_id, product_id, product_name', [
	("a5d70116-9caa-4628-a4fd-d859c5f1f5be", "f38788b8-af6e-444e-a81f-ac6309b6b182", "string"),
	("a5d70116-9caa-4628-a4fd-d859c5f1f5be", "b01ff2d4-7c4d-4205-9adc-762ff5df38cf", "123"),
    ]
)
async def test_remove_product_from_cart(user_id, product_id, product_name):
    test_cart = await CartService.remove_product_from_cart(
		user_id=user_id,
        product_id=product_id
    )
    
    assert test_cart["status"] == 200
