def count_total_discount_and_payment_amount(discount: int, total_amount: int):
    total_discount = total_amount * (discount / 100)
    payment_amount = total_amount - total_discount

    return total_discount, payment_amount
