import unittest


class BundleGuardTests(unittest.TestCase):
    def test_excludes_codex_runtime_and_icu_binaries(self):
        from scripts.bundle_guard import should_exclude_binary

        self.assertTrue(
            should_exclude_binary(
                (
                    "icuuc.dll",
                    r"C:\\Users\\USER\\.cache\\codex-runtimes\\poppler\\icuuc.dll",
                    "BINARY",
                )
            )
        )

    def test_keeps_application_binaries(self):
        from scripts.bundle_guard import should_exclude_binary

        self.assertFalse(
            should_exclude_binary(
                ("PySide6\\Qt6Core.dll", r"C:\\project\\PySide6\\Qt6Core.dll", "BINARY")
            )
        )
