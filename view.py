from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from typing import List
from model import Task


class PyQtView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Список завдань — PyQt6")
        self.resize(750, 500)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # додавання
        top_layout = QHBoxLayout()

        label = QLabel("Опис завдання:")
        label.setFont(QFont("Segoe UI", 11))
        top_layout.addWidget(label)

        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Введіть нове завдання...")
        self.entry.setFont(QFont("Segoe UI", 11))
        self.entry.returnPressed.connect(self.add_task)
        top_layout.addWidget(self.entry)

        add_btn = QPushButton("Додати")
        add_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        add_btn.clicked.connect(self.add_task)
        top_layout.addWidget(add_btn)

        layout.addLayout(top_layout)

        # таблиця завдань
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["№", "Статус", "Опис"])
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 290)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # стилізація статусу
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        # кнопки дій
        btn_layout = QHBoxLayout()

        mark_btn = QPushButton("Позначити як виконане")
        mark_btn.clicked.connect(self.mark_done)
        btn_layout.addWidget(mark_btn)

        delete_btn = QPushButton("Видалити")
        delete_btn.clicked.connect(self.delete_task)
        btn_layout.addWidget(delete_btn)

        refresh_btn = QPushButton("Оновити")
        refresh_btn.clicked.connect(self.refresh)
        btn_layout.addWidget(refresh_btn)

        exit_btn = QPushButton("Вихід")
        exit_btn.clicked.connect(QApplication.quit)
        btn_layout.addStretch()
        btn_layout.addWidget(exit_btn)

        layout.addLayout(btn_layout)

        self.refresh()

    def add_task(self):
        desc = self.entry.text().strip()
        if not desc:
            QMessageBox.warning(self, "Помилка", "Опис не може бути порожнім!")
            return

        if self.controller.model.add_task(desc):
            self.entry.clear()
            self.refresh()
            QMessageBox.information(self, "Успіх", "Завдання додано!")
        else:
            QMessageBox.critical(self, "Помилка", "Не вдалося додати завдання")

    def mark_done(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Увага", "Виберіть завдання!")
            return

        idx = row
        if self.controller.model.mark_done(idx):
            self.refresh()
            QMessageBox.information(self, "Успіх", "Завдання позначено як виконане!")
        else:
            QMessageBox.warning(self, "Помилка", "Не вдалося позначити")

    def delete_task(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Увага", "Виберіть завдання!")
            return

        reply = QMessageBox.question(
            self, "Підтвердження",
            "Видалити це завдання?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            idx = row
            if self.controller.model.delete_task(idx):
                self.refresh()
                QMessageBox.information(self, "Успіх", "Завдання видалено!")
            else:
                QMessageBox.warning(self, "Помилка", "Не вдалося видалити")

    def refresh(self):
        self.table.setRowCount(0)
        tasks: List[Task] = self.controller.model.get_all_tasks()

        if not tasks:
            self.table.insertRow(0)
            self.table.setItem(0, 1, QTableWidgetItem("[Список порожній]"))
            self.table.item(0, 1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.item(0, 1).setForeground(QColor("orange"))
            return

        for i, task in enumerate(tasks):
            self.table.insertRow(i)

            num_item = QTableWidgetItem(str(i + 1))
            num_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 0, num_item)

            status = "✓" if task.done else "—"
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if task.done:
                status_item.setForeground(QColor("green"))
                status_item.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            else:
                status_item.setForeground(QColor("gray"))
            self.table.setItem(i, 1, status_item)

            desc_item = QTableWidgetItem(task.description)
            self.table.setItem(i, 2, desc_item)