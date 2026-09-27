"""Вкладка «Фонды времени» — отображение расчёта фондов времени цеха."""
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea,
)

from config import COLORS
from core.project import Project
from core.time_funds import calculate_time_funds, get_reference_table

# ─── Стили ────────────────────────────────────────────────────────────
GROUP_STYLE = f"""
QGroupBox {{
    background-color: {COLORS['bg_panel']};
    border: 1px solid {COLORS['separator']};
    border-radius: 6px;
    margin-top: 24px;
    padding-top: 16px;
    padding-left: 12px;
    padding-right: 12px;
    padding-bottom: 12px;
    font-weight: bold;
    color: {COLORS['accent']};
    font-size: 13px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    top: 2px;
    padding: 0 6px;
    color: {COLORS['accent']};
}}
QGroupBox QLabel {{
    color: {COLORS['text_primary']};
    font-size: 13px;
    background: transparent;
}}
"""

VALUE_STYLE = f"""
QLabel {{
    color: {COLORS['accent']};
    font-size: 28px;
    font-weight: bold;
    padding: 4px 12px;
    background-color: {COLORS['bg_main']};
    border: 1px solid {COLORS['separator']};
    border-radius: 4px;
}}
"""

FORMULA_STYLE = f"""
QLabel {{
    color: {COLORS['text_secondary']};
    font-size: 12px;
    font-style: italic;
    padding: 2px 8px;
}}
"""


class TimeFundsTab(QWidget):
    """Вкладка расчёта фондов времени."""

    funds_updated = Signal(dict)

    def __init__(self, project: Project, parent=None):
        super().__init__(parent)
        self.project = project
        self._build_ui()
        self._recalculate()

    # ─────────────────────────────────────────────────────────────────
    # UI
    # ─────────────────────────────────────────────────────────────────
    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        # Заголовок
        title = QLabel("⏱ Фонды времени и режимы работы")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['accent']}; padding: 4px 0 8px 0;")
        root.addWidget(title)

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
        container.setStyleSheet(f"background-color: {COLORS['bg_main']};")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(16)
        scroll.setWidget(container)

        # ── Группа 1: Текущие значения фондов ────────────────────────
        layout.addWidget(self._build_current_funds_group())

        # ── Группа 2: Формулы расчёта ────────────────────────────────
        layout.addWidget(self._build_formulas_group())

        # ── Группа 3: Справочная таблица ─────────────────────────────
        layout.addWidget(self._build_reference_table_group())

        layout.addStretch()

    def _build_current_funds_group(self) -> QGroupBox:
        g = QGroupBox("Текущие значения фондов времени")
        g.setStyleSheet(GROUP_STYLE)
        layout = QVBoxLayout(g)
        layout.setContentsMargins(12, 20, 12, 12)
        layout.setSpacing(12)

        # Сетка 2×2 с крупными значениями
        grid = QHBoxLayout()
        grid.setSpacing(16)

        self.lbl_F_cal = self._make_fund_card("F_кал", "Календарный фонд", "ч")
        self.lbl_F_nom = self._make_fund_card("F_ном", "Номинальный фонд", "ч")
        self.lbl_F_eq  = self._make_fund_card("F_д.об", "Действ. фонд оборудования", "ч")
        self.lbl_F_wr  = self._make_fund_card("F_д.р", "Действ. фонд рабочих", "ч")

        grid.addWidget(self.lbl_F_cal)
        grid.addWidget(self.lbl_F_nom)
        grid.addWidget(self.lbl_F_eq)
        grid.addWidget(self.lbl_F_wr)

        layout.addLayout(grid)

        # Параметры режима
        params_layout = QHBoxLayout()
        self.lbl_shifts = QLabel("Смен: —")
        self.lbl_weekends = QLabel("Выходных: —")
        self.lbl_holidays = QLabel("Праздников: —")
        for lbl in (self.lbl_shifts, self.lbl_weekends, self.lbl_holidays):
            lbl.setStyleSheet(f"""
                QLabel {{
                    color: {COLORS['text_secondary']};
                    font-size: 12px;
                    padding: 4px 10px;
                    background-color: {COLORS['bg_panel']};
                    border: 1px solid {COLORS['separator']};
                    border-radius: 4px;
                }}
            """)
        params_layout.addWidget(self.lbl_shifts)
        params_layout.addWidget(self.lbl_weekends)
        params_layout.addWidget(self.lbl_holidays)
        params_layout.addStretch()
        layout.addLayout(params_layout)

        return g

    def _make_fund_card(self, code: str, name: str, unit: str) -> QWidget:
        """Создать карточку с крупным значением фонда."""
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_main']};
                border: 1px solid {COLORS['separator']};
                border-radius: 6px;
            }}
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)

        # Код
        code_lbl = QLabel(code)
        code_lbl.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['accent']};
                font-size: 14px;
                font-weight: bold;
            }}
        """)
        code_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(code_lbl)

        # Значение
        val_lbl = QLabel("—")
        val_lbl.setObjectName(f"val_{code}")
        val_lbl.setStyleSheet(VALUE_STYLE)
        val_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(val_lbl)

        # Единица
        unit_lbl = QLabel(unit)
        unit_lbl.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_secondary']};
                font-size: 11px;
            }}
        """)
        unit_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(unit_lbl)

        # Название
        name_lbl = QLabel(name)
        name_lbl.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_primary']};
                font-size: 11px;
            }}
        """)
        name_lbl.setAlignment(Qt.AlignCenter)
        name_lbl.setWordWrap(True)
        layout.addWidget(name_lbl)

        # Сохраним ссылку на метку значения
        card._value_label = val_lbl
        return card

    def _build_formulas_group(self) -> QGroupBox:
        g = QGroupBox("Формулы расчёта (по методичке)")
        g.setStyleSheet(GROUP_STYLE)
        layout = QVBoxLayout(g)
        layout.setContentsMargins(12, 20, 12, 12)
        layout.setSpacing(8)

        formulas = [
            ("F_кал", "365 × 24 = 8760 ч", "Календарный фонд — константа"),
            ("F_ном", "(365 − 104 − 12) × 24 = 5976 ч",
             "Номинальный фонд (104 выходных + 12 праздников)"),
            ("F_д.об", "Таблица 3 методички → 3890 ч (2 смены)",
             "Действительный фонд оборудования (с учётом плановых потерь)"),
            ("F_д.р", "Таблица 4 методички → 3975 ч (2 смены)",
             "Действительный фонд рабочих (с учётом отпусков и болезней)"),
        ]

        for code, formula, desc in formulas:
            row = QHBoxLayout()

            code_lbl = QLabel(code)
            code_lbl.setStyleSheet(f"""
                QLabel {{
                    color: {COLORS['accent']};
                    font-weight: bold;
                    font-size: 13px;
                    min-width: 60px;
                }}
            """)
            row.addWidget(code_lbl)

            formula_lbl = QLabel(formula)
            formula_lbl.setStyleSheet(f"""
                QLabel {{
                    color: {COLORS['text_primary']};
                    font-size: 13px;
                    font-family: "Consolas", "Courier New", monospace;
                    padding: 4px 8px;
                    background-color: {COLORS['bg_main']};
                    border: 1px solid {COLORS['separator']};
                    border-radius: 4px;
                }}
            """)
            row.addWidget(formula_lbl, 1)

            desc_lbl = QLabel(desc)
            desc_lbl.setStyleSheet(FORMULA_STYLE)
            row.addWidget(desc_lbl, 1)

            layout.addLayout(row)

        return g

    def _build_reference_table_group(self) -> QGroupBox:
        g = QGroupBox("Справочная таблица фондов времени")
        g.setStyleSheet(GROUP_STYLE)
        layout = QVBoxLayout(g)
        layout.setContentsMargins(12, 20, 12, 12)

        self.ref_table = QTableWidget()
        self.ref_table.setColumnCount(5)
        self.ref_table.setHorizontalHeaderLabels([
            "Режим работы", "F_кал, ч", "F_ном, ч", "F_д.об, ч", "F_д.р, ч"
        ])
        self.ref_table.setRowCount(3)
        self.ref_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.ref_table.setAlternatingRowColors(True)
        self.ref_table.verticalHeader().setVisible(False)
        self.ref_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['bg_main']};
                alternate-background-color: {COLORS['bg_panel']};
                color: {COLORS['text_primary']};
                gridline-color: {COLORS['separator']};
                border: 1px solid {COLORS['separator']};
                font-size: 13px;
            }}
            QHeaderView::section {{
                background-color: {COLORS['bg_panel']};
                color: {COLORS['accent']};
                padding: 8px;
                border: 1px solid {COLORS['separator']};
                font-weight: bold;
            }}
            QTableWidget::item {{
                padding: 6px;
            }}
        """)

        # Заполнить справочную таблицу
        ref_data = get_reference_table()
        for row, (shifts, values) in enumerate(sorted(ref_data.items())):
            items = [
                f"{shifts} смена{'и' if shifts > 1 else ''}",
                str(values["F_кал"]),
                str(values["F_ном"]),
                str(values["F_д.об"]),
                str(values["F_д.р"]),
            ]
            for col, val in enumerate(items):
                cell = QTableWidgetItem(val)
                cell.setTextAlignment(Qt.AlignCenter)
                # Выделить текущий режим
                if shifts == self.project.shifts_per_day:
                    cell.setBackground(QColor(COLORS["accent"]))
                    cell.setForeground(QColor(COLORS["bg_main"]))
                    cell.setFont(QFont("Segoe UI", 13, QFont.Bold))
                self.ref_table.setItem(row, col, cell)

        header = self.ref_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        for i in range(1, 5):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

        layout.addWidget(self.ref_table)
        return g

    # ─────────────────────────────────────────────────────────────────
    # Пересчёт
    # ─────────────────────────────────────────────────────────────────
    def _recalculate(self) -> None:
        """Пересчитать фонды времени на основе параметров проекта."""
        tf = calculate_time_funds(
            shifts=self.project.shifts_per_day,
            weekends=104,
            holidays=12,
        )

        # Обновить карточки
        self.lbl_F_cal._value_label.setText(f"{int(tf.F_calendar):,}")
        self.lbl_F_nom._value_label.setText(f"{int(tf.F_nominal):,}")
        self.lbl_F_eq._value_label.setText(f"{int(tf.F_equipment):,}")
        self.lbl_F_wr._value_label.setText(f"{int(tf.F_workers):,}")

        # Обновить параметры
        self.lbl_shifts.setText(f"Смен: {tf.shifts}")
        self.lbl_weekends.setText(f"Выходных: {tf.weekends}")
        self.lbl_holidays.setText(f"Праздников: {tf.holidays}")

        # Обновить выделение в справочной таблице
        self._highlight_current_shifts(tf.shifts)

        # Сохранить в проект
        self.project.F_calendar_h = tf.F_calendar
        self.project.F_nominal_h = tf.F_nominal
        self.project.F_equipment_h = tf.F_equipment
        self.project.F_workers_h = tf.F_workers

        # Сигнал для других вкладок
        self.funds_updated.emit(tf.as_dict())

    def _highlight_current_shifts(self, shifts: int) -> None:
        """Подсветить строку текущего режима в справочной таблице."""
        for row in range(self.ref_table.rowCount()):
            for col in range(self.ref_table.columnCount()):
                item = self.ref_table.item(row, col)
                if item is None:
                    continue
                # Сбросить стили
                bg = COLORS["bg_main"] if row % 2 == 0 else COLORS["bg_panel"]
                item.setBackground(QColor(bg))
                item.setForeground(QColor(COLORS["text_primary"]))
                item.setFont(QFont("Segoe UI", 13))

            # Выделить текущий режим
            first_item = self.ref_table.item(row, 0)
            if first_item and str(shifts) in first_item.text():
                for col in range(self.ref_table.columnCount()):
                    item = self.ref_table.item(row, col)
                    if item:
                        item.setBackground(QColor(COLORS["accent"]))
                        item.setForeground(QColor(COLORS["bg_main"]))
                        item.setFont(QFont("Segoe UI", 13, QFont.Bold))

    def on_project_changed(self) -> None:
        """Вызывается при изменении параметров проекта."""
        self._recalculate()