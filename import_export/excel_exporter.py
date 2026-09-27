"""Импорт номенклатуры отливок из Excel.

Структура Excel соответствует Таблице 9 «Ведомость формовки» из диплома:
  № | Наименование | Масса с ЛПС, кг | Габариты, мм | Годовое кол-во форм |
    | Размеры опок, мм | Заливочная масса, кг | Масса металла в год, т |
    | Объём смеси, м³ | Тип формовочной машины
"""
from pathlib import Path
from typing import List, Optional

from openpyxl import load_workbook

from core.casting_item import CastingItem


# Ожидаемые заголовки столбцов (в порядке следования)
EXPECTED_HEADERS = [
    "№",
    "Наименование отливки",
    "Масса с ЛПС, кг",
    "Габариты, мм",
    "Годовое кол-во форм с учётом брака",
    "Размеры опок, мм",
    "Заливочная масса, кг",
    "Масса металла в год, т",
    "Объём смеси, м³",
    "Тип формовочной машины",
]


class ExcelImporter:
    """Парсер Excel-файла номенклатуры отливок."""

    def __init__(self, filepath: Path):
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            raise FileNotFoundError(f"Файл не найден: {self.filepath}")

    def parse(self, header_row: int = 1, data_start_row: int = 2) -> List[CastingItem]:
        """Разобрать Excel и вернуть список CastingItem.

        Args:
            header_row: номер строки с заголовками
            data_start_row: номер первой строки данных
        """
        wb = load_workbook(self.filepath, data_only=True)
        ws = wb.active

        items: List[CastingItem] = []
        for row_idx, row in enumerate(ws.iter_rows(min_row=data_start_row, values_only=True),
                                     start=data_start_row):
            # Пропускаем пустые строки и строки-итоги
            if not row or row[0] is None:
                continue
            first_cell = str(row[0]).strip().lower()
            if first_cell in ("итого", "всего", ""):
                continue

            try:
                item = self._row_to_casting(row, row_idx)
                if item and item.validate():
                    items.append(item)
            except (ValueError, IndexError) as e:
                print(f"[ExcelImporter] Строка {row_idx} пропущена: {e}")
                continue

        wb.close()
        return items

    # ---------- internals ----------
    @staticmethod
    def _to_float(value, default: float = 0.0) -> float:
        if value is None:
            return default
        try:
            return float(str(value).replace(",", ".").strip())
        except ValueError:
            return default

    @staticmethod
    def _to_int(value, default: int = 0) -> int:
        return int(ExcelImporter._to_float(value, float(default)))

    def _row_to_casting(self, row, row_idx: int) -> Optional[CastingItem]:
        """Преобразовать строку Excel в CastingItem.

        Соответствие колонок (Таблица 9 диплома):
          0: №
          1: Наименование
          2: Масса с ЛПС, кг
          3: Габариты, мм
          4: Годовое кол-во форм с учётом брака
          5: Размеры опок, мм
          6: Заливочная масса, кг
          7: Масса металла в год, т
          8: Объём смеси, м³
          9: Тип формовочной машины
        """
        if len(row) < 10:
            return None

        return CastingItem(
            index=self._to_int(row[0], row_idx),
            name=str(row[1]).strip() if row[1] else "",
            mass_with_LPS_kg=self._to_float(row[2]),
            dimensions_mm=str(row[3]).strip() if row[3] else "",
            molds_per_year=self._to_int(row[4]),
            flask_size_mm=str(row[5]).strip() if row[5] else "",
            pouring_mass_kg=self._to_float(row[6]),
            annual_metal_t=self._to_float(row[7]),
            mix_volume_m3=self._to_float(row[8]),
            molding_machine=str(row[9]).strip() if row[9] else "ИЛ-225",
            annual_qty_with_brak=self._to_int(row[4]),  # формы = кол-во с браком
        )