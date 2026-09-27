# utils/converters.py
"""Конвертеры единиц и вспомогательные функции."""


def kg_to_t(kg: float) -> float:
    return kg / 1000.0


def t_to_kg(t: float) -> float:
    return t * 1000.0


def m3_to_cm3(m3: float) -> float:
    return m3 * 1_000_000.0


def round2(value: float) -> float:
    return round(value, 2)