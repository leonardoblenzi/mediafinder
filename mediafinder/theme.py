"""Tema global da interface do MediaFinder."""

APP_THEME = """
* {
    color: #1f2937;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 14px;
}

QMainWindow, QDialog {
    background: #f5f7fb;
}

QWidget {
    color: #1f2937;
}

QLabel {
    color: #1f2937;
}

QWidget#centralWidget, QWidget#contentArea {
    background: #f5f7fb;
}

QFrame#resultCard, QFrame#sidebar, QFrame#emptyState {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
}

QLabel#title {
    color: #111827;
    font-size: 24px;
    font-weight: 700;
}

QLabel#subtitle, QLabel#status, QLabel#filePath {
    color: #64748b;
}

QLabel#fileName {
    color: #111827;
    font-size: 15px;
    font-weight: 600;
}

QLabel#badges {
    color: #475569;
}

QLabel#preview {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 7px;
}

QLineEdit, QComboBox, QSpinBox, QTextEdit {
    min-height: 36px;
    padding: 0 10px;
    color: #1f2937;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 7px;
    selection-background-color: #bfdbfe;
}

QTextEdit {
    padding: 8px;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QTextEdit:focus {
    border: 2px solid #2563eb;
}

QPushButton {
    min-height: 34px;
    padding: 0 13px;
    color: #1f2937;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 7px;
    font-weight: 600;
}

QPushButton:hover {
    background: #f1f5f9;
    border-color: #94a3b8;
}

QPushButton:pressed {
    background: #e2e8f0;
}

QPushButton#primaryButton {
    color: #ffffff;
    background: #2563eb;
    border-color: #2563eb;
}

QPushButton#primaryButton:hover {
    background: #1d4ed8;
    border-color: #1d4ed8;
}

QPushButton#secondaryButton {
    color: #1e40af;
    background: #eff6ff;
    border-color: #bfdbfe;
}

QPushButton#secondaryButton:hover {
    background: #dbeafe;
    border-color: #93c5fd;
}

QPushButton#dangerButton {
    color: #b91c1c;
    background: #fef2f2;
    border-color: #fecaca;
}

QPushButton#dangerButton:hover {
    color: #ffffff;
    background: #dc2626;
    border-color: #dc2626;
}

QPushButton#dangerButton:pressed {
    color: #ffffff;
    background: #b91c1c;
    border-color: #b91c1c;
}

QTableView, QTableWidget, QListView, QTreeView {
    color: #1f2937;
    background: #ffffff;
    alternate-background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    gridline-color: #e2e8f0;
    selection-background-color: #dbeafe;
    selection-color: #111827;
}

QHeaderView::section {
    padding: 8px;
    color: #475569;
    background: #f8fafc;
    border: none;
    border-bottom: 1px solid #e2e8f0;
    font-weight: 700;
}

QScrollArea {
    border: none;
    background: transparent;
}

QMenu {
    padding: 6px;
    color: #1f2937;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 7px;
}

QMenu::item {
    padding: 8px 26px 8px 10px;
    border-radius: 5px;
}

QMenu::item:selected {
    color: #1e3a8a;
    background: #dbeafe;
}

QToolTip {
    padding: 6px 8px;
    color: #ffffff;
    background: #1f2937;
    border: 1px solid #334155;
    border-radius: 5px;
}
"""


def apply_theme(widget):
    """Aplica a folha de estilos global ao widget raiz da aplicação."""
    widget.setStyleSheet(APP_THEME)
