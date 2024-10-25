import hashlib


def generate_signature(order_id, secret_key):
    sigma = f"{order_id}{secret_key}"
    hash_object = hashlib.sha256(sigma.encode())
    signature = hash_object.hexdigest()
    return signature
