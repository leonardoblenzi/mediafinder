from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QApplication,
    QFrame,
    QMessageBox,
    QToolButton,
    QMenu,
    QSizePolicy,
)

from .utils import open_file, open_containing_folder


class ResultCard(QFrame):
    def __init__(self, row, parent=None):
        super().__init__(parent)
        self.row = row
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setObjectName("resultCard")
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setMinimumWidth(240)
        self.setMinimumHeight(180)
        self._source_pixmap = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        self.preview = QLabel()
        self.preview.setFixedHeight(56)
        self.preview.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview.setObjectName("preview")

        self.preview.setText(
            "🖼 Imagem" if row["media_type"] == "Imagem" else "▶ Vídeo"
        )

        layout.addWidget(self.preview)

        title_row = QHBoxLayout()
        title_row.setSpacing(8)

        name = QLabel(row["file_name"])
        name.setObjectName("fileName")
        name.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        name.setWordWrap(True)
        title_row.addWidget(name, 1)

        actions_button = QToolButton()
        actions_button.setObjectName("actionsButton")
        actions_button.setText("⋮")
        actions_button.setToolTip("Ações do arquivo")
        actions_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        actions_menu = QMenu(actions_button)
        actions_menu.addAction("Abrir", self.open_item)
        actions_menu.addAction("Abrir pasta", self.open_folder)
        actions_menu.addAction("Copiar caminho", self.copy_path)
        actions_button.setMenu(actions_menu)
        title_row.addWidget(actions_button, 0, Qt.AlignmentFlag.AlignTop)
        layout.addLayout(title_row)

        badges = QLabel(
            f"{row['media_type']}   •   "
            f"{row['classification'] or 'Sem classificação'}   •   "
            f"{row['directory_label']}"
        )
        badges.setObjectName("badges")
        badges.setWordWrap(True)
        layout.addWidget(badges)

        full_path = QLabel(row["full_path"])
        full_path.setObjectName("filePath")
        full_path.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        full_path.setWordWrap(True)
        layout.addWidget(full_path)

    def open_item(self):
        try:
            open_file(self.row["full_path"])
        except Exception as exc:
            QMessageBox.critical(self, "Erro", str(exc))

    def open_folder(self):
        try:
            open_containing_folder(self.row["full_path"])
        except Exception as exc:
            QMessageBox.critical(self, "Erro", str(exc))

    def copy_path(self):
        QApplication.clipboard().setText(self.row["full_path"])
