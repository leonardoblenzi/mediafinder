from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
    QLineEdit,
    QComboBox,
    QLabel,
    QMessageBox,
    QHeaderView,
)


class DirectoryDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Diretório")
        self.setMinimumWidth(560)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 20)
        layout.setSpacing(10)

        name_label = QLabel("Nome")
        layout.addWidget(name_label)
        self.label_edit = QLineEdit()
        self.label_edit.setPlaceholderText("Ex.: Fotos da família")
        name_label.setBuddy(self.label_edit)
        layout.addWidget(self.label_edit)

        path_label = QLabel("Caminho")
        layout.addWidget(path_label)
        path_row = QHBoxLayout()
        path_row.setSpacing(8)
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Selecione uma pasta para pesquisar")
        path_label.setBuddy(self.path_edit)
        browse_btn = QPushButton("Procurar...")
        browse_btn.setObjectName("secondaryButton")
        browse_btn.clicked.connect(self.browse)
        path_row.addWidget(self.path_edit)
        path_row.addWidget(browse_btn)
        layout.addLayout(path_row)

        classification_label = QLabel("Classificação (opcional)")
        layout.addWidget(classification_label)
        self.classification = QComboBox()
        self.classification.setEditable(True)
        self.classification.addItems(["", "Fotos", "Vídeos", "Geral"])
        classification_label.setBuddy(self.classification)
        layout.addWidget(self.classification)

        buttons = QHBoxLayout()
        buttons.setSpacing(8)
        buttons.addStretch()
        cancel = QPushButton("Cancelar")
        save = QPushButton("Salvar")
        cancel.setObjectName("secondaryButton")
        save.setObjectName("primaryButton")
        cancel.clicked.connect(self.reject)
        save.clicked.connect(self.validate_and_accept)
        buttons.addWidget(cancel)
        buttons.addWidget(save)
        layout.addLayout(buttons)

        if data:
            self.label_edit.setText(data["label"])
            self.path_edit.setText(data["path"])
            current = data["classification"] or ""
            idx = self.classification.findText(current)
            if idx < 0:
                self.classification.addItem(current)
                idx = self.classification.findText(current)
            self.classification.setCurrentIndex(idx)

    def browse(self):
        folder = QFileDialog.getExistingDirectory(self, "Escolher diretório")
        if folder:
            self.path_edit.setText(folder)
            if not self.label_edit.text().strip():
                self.label_edit.setText(folder.split("/")[-1].split("\\")[-1])

    def validate_and_accept(self):
        if not self.label_edit.text().strip():
            QMessageBox.warning(self, "Atenção", "Informe um nome para o diretório.")
            return
        if not self.path_edit.text().strip():
            QMessageBox.warning(self, "Atenção", "Informe o caminho do diretório.")
            return
        self.accept()

    def values(self):
        return (
            self.label_edit.text().strip(),
            self.path_edit.text().strip(),
            self.classification.currentText().strip() or None,
        )


class SettingsDialog(QDialog):
    changed = False

    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Configurações de diretórios")
        self.resize(820, 440)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 20)
        layout.setSpacing(14)

        info = QLabel(
            "Cadastre as pastas que serão pesquisadas. A classificação é opcional."
        )
        info.setObjectName("subtitle")
        info.setWordWrap(True)
        layout.addWidget(info)

        self.table = QTableWidget(0, 3)
        self.table.setObjectName("settingsTable")
        self.table.setHorizontalHeaderLabels(["Nome", "Caminho", "Classificação"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.table)

        actions = QHBoxLayout()
        actions.setSpacing(8)
        add_btn = QPushButton("Adicionar")
        edit_btn = QPushButton("Editar")
        remove_btn = QPushButton("Remover")
        close_btn = QPushButton("Fechar")

        add_btn.setObjectName("primaryButton")
        edit_btn.setObjectName("secondaryButton")
        remove_btn.setObjectName("dangerButton")
        close_btn.setObjectName("secondaryButton")

        add_btn.clicked.connect(self.add_directory)
        edit_btn.clicked.connect(self.edit_directory)
        remove_btn.clicked.connect(self.remove_directory)
        close_btn.clicked.connect(self.accept)

        actions.addWidget(add_btn)
        actions.addWidget(edit_btn)
        actions.addWidget(remove_btn)
        actions.addStretch()
        actions.addWidget(close_btn)

        layout.addLayout(actions)
        self.load()

    def load(self):
        self.table.setRowCount(0)
        rows = self.db.list_directories()

        for d in rows:
            row = self.table.rowCount()
            self.table.insertRow(row)

            items = [
                QTableWidgetItem(d["label"]),
                QTableWidgetItem(d["path"]),
                QTableWidgetItem(d["classification"] or "—"),
            ]

            for col, item in enumerate(items):
                item.setData(32, d["id"])
                self.table.setItem(row, col, item)

    def selected_directory(self):
        row = self.table.currentRow()
        if row < 0:
            return None

        directory_id = self.table.item(row, 0).data(32)
        for d in self.db.list_directories():
            if d["id"] == directory_id:
                return d
        return None

    def add_directory(self):
        dialog = DirectoryDialog(self)
        if dialog.exec():
            label, path, classification = dialog.values()
            try:
                self.db.add_directory(label, path, classification)
                self.changed = True
                self.load()
            except Exception as exc:
                QMessageBox.critical(self, "Erro", str(exc))

    def edit_directory(self):
        selected = self.selected_directory()
        if not selected:
            QMessageBox.information(self, "Editar", "Selecione um diretório.")
            return

        dialog = DirectoryDialog(self, selected)
        if dialog.exec():
            label, path, classification = dialog.values()
            try:
                self.db.update_directory(selected["id"], label, path, classification)
                self.changed = True
                self.load()
            except Exception as exc:
                QMessageBox.critical(self, "Erro", str(exc))

    def remove_directory(self):
        selected = self.selected_directory()
        if not selected:
            QMessageBox.information(self, "Remover", "Selecione um diretório.")
            return

        answer = QMessageBox.question(
            self,
            "Remover diretório",
            f"Remover '{selected['label']}' da pesquisa?\n\nOs arquivos não serão apagados.",
        )

        if answer == QMessageBox.StandardButton.Yes:
            self.db.delete_directory(selected["id"])
            self.changed = True
            self.load()
