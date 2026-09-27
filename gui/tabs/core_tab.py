"""Вкладка «Стержневое отделение» — расчет стержневого производства."""
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QLabel, QLineEdit, QDoubleSpinBox, QSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QScrollArea, QAbstractItemView,
)

from config import COLORS
from core.project import Project


# ─── Стили ──
GROUP_STYLE = f"""
QGroupBox {{
    background-color: {COLORS['bg_panel']};
    border: 1px solid {COLORS['separator']};
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 18px;
    font-weight: bold;
    color: {COLORS['accent']};
    font-size: 13px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 14px;
    padding: 0 6px;
}}
"""

FIELD_STYLE = f"""
QLineEdit, QSpinBox, QDoubleSpinBox {{
    background-color: #3A1010;
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['separator']};
    border-radius: 4px;
    padding: 6px 10px;
    font-size: 13px;
    min-height: 28px;
}}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 1px solid {COLORS['accent']};
}}
QLabel {{
    color: {COLORS['text_primary']};
    font-size: 13px;
}}
"""


class CoreTab(QWidget):
    """Вкладка расчета стержневого отделения."""

    def __init__(self, project: Project, parent=None):
        super().__init__(parent)
        self.project = project
        self._building = True
        self._build_ui()
        self._load_from_project()
        self._building = False

    # ─────────────────────────────────────────────────────────────────
    # UI
    # ─────────────────────────────────────────────────────────────────
    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        # Заголовок
        title = QLabel("🧱 Стержневое отделение")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['accent']}; padding: 4px 0 8px 0;")
        root.addWidget(title)

        # Скролл
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: {COLORS['bg_main']};
                border: 1px solid {COLORS['separator']};
                border-radius: 4px;
            }}
        """)
        root.addWidget(scroll, 1)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(14)
        scroll.setWidget(container)

        # ── Группа 1: Параметры стержневой смеси ──
        layout.addWidget(self._build_mix_group())

        # ── Группа 2: Параметры стержневого ящика ──
        layout.addWidget(self._build_core_box_group())

        # ── Группа 3: Оборудование ──
        layout.addWidget(self._build_equipment_group())

        # ── Кнопка расчета ──
        calc_btn = QPushButton("️ Рассчитать параметры")
        calc_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']};
                color: {COLORS['bg_main']};
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{ background-color: #FF8555; }}
            QPushButton:pressed {{ background-color: #D95520; }}
        """)
        calc_btn.clicked.connect(self._calculate)
        layout.addWidget(calc_btn)

        # ── Результаты ──
        layout.addWidget(self._build_results_group())

        layout.addStretch()

    # ─────────────────────────────────────────────────────────────────
    # Группы параметров
    # ─────────────────────────────────────────────────────────────────
    def _build_mix_group(self) -> QGroupBox:
        g = QGroupBox("Параметры стержневой смеси")
        g.setStyleSheet(GROUP_STYLE)
        form = QFormLayout(g)
        form.setLabelAlignment(Qt.AlignRight)
        form.setStyleSheet(FIELD_STYLE)

        self.combo_mix_type = QDoubleSpinBox()
        self.combo_mix_type.setRange(0, 100)
        self.combo_mix_type.setDecimals(1)
        self.combo_mix_type.setValue(94.0)
        self.combo_mix_type.setSuffix(" % кварцевого песка")
        form.addRow("Кварцевый песок:", self.combo_mix_type)

        self.spin_binder = QDoubleSpinBox()
        self.spin_binder.setRange(0, 100)
        self.spin_binder.setDecimals(1)
        self.spin_binder.setValue(3.0)
        self.spin_binder.setSuffix(" % связующего")
        form.addRow("Связующее (УСК-1):", self.spin_binder)

        self.spin_lignosulfonate = QDoubleSpinBox()
        self.spin_lignosulfonate.setRange(0, 100)
        self.spin_lignosulfonate.setDecimals(1)
        self.spin_lignosulfonate.setValue(3.0)
        self.spin_lignosulfonate.setSuffix(" % лигносульфоната")
        form.addRow("Лигносульфонат:", self.spin_lignosulfonate)

        return g

    def _build_core_box_group(self) -> QGroupBox:
        g = QGroupBox("Параметры стержневого ящика")
        g.setStyleSheet(GROUP_STYLE)
        form = QFormLayout(g)
        form.setLabelAlignment(Qt.AlignRight)
        form.setStyleSheet(FIELD_STYLE)

        self.spin_cavities = QSpinBox()
        self.spin_cavities.setRange(1, 100)
        self.spin_cavities.setValue(1)
        self.spin_cavities.setSuffix(" гнезд")
        form.addRow("Количество гнезд:", self.spin_cavities)

        self.spin_core_time = QDoubleSpinBox()
        self.spin_core_time.setRange(0.1, 60)
        self.spin_core_time.setDecimals(1)
        self.spin_core_time.setValue(5.0)
        self.spin_core_time.setSuffix(" мин на стержень")
        form.addRow("Время изготовления:", self.spin_core_time)

        return g

    def _build_equipment_group(self) -> QGroupBox:
        g = QGroupBox("Оборудование (по методичке)")
        g.setStyleSheet(GROUP_STYLE)
        form = QFormLayout(g)
        form.setLabelAlignment(Qt.AlignRight)
        form.setStyleSheet(FIELD_STYLE)

        self.edit_machine = QLineEdit("23229А2А")
        self.edit_machine.setReadOnly(True)
        form.addRow("Машина:", self.edit_machine)

        self.edit_machine_output = QLineEdit("54 форм/ч")
        self.edit_machine_output.setReadOnly(True)
        form.addRow("Производительность:", self.edit_machine_output)

        self.edit_box_size = QLineEdit("1600×800×300 мм")
        self.edit_box_size.setReadOnly(True)
        form.addRow("Макс. размер ящика:", self.edit_box_size)

        return g

    def _build_results_group(self) -> QGroupBox:
        g = QGroupBox("Результаты расчета")
        g.setStyleSheet(GROUP_STYLE)
        layout = QVBoxLayout(g)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Параметр", "Значение"])
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: #3A1010;
                alternate-background-color: #4A1515;
                color: {COLORS['text_primary']};
                gridline-color: {COLORS['separator']};
                border: 1px solid {COLORS['separator']};
                font-size: 12px;
            }}
            QHeaderView::section {{
                background-color: {COLORS['bg_panel']};
                color: {COLORS['accent']};
                padding: 6px;
                border: 1px solid {COLORS['separator']};
                font-weight: bold;
            }}
        """)
        layout.addWidget(self.results_table)
        return g

    # ─────────────────────────────────────────────────────────────────
    # Загрузка данных
    # ─────────────────────────────────────────────────────────────────
    def _load_from_project(self) -> None:
        # Пока базовые значения, позже свяжем с моделью
        pass

    # ─────────────────────────────────────────────────────────────────
    # Расчет
    # ─────────────────────────────────────────────────────────────────
    def _calculate(self) -> None:
        try:
            cavities = self.spin_cavities.value()
            time_per_core = self.spin_core_time.value()

            # Производительность: стержней в час
            hourly_output = (60.0 / time_per_core) * cavities
            # Годовая производительность (2 смены, 249 дней, 8 ч/смена)
            annual_hours = 2 * 249 * 8  # 3984 ч
            annual_output = hourly_output * annual_hours

            # Коэффициент загрузки (примерно)
            load_factor = min(1.0, annual_output / (annual_hours * 54))

            # Очистка таблицы
            self.results_table.setRowCount(0)

            results = [
                ("Время изготовления 1 стержня", f"{time_per_core} мин"),
                ("Количество гнезд в ящике", f"{cavities}"),
                ("Производительность", f"{hourly_output:.1f} стержней/ч"),
                ("Годовой фонд времени", f"{annual_hours} ч"),
                ("Годовая производительность", f"{annual_output:,.0f} стержней"),
                ("Коэффициент загрузки", f"{load_factor:.2f}"),
                ("Рекомендуемая машина", "23229А2А"),
                ("Паспортная производительность", "54 форм/ч"),
            ]

            self.results_table.setRowCount(len(results))
            for row, (param, value) in enumerate(results):
                self.results_table.setItem(row, 0, QTableWidgetItem(param))
                self.results_table.setItem(row, 1, QTableWidgetItem(value))

            self.results_table.horizontalHeader().setSectionResizeMode(
                0, QHeaderView.Stretch
            )
            self.results_table.horizontalHeader().setSectionResizeMode(
                1, QHeaderView.ResizeToContents
            )

        except Exception as e:
            QMessageBox.critical(self, "Ошибка расчета", f"{type(e).__name__}: {e}")