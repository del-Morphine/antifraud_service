from pydantic import BaseModel, field_validator, Field
from typing import List
from enum import StrEnum
from datetime import date, datetime
import re

PHONE_REGEX = re.compile(r"^(8|\+7)\d{10}$")

class StopFactor(StrEnum):
    """Перечисление возможных стоп-факторов при проверке антифрода"""
    INVALID_PHONE = "invalid_phone"
    UNDERAGE = "underage" 
    OPEN_LOAN = "open_loan"

class Loan(BaseModel):
    """Модель данных о займе клиента"""
    
    amount: int = Field(
        description="Сумма займа в рублях",
        example=10000,
        gt=0  # Чекаем, что сумма больше нуля
    )
    
    loan_date: date = Field(
        description="Дата оформления займа в формате DD.MM.YYYY",
        example="22.10.2025"
    )
    
    is_closed: bool = Field(
        description="Статус закрытия займа: true - закрыт, false - активен",
        example=True
    )

    @field_validator("loan_date", mode="before")
    @classmethod
    def parse_loan_date(cls, value: str) -> date:
        """Преобразование строки в объект date с валидацией формата"""
        try:
            return datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("loan_date must be in DD.MM.YYYY format")

    @field_validator("loan_date")
    @classmethod
    def validate_loan_date_not_future(cls, value: date) -> date:
        """Валидация, что дата займа не из будущего"""
        if value > date.today():
            raise ValueError("loan_date cannot be in the future")
        return value

class AntifraudRequest(BaseModel):
    """Модель запроса для проверки антифрода"""
    
    birth_date: date = Field(
        description="Дата рождения клиента в формате DD.MM.YYYY",
        example="22.08.1977"
    )
    
    phone_number: str = Field(
        description="Номер телефона клиента, должен начинаться с +7 или 8",
        examples=["+79132281337", "89132281337"],
        min_length=11,
        max_length=12
    )
    
    loans_history: List[Loan] = Field(
        description="История займов клиента",
        example=[
            {"amount": 10000, "loan_date": "22.10.2023", "is_closed": True},
            {"amount": 25000, "loan_date": "01.12.2023", "is_closed": False}
        ]
    )

    @field_validator("birth_date", mode="before")
    @classmethod
    def parse_birth_date(cls, value: str) -> date:
        """Преобразование строки даты рождения в объект date"""
        try:
            return datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("birth_date must be in DD.MM.YYYY format")

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date_not_future(cls, value: date) -> date:
        """Валидация, что дата рождения не из будущего"""
        if value > date.today():
            raise ValueError("birth_date cannot be in the future")
        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        """Валидация номера телефона по регулярному выражению"""
        if not PHONE_REGEX.match(value):
            raise ValueError(
                "phone_number must start with +7 or 8 and contain 10 digits after"
            )
        return value


class AntifraudResponse(BaseModel):
    """Модель ответа с результатом проверки антифрода"""
    
    stop_factors: List[str] = Field(
        description="Список выявленных стоп-факторов",
        example=["invalid_phone", "underage"]
    )
    
    result: bool = Field(
        description="Итоговый результат проверки: true - клиент прошел проверку, false - проверка не пройдена",
        example=False
    )