"""Загрузчик JSON-справочников с поддержкой подпапок."""
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class DataLoader:
    """Единая точка доступа к JSON-справочникам."""

    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            from config import DATA_DIR
            data_dir = DATA_DIR
        self.data_dir = Path(data_dir)
        self._cache: Dict[str, Any] = {}

    def _resolve_path(self, filename: str) -> Path:
        """Найти файл: сначала в подпапках, потом в корне data/."""
        # Проверяем прямое указание пути (например, "equipment/furnaces.json")
        direct = self.data_dir / filename
        if direct.exists():
            return direct

        # Ищем в подпапках
        for subdir in self.data_dir.iterdir():
            if subdir.is_dir():
                candidate = subdir / filename
                if candidate.exists():
                    return candidate

        raise FileNotFoundError(f"Справочник не найден: {filename} (искать в {self.data_dir})")

    def load(self, filename: str, use_cache: bool = True) -> Any:
        """Загрузить JSON-файл."""
        if use_cache and filename in self._cache:
            return self._cache[filename]

        path = self._resolve_path(filename)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if use_cache:
            self._cache[filename] = data
        return data

    def load_list(self, filename: str, key: Optional[str] = None) -> List[Dict[str, Any]]:
        """Загрузить JSON как список.
        
        Args:
            filename: имя файла
            key: если JSON — словарь, взять список по этому ключу (например, "furnaces")
        """
        data = self.load(filename)
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and key:
            return data.get(key, [])
        if isinstance(data, dict) and "alloys" in data:
            return data["alloys"]
        if isinstance(data, dict) and "furnaces" in data:
            return data["furnaces"]
        raise ValueError(f"Ожидался список в {filename}")

    def load_dict(self, filename: str) -> Dict[str, Any]:
        """Загрузить JSON как словарь."""
        data = self.load(filename)
        if not isinstance(data, dict):
            raise ValueError(f"Ожидался словарь в {filename}")
        return data

    def get_alloy(self, alloy_id: str) -> Optional[Dict[str, Any]]:
        """Найти сплав по ID."""
        alloys = self.load_list("materials/alloys.json")
        for a in alloys:
            if a["id"] == alloy_id:
                return a
        return None

    def get_alloy_category(self, alloy_id: str) -> Optional[str]:
        """Получить категорию сплава (steel, cast_iron, aluminum)."""
        alloy = self.get_alloy(alloy_id)
        return alloy.get("category") if alloy else None

    def get_categories(self) -> List[Dict[str, str]]:
        """Получить список категорий материалов."""
        data = self.load("materials/alloys.json")
        return data.get("categories", [])

    def get_alloys_by_category(self, category_id: str) -> List[Dict[str, Any]]:
        """Получить сплавы по категории."""
        alloys = self.load_list("materials/alloys.json")
        return [a for a in alloys if a.get("category") == category_id]

    def get_coefficient(self, name: str, default: float = 0.0) -> float:
        """Получить коэффициент по имени."""
        try:
            coeffs = self.load_dict("coefficients.json")
            return float(coeffs.get(name, default))
        except (FileNotFoundError, ValueError):
            return default

    def clear_cache(self) -> None:
        """Очистить кэш (например, после редактирования JSON)."""
        self._cache.clear()