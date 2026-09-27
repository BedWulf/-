"""Вкладка: Отделение обрубки, очистки и термообработки"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class CleaningTab(QWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)
        self.project = project
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        header = QLabel("🧹 Обрубка, очистка и термообработка")
        header.setObjectName("title")
        layout.addWidget(header)
        subtitle = QLabel("Раздел 7: ПМР-1000, 42322, ЗМ636, нормализация")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        info = QLabel("• Газокислородная резка\n• Дробемётная очистка\n• Обдирочно-шлифовальные станки\n• Агрегаты нормализации")
        info.setStyleSheet("color: #C9A84C; padding: 16px;")
        layout.addWidget(info)
        layout.addStretch()