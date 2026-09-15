import sys

from PySide6.QtWidgets import QApplication

from mediafinder.db import Database
from mediafinder.main_window import MainWindow
from mediafinder.theme import apply_theme


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Pesquisa de Mídias")
    app.setOrganizationName("FZ Tech")
    apply_theme(app)

    db = Database()
    window = MainWindow(db)
    window.resize(1180, 760)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
