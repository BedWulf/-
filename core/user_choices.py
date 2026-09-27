"""Сохранение и загрузка выборов пользователя."""
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class UserChoices:
    """Управление выборами оборудования и материалов пользователем."""

    def __init__(self, base_dir: Optional[Path] = None):
        if base_dir is None:
            from config import BASE_DIR
            base_dir = BASE_DIR
        self.choices_dir = base_dir / "user_data"
        self.choices_dir.mkdir(parents=True, exist_ok=True)
        self.choices_file = self.choices_dir / "choices.json"
        self._data: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        """Загрузить выборы из файла."""
        if self.choices_file.exists():
            try:
                with open(self.choices_file, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._data = {}

    def _save(self) -> None:
        """Сохранить выборы в файл."""
        with open(self.choices_file, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    def get_choice(self, project_id: str, category: str) -> Optional[Dict[str, Any]]:
        """Получить выбор для проекта."""
        project_choices = self._data.get(project_id, {})
        return project_choices.get(category)

    def set_choice(
        self,
        project_id: str,
        category: str,
        choice_data: Dict[str, Any],
    ) -> None:
        """Сохранить выбор."""
        if project_id not in self._data:
            self._data[project_id] = {}
        
        self._data[project_id][category] = {
            **choice_data,
            "updated_at": datetime.now().isoformat(),
        }
        self._save()

    def get_project_choices(self, project_id: str) -> Dict[str, Any]:
        """Получить все выборы для проекта."""
        return self._data.get(project_id, {})

    def clear_project_choices(self, project_id: str) -> None:
        """Очистить выборы для проекта."""
        if project_id in self._data:
            del self._data[project_id]
            self._save()

    def get_selected_alloy(self, project_id: str) -> Optional[str]:
        """Получить выбранный сплав для проекта."""
        choice = self.get_choice(project_id, "alloy")
        return choice.get("alloy_id") if choice else None