"""Вкладка: Смесеприготовительное отделение"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class SandTab(QWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)
        self.project = project
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        header = QLabel(" Смесеприготовительное отделение")
        header.setObjectName("title")
        layout.addWidget(header)
        subtitle = QLabel("Раздел 6: Состав ЕФС, бегуны 15126 и 1А11, регенерация")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        info = QLabel("• Состав формовочной смеси\n• Расчёт бегунов\n• Оборудование регенерации")
        info.setStyleSheet("color: #C9A84C; padding: 16px;")
        layout.addWidget(info)
        layout.addStretch()