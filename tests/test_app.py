import pytest
import hashlib
from unittest.mock import patch
from app import generate_signature


def test_generate_signature():
    order_id = "12345"
    secret_key = "test_secret_key"
    expected_signature = 'e1ce78a08ef9c6b83cedf47237afe3c8da46ab69ba6b05daf35d504ebb8c7196'
    with patch('app.app.config', {'SECRET_KEY': secret_key}):
        signature = generate_signature(order_id)
        assert signature == expected_signature
    signature = generate_signature(order_id)
    assert signature != expected_signature
