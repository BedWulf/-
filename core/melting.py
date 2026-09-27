from dataclasses import dataclass, field
from typing import List
@dataclass
class MeltingCalculation:
    """Расчет плавильного отделения"""
    annual_metal_charge_t: float  # Годовая металлозавалка, т
    furnace_type: str  # Тип печи (ИСТ-6М1, ДСП, и т.д.)
    furnace_capacity_t: float  # Емкость тигля, т
    furnace_productivity_t_h: float  # Производительность, т/ч
    fund_hours: float  # Действительный фонд времени, ч
    k_uneven: float  # Коэффициент неравномерности (1.0-1.2)
    
    # Результаты расчета
    furnace_count: int  # Количество печей
    load_factor: float  # Коэффициент загрузки