# utils/validators.py
"""Валидаторы входных данных."""


def is_positive(value: float, name: str = "value") -> float:
    if value <= 0:
        raise ValueError(f"{name} должно быть > 0, получено {value}")
    return float(value)


def in_range(value: float, lo: float, hi: float, name: str = "value") -> float:
    if not (lo <= value <= hi):
        raise ValueError(f"{name} должно быть в [{lo}, {hi}], получено {value}")
    return float(value)


def pct(value: float, name: str = "percent") -> float:
    """Процент в диапазоне 0..100."""
    return in_range(value, 0.0, 100.0, name)