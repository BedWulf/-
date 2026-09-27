"""Вкладка: Рабочая сила"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class WorkforceTab(QWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)
        self.project = project
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        header = QLabel("👥 Рабочая сила")
        header.setObjectName("title")
        layout.addWidget(header)
        subtitle = QLabel("Раздел 9: Основные и вспомогательные рабочие")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        info = QLabel("• Основные рабочие по отделениям\n• Вспомогательные рабочие\n• Лаборанты, кладовщики, крановщики")
        info.setStyleSheet("color: #C9A84C; padding: 16px;")
        layout.addWidget(info)
        layout.addStretch()