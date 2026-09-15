from PySide6.QtCore import QTimer, QThread, Qt
from PySide6.QtWidgets import (
    QComboBox, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMessageBox, QPushButton, QScrollArea, QVBoxLayout, QWidget,
)

from .result_card import ResultCard
from .settings_dialog import SettingsDialog
from .theme import apply_theme
from .workers import IndexWorker


class MainWindow(QMainWindow):
    """Pesquisa, filtros e apresentação responsiva do índice de mídias."""

    CARD_MINIMUM_WIDTH = 280

    def __init__(self, db):
        super().__init__()
        self.db, self.thread, self.worker = db, None, None
        self.result_cards = []
        self._grid_columns = 0
        self._grid_rows = 0
        self.setWindowTitle("Pesquisa de Mídias")
        self.setMinimumSize(820, 560)
        apply_theme(self)

        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(16)
        root.addLayout(self._header())
        root.addLayout(self._search_bar())
        root.addLayout(self._content(), 1)

        self.search_timer = QTimer(self)
        self.search_timer.setSingleShot(True)
        self.search_timer.setInterval(220)
        self.search_timer.timeout.connect(self.search)
        self.search_edit.textChanged.connect(self.queue_search)
        self.type_filter.currentTextChanged.connect(self.queue_search)
        self.class_filter.currentTextChanged.connect(self.queue_search)
        self.reload_classifications()
        self.search()
        if not self.db.list_directories():
            QTimer.singleShot(400, self.first_run_hint)

    def _header(self):
        row, titles = QHBoxLayout(), QVBoxLayout()
        titles.setSpacing(2)
        title = QLabel("Pesquisa de Mídias")
        title.setObjectName("title")
        subtitle = QLabel("Encontre fotos e vídeos nas pastas compartilhadas.")
        subtitle.setObjectName("subtitle")
        titles.addWidget(title)
        titles.addWidget(subtitle)
        row.addLayout(titles)
        row.addStretch()
        settings = QPushButton("Configurações")
        settings.setObjectName("secondaryButton")
        settings.clicked.connect(self.open_settings)
        refresh = QPushButton("Atualizar índice")
        refresh.setObjectName("primaryButton")
        refresh.clicked.connect(self.reindex)
        row.addWidget(settings)
        row.addWidget(refresh)
        return row

    def _search_bar(self):
        row = QHBoxLayout()
        row.addWidget(QLabel("Pesquisar"))
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Ex.: poltrona pé palito")
        self.search_edit.setClearButtonEnabled(True)
        self.search_edit.setAccessibleName("Pesquisar mídias")
        row.addWidget(self.search_edit, 1)
        self.count_label = QLabel("")
        self.count_label.setObjectName("status")
        row.addWidget(self.count_label)
        return row

    def _content(self):
        content = QHBoxLayout()
        content.setSpacing(16)
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        filters = QVBoxLayout(sidebar)
        filters.setContentsMargins(16, 16, 16, 16)
        filters.setSpacing(8)
        heading = QLabel("Filtros")
        heading.setObjectName("fileName")
        filters.addWidget(heading)
        filters.addWidget(QLabel("Tipo"))
        self.type_filter = QComboBox()
        self.type_filter.addItems(["Todos", "Imagem", "Vídeo"])
        self.type_filter.setAccessibleName("Filtrar por tipo")
        filters.addWidget(self.type_filter)
        filters.addWidget(QLabel("Classificação"))
        self.class_filter = QComboBox()
        self.class_filter.setAccessibleName("Filtrar por classificação")
        filters.addWidget(self.class_filter)
        filters.addSpacing(18)
        status_title = QLabel("Status do índice")
        status_title.setObjectName("fileName")
        filters.addWidget(status_title)
        self.status = QLabel("")
        self.status.setObjectName("status")
        self.status.setWordWrap(True)
        filters.addWidget(self.status)
        filters.addStretch()
        content.addWidget(sidebar)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.results_widget = QWidget()
        self.results_widget.setObjectName("contentArea")
        self.results_layout = QGridLayout(self.results_widget)
        self.results_layout.setContentsMargins(4, 4, 4, 4)
        self.results_layout.setHorizontalSpacing(12)
        self.results_layout.setVerticalSpacing(12)
        self.results_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll.setWidget(self.results_widget)
        content.addWidget(self.scroll, 1)
        return content

    def first_run_hint(self):
        QMessageBox.information(self, "Primeiro uso", "Cadastre pelo menos um diretório em Configurações.\n\nDepois clique em 'Atualizar índice'.")

    def reload_classifications(self):
        current = self.class_filter.currentText()
        self.class_filter.blockSignals(True)
        self.class_filter.clear()
        self.class_filter.addItems(["Todas", "Sem classificação"])
        self.class_filter.addItems(self.db.distinct_classifications())
        index = self.class_filter.findText(current)
        self.class_filter.setCurrentIndex(index if index >= 0 else 0)
        self.class_filter.blockSignals(False)

    def queue_search(self):
        self.search_timer.start()

    def clear_results(self):
        self._take_grid_items(delete_widgets=True)
        self._reset_grid_stretches()
        self.result_cards.clear()

    def _take_grid_items(self, delete_widgets=False):
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            if delete_widgets and item.widget():
                item.widget().deleteLater()

    def _reset_grid_stretches(self):
        columns = max(self._grid_columns, self.results_layout.columnCount())
        rows = max(self._grid_rows, self.results_layout.rowCount())
        for column in range(columns):
            self.results_layout.setColumnStretch(column, 0)
        for row in range(rows):
            self.results_layout.setRowStretch(row, 0)
        self._grid_columns = 0
        self._grid_rows = 0

    def _empty_state(self, title, message, action_text=None, callback=None):
        self._take_grid_items()
        self._reset_grid_stretches()
        state = QFrame()
        state.setObjectName("emptyState")
        layout = QVBoxLayout(state)
        layout.setContentsMargins(32, 42, 32, 42)
        layout.addStretch()
        heading = QLabel(title)
        heading.setObjectName("fileName")
        heading.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(heading)
        detail = QLabel(message)
        detail.setObjectName("status")
        detail.setWordWrap(True)
        detail.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(detail)
        if action_text and callback:
            action = QPushButton(action_text)
            action.setObjectName("primaryButton")
            action.clicked.connect(callback)
            layout.addWidget(action, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()
        self.results_layout.addWidget(state, 0, 0)
        self.results_layout.setRowStretch(0, 1)
        self.results_layout.setColumnStretch(0, 1)
        self._grid_columns = 1
        self._grid_rows = 1

    def _populate_grid(self):
        self._take_grid_items()
        self._reset_grid_stretches()
        columns = max(1, self.scroll.viewport().width() // self.CARD_MINIMUM_WIDTH)
        for column in range(columns):
            self.results_layout.setColumnStretch(column, 1)
        for index, card in enumerate(self.result_cards):
            self.results_layout.addWidget(card, index // columns, index % columns)
        self._grid_columns = columns
        self._grid_rows = (len(self.result_cards) + columns - 1) // columns

    def _show_results(self, rows):
        self.clear_results()
        self.result_cards = [ResultCard(row) for row in rows]
        self._populate_grid()

    def search(self):
        directories = self.db.list_directories()
        query = self.search_edit.text().strip()
        type_filter, class_filter = self.type_filter.currentText(), self.class_filter.currentText()
        total = self.db.count_files()
        self.clear_results()
        if not directories:
            self.count_label.setText("Nenhum diretório")
            self.status.setText("Cadastre um diretório para começar.")
            self._empty_state("Nenhum diretório cadastrado", "Adicione as pastas onde suas mídias estão armazenadas para pesquisar nelas.", "Abrir configurações", self.open_settings)
            return
        if not query and type_filter == "Todos" and class_filter == "Todas":
            self.count_label.setText("")
            self.status.setText(f"{total} arquivo(s) indexado(s).")
            message = "Digite uma palavra para procurar no índice." if total else "Atualize o índice para disponibilizar os arquivos cadastrados."
            self._empty_state("Comece uma pesquisa", message)
            return
        rows = self.db.search(query, type_filter, class_filter)
        self.count_label.setText(f"{len(rows)} resultado(s)")
        if not self.thread:
            self.status.setText(f"{total} arquivo(s) indexado(s).")
        if rows:
            self._show_results(rows)
        else:
            self._empty_state("Nenhum resultado encontrado", "Tente outra busca ou ajuste os filtros para ampliar os resultados.")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.result_cards:
            self._populate_grid()

    def open_settings(self):
        dialog = SettingsDialog(self.db, self)
        dialog.exec()
        if dialog.changed:
            self.reload_classifications()
            self.search()
            answer = QMessageBox.question(self, "Atualizar índice", "Os diretórios foram alterados. Deseja atualizar o índice agora?")
            if answer == QMessageBox.StandardButton.Yes:
                self.reindex()

    def reindex(self):
        if self.thread is not None:
            QMessageBox.information(self, "Indexação", "A atualização do índice já está em andamento.")
            return
        directories = self.db.list_directories()
        if not directories:
            QMessageBox.information(self, "Indexação", "Cadastre ao menos um diretório em Configurações.")
            return
        self.status.setText("Iniciando indexação...")
        self.thread = QThread(self)
        self.worker = IndexWorker(self.db.db_path, directories)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.status.setText)
        self.worker.error.connect(self.show_index_error)
        self.worker.finished.connect(self.on_index_finished)
        self.worker.finished.connect(self.thread.quit)
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.cleanup_thread)
        self.thread.start()

    def show_index_error(self, message):
        self.status.setText(message)

    def on_index_finished(self, total):
        self.reload_classifications()
        self.search()
        self.status.setText(f"Índice atualizado: {total} arquivo(s).")

    def cleanup_thread(self):
        if self.thread:
            self.thread.deleteLater()
        self.thread = None
        self.worker = None
