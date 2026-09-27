"""Подбор оборудования по параметрам проекта с фильтрацией по материалу."""
from typing import List, Dict, Any, Optional
from data.loader import DataLoader


class EquipmentSelector:
    """Фильтрует и ранжирует оборудование по критериям проекта."""

    def __init__(self, loader: DataLoader):
        self.loader = loader

    def find_furnaces(
        self,
        material_category: str,
        annual_charge_t: float,
        working_hours: float = 3890,
        top_n: int = 5,
    ) -> List[Dict[str, Any]]:
        """Найти подходящие печи.
        
        Args:
            material_category: категория материала (steel, cast_iron, aluminum)
            annual_charge_t: годовая металлозавалка, т
            working_hours: действительный фонд времени, ч
            top_n: сколько лучших вариантов вернуть
            
        Returns:
            Список подходящих печей с расчётными параметрами
        """
        furnaces = self.loader.load_list("equipment/furnaces.json")
        
        # Требуемая производительность
        required_productivity = annual_charge_t / working_hours if working_hours > 0 else 0
        
        candidates = []
        for f in furnaces:
            app = f.get("applicable_for", {})
            
            # Фильтр по материалу
            if material_category not in app.get("materials", []):
                continue
            
            # Расчёт количества печей
            productivity = f["specs"].get("productivity_t_h", 0)
            if productivity <= 0:
                continue
            
            import math
            num_furnaces = math.ceil(required_productivity / productivity)
            load_factor = required_productivity / (num_furnaces * productivity)
            
            # Оценка релевантности
            score = self._score_furnace(f, load_factor)
            
            candidates.append({
                **f,
                "_score": score,
                "_num_required": num_furnaces,
                "_load_factor": round(load_factor, 3),
                "_productivity_required": round(required_productivity, 3),
            })
        
        # Сортировка: recommended сначала, потом по score
        candidates.sort(
            key=lambda x: (
                x["applicable_for"].get("recommended", False),
                x["_score"]
            ),
            reverse=True,
        )
        
        return candidates[:top_n]

    def _score_furnace(self, furnace: Dict, load_factor: float) -> float:
        """Оценка релевантности печи (0..1).
        
        Оптимальная загрузка: 0.7-0.85
        """
        # Гауссиана вокруг идеальной загрузки 0.75
        ideal_load = 0.75
        score = 1.0 / (1.0 + 5 * (load_factor - ideal_load) ** 2)
        return round(score, 3)

    def get_all_furnace_types(self) -> List[str]:
        """Получить все типы печей из справочника."""
        furnaces = self.loader.load_list("equipment/furnaces.json")
        return list(set(f.get("type", "") for f in furnaces))