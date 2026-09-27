"""Тесты для модуля расчёта фондов времени.

Эталонные значения из диплома (2 смены, 249 рабочих дней):
  F_кал = 8760 ч
  F_ном = 5976 ч
  F_д.об = 3890 ч
  F_д.р = 3975 ч
"""
import sys
from pathlib import Path

# Добавляем корень проекта в path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.time_funds import calculate_time_funds, get_reference_table


def test_calendar_fund():
    """F_кал всегда = 8760 ч."""
    tf = calculate_time_funds(shifts=2)
    assert tf.F_calendar == 8760, f"Ожидалось 8760, получено {tf.F_calendar}"
    print("✅ F_кал = 8760 ч")


def test_nominal_fund():
    """F_ном = (365 − 104 − 12) × 24 = 5976 ч."""
    tf = calculate_time_funds(shifts=2, weekends=104, holidays=12)
    assert tf.F_nominal == 5976, f"Ожидалось 5976, получено {tf.F_nominal}"
    print("✅ F_ном = 5976 ч")


def test_equipment_fund_2shifts():
    """F_д.об для 2 смен = 3890 ч (табл. 3 методички)."""
    tf = calculate_time_funds(shifts=2)
    assert tf.F_equipment == 3890, f"Ожидалось 3890, получено {tf.F_equipment}"
    print("✅ F_д.об = 3890 ч (2 смены)")


def test_workers_fund_2shifts():
    """F_д.р для 2 смен = 3975 ч (табл. 4 методички)."""
    tf = calculate_time_funds(shifts=2)
    assert tf.F_workers == 3975, f"Ожидалось 3975, получено {tf.F_workers}"
    print("✅ F_д.р = 3975 ч (2 смены)")


def test_reference_table():
    """Проверка справочной таблицы для всех режимов."""
    ref = get_reference_table()
    assert 1 in ref and 2 in ref and 3 in ref
    assert ref[2]["F_д.об"] == 3890
    assert ref[2]["F_д.р"] == 3975
    print("✅ Справочная таблица корректна")


def test_as_dict():
    """Метод as_dict возвращает правильный словарь."""
    tf = calculate_time_funds(shifts=2)
    d = tf.as_dict()
    assert d["F_кал"] == 8760
    assert d["F_ном"] == 5976
    assert d["F_д.об"] == 3890
    assert d["F_д.р"] == 3975
    print("✅ as_dict() работает корректно")


if __name__ == "__main__":
    print("🧪 Тесты модуля time_funds\n" + "=" * 40)
    test_calendar_fund()
    test_nominal_fund()
    test_equipment_fund_2shifts()
    test_workers_fund_2shifts()
    test_reference_table()
    test_as_dict()
    print("\n🎉 Все тесты пройдены!")