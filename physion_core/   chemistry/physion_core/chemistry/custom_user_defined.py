from .base import BaseChemistry

class CustomUserChemistry(BaseChemistry):
    def __init__(self, params):
        self.p = params

    # کاربر همهٔ توابع را خودش تعریف می‌کند
