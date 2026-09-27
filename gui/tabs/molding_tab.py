"""Вкладка: Формовочное отделение"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class MoldingTab(QWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)
        self.project = project
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        header = QLabel("🏗 Формовочное отделение")
        header.setObjectName("title")
        layout.addWidget(header)

        subtitle = QLabel("Раздел 4: Метод формовки, группы по массе, АФЛ ИЛ-225, заливка")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)

        info = QLabel(
            "• Выбор метода изготовления форм\n"
            "• Анализ групп по массе\n"
            "• Расчёт количества АФЛ\n"
            "• Выбор способа заливки\n"
            "• Расчёт ковшей"
        )
        info.setStyleSheet("color: #C9A84C; padding: 16px;")
        layout.addWidget(info)
        layout.addStretch()