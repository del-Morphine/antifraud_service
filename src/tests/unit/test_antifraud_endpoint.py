import pytest
from fastapi.testclient import TestClient
from datetime import date, timedelta

from app.main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def valid_request_body(
    *,
    birth_date: date,
    phone_number: str,
    loans_history: list,
) -> dict:
    return {
        "birth_date": birth_date.strftime("%d.%m.%Y"),
        "phone_number": phone_number,
        "loans_history": loans_history,
    }


# --- Позитивные кейсы ---

def test_antifraud_ok(client):
    body = valid_request_body(
        birth_date=date.today().replace(year=date.today().year - 30),
        phone_number="+79123456789",
        loans_history=[
            {
                "amount": 10_000,
                "loan_date": "01.01.2023",
                "is_closed": True,
            }
        ],
    )

    response = client.post("/antifraud/check", json=body)

    assert response.status_code == 200
    assert response.json() == {
        "stop_factors": [],
        "result": True,
    }


# --- Чек отдельных стоп-факторов ---

@pytest.mark.parametrize(
    "body,expected_stop_factors",
    [
        (
            # Несовершеннолетний
            {
                "birth_date": date.today().strftime("%d.%m.%Y"),
                "phone_number": "+79123456789",
                "loans_history": [],
            },
            ["underage"],
        ),
        (
            # Невалидный телефон
            {
                "birth_date": "01.01.1990",
                "phone_number": "123",
                "loans_history": [],
            },
            ["invalid_phone"],
        ),
        (
            # Открытый займ
            {
                "birth_date": "01.01.1990",
                "phone_number": "+79123456789",
                "loans_history": [
                    {
                        "amount": 10_000,
                        "loan_date": "01.01.2023",
                        "is_closed": False,
                    }
                ],
            },
            ["open_loan"],
        ),
    ],
)
def test_antifraud_stop_factors(client, body, expected_stop_factors):
    response = client.post("/antifraud/check", json=body)

    assert response.status_code == 200
    assert response.json()["result"] is False
    assert set(response.json()["stop_factors"]) == set(expected_stop_factors)


# --- Чек нескольких стоп-факторов ---

def test_multiple_stop_factors(client):
    body = {
        "birth_date": date.today().strftime("%d.%m.%Y"),
        "phone_number": "123",
        "loans_history": [
            {
                "amount": 10_000,
                "loan_date": "01.01.2023",
                "is_closed": False,
            }
        ],
    }

    response = client.post("/antifraud/check", json=body)

    assert response.status_code == 200
    assert response.json()["result"] is False
    assert set(response.json()["stop_factors"]) == {
        "invalid_phone",
        "underage",
        "open_loan",
    }


@pytest.mark.parametrize(
    "body",
    [
        # Дата рождения в будущем
        {
            "birth_date": (date.today() + timedelta(days=1)).strftime("%d.%m.%Y"),
            "phone_number": "+79123456789",
            "loans_history": [],
        },
        # Дата займа в будущем
        {
            "birth_date": "01.01.1990",
            "phone_number": "+79123456789",
            "loans_history": [
                {
                    "amount": 10_000,
                    "loan_date": (date.today() + timedelta(days=1)).strftime("%d.%m.%Y"),
                    "is_closed": True,
                }
            ],
        },
    ],
)
def test_invalid_input_returns_422(client, body):
    response = client.post("/antifraud/check", json=body)

    assert response.status_code == 422
