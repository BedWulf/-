"""Вкладка: Сводная ведомость"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class SummaryTab(QWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)
        self.project = project
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        header = QLabel("📊 Сводная ведомость")
        header.setObjectName("title")
        layout.addWidget(header)
        subtitle = QLabel("Итоговые результаты расчёта цеха")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        info = QLabel("• Сводная ведомость оборудования\n• Итоговая численность рабочих\n• Общая площадь цеха\n• Экспорт в Excel/Word")
        info.setStyleSheet("color: #C9A84C; padding: 16px;")
        layout.addWidget(info)
        layout.addStretch()