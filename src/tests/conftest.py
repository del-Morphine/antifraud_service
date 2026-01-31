import random
import pytest
from datetime import date, timedelta
from app.api.schemas.antifraud import Loan

@pytest.fixture
def adult_birth_date():
    return date.today().replace(year=date.today().year - 25)


@pytest.fixture
def valid_phone():
    prefix = random.choice(['+7', '8'])
    digits = ''.join(str(random.randint(0, 9)) for _ in range(10))
    return f"{prefix}{digits}"


@pytest.fixture
def closed_loan():
    return Loan(
        amount=10_000,
        loan_date=date.today() - timedelta(days=30),
        is_closed=True,
    )


@pytest.fixture
def open_loan():
    return Loan(
        amount=10_000,
        loan_date=date.today() - timedelta(days=30),
        is_closed=False,
    )
