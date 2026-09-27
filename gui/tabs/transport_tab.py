"""Вкладка: Транспорт"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class TransportTab(QWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)
        self.project = project
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        header = QLabel("🚛 Внутрицеховой транспорт")
        header.setObjectName("title")
        layout.addWidget(header)
        subtitle = QLabel("Раздел 12: Мостовые краны, конвейеры, пневмотранспорт")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        info = QLabel("• Мостовые краны\n• Роликовые и пластинчатые конвейеры\n• Пневмотранспорт")
        info.setStyleSheet("color: #C9A84C; padding: 16px;")
        layout.addWidget(info)
        layout.addStretch()