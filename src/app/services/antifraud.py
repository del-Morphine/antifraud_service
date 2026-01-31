from datetime import date
from typing import List

from ..api.schemas.antifraud import AntifraudRequest, StopFactor

class AntifraudService:
    @staticmethod
    def check(request: AntifraudRequest) -> List[StopFactor]:
        stop_factors: List[StopFactor] = []

        if not AntifraudService._check_phone(request.phone_number):
            stop_factors.append(StopFactor.INVALID_PHONE)
        
        if not AntifraudService._check_age(request.birth_date):
            stop_factors.append(StopFactor.UNDERAGE)

        if not AntifraudService._check_loans(request.loans_history):
            stop_factors.append(StopFactor.OPEN_LOAN)
    
        return stop_factors

    @staticmethod
    def _check_phone(phone: str) -> bool:
        return phone.startswith("+7") or phone.startswith("8")
    
    @staticmethod
    def _check_age(birth_date: date) -> bool:
        today = date.today()
        age = today.year - birth_date.year
        age -= (today.month, today.day) < (birth_date.month, birth_date.day)

        return age >= 18
    
    @staticmethod
    def _check_loans(loans) -> bool:
        return all(loan.is_closed for loan in loans)