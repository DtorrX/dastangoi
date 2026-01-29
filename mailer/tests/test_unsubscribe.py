from src.unsubscribe import build_unsubscribe_token, verify_unsubscribe_token


def test_unsubscribe_roundtrip():
    token = build_unsubscribe_token("user@example.com")
    email = verify_unsubscribe_token(token)
    assert email == "user@example.com"
