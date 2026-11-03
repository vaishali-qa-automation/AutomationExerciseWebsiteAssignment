import uuid


def generate_unique_email() -> str:
    """Generate a unique email address for test execution.

    Returns:
        A unique email address that can be used for signup testing.
    """
    unique_id = uuid.uuid4().hex[:8]
    return f"testuser_{unique_id}@example.com"