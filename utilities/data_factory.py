import uuid

from faker import Faker

from models.user import User, Address

fake = Faker()


def generate_unique_email() -> str:
    """Generate a unique email address for test execution.

    Returns:
        A unique email address that can be used for signup testing.
    """
    unique_id = uuid.uuid4().hex[:8]
    return f"test_user_{unique_id}@example.com"


def generate_random_password() -> str:
    """Generate a random password for test execution.
    Returns: generated random password for test execution.
    """
    return fake.password(length=12)


# This we will use in testcase to pass data
def new_user(**overrides) -> User:
    first_name = fake.first_name()
    last_name = fake.last_name()

    data = {
        "name": f"{first_name} {last_name}",
        "email": generate_unique_email(),
        "password": generate_random_password(),
        "address": Address(first_name=first_name, last_name=last_name),
    }
    data.update(overrides)
    return User(**data)