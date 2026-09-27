"""Вкладка: Площади"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class AreasTab(QWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)
        self.project = project
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        header = QLabel("📐 Площади цеха")
        header.setObjectName("title")
        layout.addWidget(header)
        subtitle = QLabel("Раздел 10, 11: Производственные и административные площади")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        info = QLabel("• Производственные площади по отделениям\n• Складские площади\n• Административно-бытовые помещения")
        info.setStyleSheet("color: #C9A84C; padding: 16px;")
        layout.addWidget(info)
        layout.addStretch()