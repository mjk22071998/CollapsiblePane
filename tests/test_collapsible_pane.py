import sys
import unittest
from PySide6.QtWidgets import QApplication, QLabel, QWidget
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt

from collapsiblepane import CollapsiblePane

# Ensure a single QApplication instance exists for tests
app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)


class TestCollapsiblePane(unittest.TestCase):
    def setUp(self):
        self.pane = CollapsiblePane(title="Test Pane", animation_duration=50)

    def tearDown(self):
        self.pane.deleteLater()

    def test_initial_state(self):
        self.assertEqual(self.pane.title, "Test Pane")
        self.assertFalse(self.pane.is_expanded)
        self.assertIsNone(self.pane.content_widget)
        self.assertEqual(self.pane.animation_duration, 50)
        self.assertEqual(self.pane.chevron_label.text(), "▸")

    def test_title_property_and_setter(self):
        self.pane.title = "Updated Title"
        self.assertEqual(self.pane.title, "Updated Title")
        self.assertEqual(self.pane.title_label.text(), "Updated Title")

        self.pane.set_title("Second Update")
        self.assertEqual(self.pane.title, "Second Update")

    def test_content_widget_attachment_and_clear(self):
        label = QLabel("Hello World")
        self.pane.set_content_widget(label)

        self.assertIsNotNone(self.pane.content_widget)
        self.assertIs(self.pane.content_widget, label)

        self.pane.clear_widget()
        self.assertIsNone(self.pane.content_widget)

    def test_chevron_icons_text(self):
        self.pane.set_chevron_icons("+", "-")
        self.assertEqual(self.pane.chevron_label.text(), "+")

        self.pane.set_collapsed(False)
        self.assertEqual(self.pane.chevron_label.text(), "-")

    def test_chevron_icons_qicon(self):
        pix = QPixmap(16, 16)
        pix.fill(Qt.red)
        icon1 = QIcon(pix)
        icon2 = QIcon(pix)

        self.pane.set_chevron_icons(icon1, icon2)
        self.assertTrue(self.pane._use_qicon)
        self.assertFalse(self.pane.chevron_label.pixmap().isNull())

    def test_item_count_badge(self):
        self.pane.set_item_count(42)
        self.assertIn("42", self.pane.count_label.text())

        self.pane.set_item_badge_style(text="Active", bg_color="#ff0000")
        self.assertEqual(self.pane.count_label.text(), "Active")

        self.pane.set_item_count(None)
        self.assertEqual(self.pane.count_label.text(), "")

    def test_header_style_and_alias(self):
        self.pane.set_header_style(background_color="#123456", text_color="#ffffff")
        # Ensure alias exists and executes without error
        self.pane.set_title_bar_style(background_color="#654321")

    def test_card_style_and_alias(self):
        self.pane.set_card_style(background="#fafafa", border="#cccccc")
        # Ensure alias exists and executes without error
        self.pane.set_content_style(background="#ffffff")

    def test_card_shadow_does_not_break_opacity(self):
        self.pane.set_card_shadow(color="#000000", blur=15, offset_y=3)
        self.assertIsNotNone(self.pane.content_area.graphicsEffect())
        self.assertIsNotNone(self.pane.opacity_effect)

    def test_set_collapsed_immediate(self):
        content = QLabel("Detailed content")
        self.pane.set_content_widget(content)

        self.pane.set_collapsed(False)
        self.assertTrue(self.pane.is_expanded)
        self.assertGreater(self.pane.content_area.maximumHeight(), 0)

        self.pane.set_collapsed(True)
        self.assertFalse(self.pane.is_expanded)
        self.assertEqual(self.pane.content_area.maximumHeight(), 0)

    def test_signal_emission_on_toggle(self):
        content = QLabel("Signal Test")
        self.pane.set_content_widget(content)

        received_states = []
        self.pane.toggled.connect(received_states.append)

        self.pane.toggle(True)
        self.assertIn(True, received_states)

        self.pane.toggle(False)
        self.assertIn(False, received_states)

    def test_theme_and_stylesheet(self):
        from collapsiblepane import Theme, get_theme_stylesheet
        self.pane.apply_theme(Theme.LIGHT)
        self.assertIn("#f8fafc", self.pane.styleSheet())

        dark_css = get_theme_stylesheet(Theme.DARK)
        self.assertIn("#1e293b", dark_css)
        self.pane.setStyleSheet(dark_css)
        self.assertIn("#1e293b", self.pane.styleSheet())

    def test_max_content_height(self):
        container = QWidget()
        container.resize(200, 800)
        container.setMinimumHeight(800)
        self.pane.set_content_widget(container)
        self.pane.set_max_content_height(250)

        self.pane.set_collapsed(False)
        self.assertLessEqual(self.pane.content_area.maximumHeight(), 250)

    def test_size_hint_reflects_content(self):
        label = QLabel("Test size hint line")
        self.pane.set_content_widget(label)
        collapsed_hint = self.pane.sizeHint()

        self.pane.set_collapsed(False)
        expanded_hint = self.pane.sizeHint()
        self.assertGreater(expanded_hint.height(), collapsed_hint.height())


if __name__ == "__main__":
    unittest.main()
