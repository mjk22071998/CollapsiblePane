import sys
import unittest
from PySide6.QtWidgets import QApplication, QLabel, QWidget
from PySide6.QtGui import QIcon, QPixmap, QMouseEvent, QKeyEvent
from PySide6.QtCore import Qt, QEvent, QPointF

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

    def test_modena_javafx_theme_and_style(self):
        self.pane.apply_modena_style(dark=False)
        self.assertTrue(self.pane.unified_box)
        self.assertEqual(self.pane._collapsed_icon, "▶")
        self.assertEqual(self.pane._expanded_icon, "▼")
        self.assertIn("#0096C9", self.pane.styleSheet())  # JavaFX Modena focus accent

        self.pane.apply_modena_style(dark=True)
        self.assertIn("#389fd6", self.pane.styleSheet())

    def test_keyboard_navigation_toggle(self):
        from PySide6.QtGui import QKeyEvent
        from PySide6.QtCore import QEvent
        content = QLabel("Key Test Content")
        self.pane.set_content_widget(content)

        self.assertFalse(self.pane.is_expanded)
        # Simulate Space key on header
        space_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Space, Qt.NoModifier)
        self.pane._on_header_key_press(space_event)
        self.assertTrue(self.pane.is_expanded)

        # Simulate Return key on header
        return_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Return, Qt.NoModifier)
        self.pane._on_header_key_press(return_event)
        self.assertFalse(self.pane.is_expanded)

    def test_collapsible_property(self):
        self.assertTrue(self.pane.is_collapsible)
        self.pane.is_collapsible = False
        self.assertFalse(self.pane.is_collapsible)
        self.assertFalse(self.pane.chevron_label.isVisible())
        self.assertTrue(self.pane.is_expanded)  # Non-collapsible auto-expands

        # Clicking should not collapse
        self.pane.toggle(False)
        self.assertTrue(self.pane.is_expanded)

        press_event = QMouseEvent(
            QEvent.MouseButtonPress,
            QPointF(5, 5),
            QPointF(5, 5),
            Qt.LeftButton,
            Qt.LeftButton,
            Qt.NoModifier
        )
        self.pane._on_header_mouse_press(press_event)
        # Should stay expanded because collapsible is False
        self.assertTrue(self.pane.is_expanded)

    def test_animated_property(self):
        self.assertTrue(self.pane.is_animated)
        content = QLabel("Animated Test Content")
        self.pane.set_content_widget(content)

        self.pane.is_animated = False
        self.assertFalse(self.pane.is_animated)

        self.pane.toggle(True)
        self.assertTrue(self.pane.is_expanded)
        # Instant toggle should immediately set full content height without waiting
        self.assertGreater(self.pane.content_area.maximumHeight(), 0)

    def test_graphic_widget(self):
        self.assertIsNone(self.pane.graphic)
        icon_widget = QLabel("★")
        self.pane.set_graphic(icon_widget)
        self.assertIs(self.pane.graphic, icon_widget)

        self.pane.set_graphic(None)
        self.assertIsNone(self.pane.graphic)

    def test_accordion_container(self):
        from collapsiblepane import Accordion
        accordion = Accordion()

        pane1 = CollapsiblePane("Pane 1", animation_duration=10)
        pane2 = CollapsiblePane("Pane 2", animation_duration=10)
        content1 = QLabel("C1")
        content2 = QLabel("C2")
        pane1.set_content_widget(content1)
        pane2.set_content_widget(content2)

        accordion.add_pane(pane1)
        accordion.add_pane(pane2)

        self.assertEqual(len(accordion.panes), 2)
        self.assertIsNone(accordion.expanded_pane)

        # Expand pane 1
        accordion.set_expanded_pane(pane1)
        self.assertIs(accordion.expanded_pane, pane1)
        self.assertTrue(pane1.is_expanded)
        self.assertFalse(pane2.is_expanded)

        # Expand pane 2 -> pane 1 should automatically collapse
        accordion.set_expanded_pane(pane2)
        self.assertIs(accordion.expanded_pane, pane2)
        self.assertTrue(pane2.is_expanded)
        self.assertFalse(pane1.is_expanded)

        accordion.deleteLater()
        pane1.deleteLater()
        pane2.deleteLater()


if __name__ == "__main__":
    unittest.main()
