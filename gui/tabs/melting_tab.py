"""Вкладка: Плавильное отделение"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class MeltingTab(QWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)
        self.project = project
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        header = QLabel("🔥 Плавильное отделение")
        header.setObjectName("title")
        layout.addWidget(header)

        subtitle = QLabel("Раздел 3: Металлозавалка, шихта, расчёт печей (ИСТ-6М1)")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)

        # TODO: Здесь будет полный расчёт плавильного отделения
        info = QLabel(
            "• Расчёт металлозавалки\n"
            "• Ведомость шихтовых материалов\n"
            "• Выбор типа печей\n"
            "• Расчёт количества печей\n"
            "• Коэффициент загрузки"
        )
        info.setStyleSheet("color: #C9A84C; padding: 16px;")
        layout.addWidget(info)
        layout.addStretch()