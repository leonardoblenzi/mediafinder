import unittest


class ThemeTests(unittest.TestCase):
    def test_theme_defines_clear_visual_tokens_and_component_selectors(self):
        from mediafinder.theme import APP_THEME

        required_tokens = (
            "#1f2937",  # readable dark text
            "#ffffff",  # white cards and controls
            "#2563eb",  # primary action
        )
        required_selectors = (
            "QMainWindow",
            "QWidget {",
            "QLabel {",
            "QFrame#resultCard",
            "QPushButton#primaryButton",
            "QPushButton#secondaryButton",
            "QPushButton#dangerButton",
            "QPushButton#dangerButton:hover",
            "QPushButton#dangerButton:pressed",
            "QTableView",
            "QTableWidget",
            "QMenu",
            "QToolTip",
        )

        for token in required_tokens:
            self.assertIn(token, APP_THEME)
        for selector in required_selectors:
            self.assertIn(selector, APP_THEME)

        self.assertIn("QWidget {\n    color: #1f2937;", APP_THEME)
        self.assertIn("QLabel {\n    color: #1f2937;", APP_THEME)

    def test_apply_theme_sets_the_global_stylesheet(self):
        from mediafinder.theme import APP_THEME, apply_theme

        class Widget:
            def __init__(self):
                self.stylesheet = None

            def setStyleSheet(self, stylesheet):
                self.stylesheet = stylesheet

        widget = Widget()
        apply_theme(widget)

        self.assertEqual(APP_THEME, widget.stylesheet)


if __name__ == "__main__":
    unittest.main()
