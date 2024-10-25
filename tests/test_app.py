from app.utils import generate_signature


def test_generate_signature():
    order_id = "12345"
    secret_key = "test_secret_key"
    expected_signature = (
        "e1ce78a08ef9c6b83cedf47237afe3c8da46ab69ba6b05daf35d504ebb8c7196"
    )
    signature = generate_signature(order_id, secret_key)
    assert signature == expected_signature
    secret_key = "other_secret_key"
    signature = generate_signature(order_id, secret_key)
    assert signature != expected_signature
