import pytest
from datetime import date, timedelta
from app.api.schemas.antifraud import Loan

@pytest.fixture
def adult_birth_date():
    return date.today().replace(year=date.today().year - 25)


@pytest.fixture
def valid_phone_plus7():
    return "+79123456789"


@pytest.fixture
def valid_phone_8():
    return "89123456789"


@pytest.fixture
def closed_loan():
    return Loan(
        amount=10_000,
        loan_date=date.today() - timedelta(days=30),
        is_closed=True,
    )


@pytest.fixture
def underage_birth_date():
    return date.today().replace(year=date.today().year - 10)


@pytest.fixture
def future_birth_date():
    return date.today() + timedelta(days=1)


@pytest.fixture
def invalid_phone():
    return "123456"


@pytest.fixture
def open_loan():
    return Loan(
        amount=10_000,
        loan_date=date.today() - timedelta(days=30),
        is_closed=False,
    )


@pytest.fixture
def future_loan():
    return Loan(
        amount=10_000,
        loan_date=date.today() + timedelta(days=1),
        is_closed=True,
    )