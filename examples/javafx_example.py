"""
JavaFX TitledPane & Accordion Showcase for PySide6 (CollapsiblePane)
Demonstrates:
  1. Authentic JavaFX Modena Light & Dark themes
  2. Solid directional arrows (▶ / ▼) with 0px gap unified box styling
  3. Interactive keyboard accessibility (Tab focus + #0096C9 focus ring + Space/Enter toggle)
  4. Header graphic node support (matching JavaFX setGraphic)
  5. Non-collapsible pane (JavaFX collapsible=false)
  6. JavaFX Accordion container with mutually exclusive expansion
"""

import sys
from pathlib import Path

# Ensure package root is in sys.path when running from source
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox, QRadioButton,
    QFrame, QScrollArea, QTabWidget
)
from PySide6.QtCore import Qt
from collapsiblepane import CollapsiblePane, Accordion, Theme


class JavaFXShowcase(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JavaFX TitledPane & Accordion Showcase (PySide6)")
        self.resize(720, 680)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # --- Top Header Banner ---
        banner = QFrame(self)
        banner.setStyleSheet("""
            QFrame {
                background: #f4f6f8;
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 12px 16px;
            }
        """)
        banner_layout = QHBoxLayout(banner)
        banner_layout.setContentsMargins(8, 8, 8, 8)

        title_col = QVBoxLayout()
        title_lbl = QLabel("JavaFX TitledPane Look & Feel", banner)
        title_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #1f2328;")
        sub_lbl = QLabel(
            "Authentic Modena gradients, #0096C9 focus ring, solid arrows, unified box geometry, and Accordion.",
            banner
        )
        sub_lbl.setStyleSheet("font-size: 12px; color: #656d76;")
        title_col.addWidget(title_lbl)
        title_col.addWidget(sub_lbl)
        banner_layout.addLayout(title_col)
        banner_layout.addStretch()

        # Theme toggle button
        self.dark_mode = False
        self.theme_btn = QPushButton("Switch to Modena Dark", banner)
        self.theme_btn.setCursor(Qt.PointingHandCursor)
        self.theme_btn.setStyleSheet("""
            QPushButton {
                background: #24292f;
                color: #ffffff;
                border-radius: 6px;
                padding: 6px 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #32383f;
            }
        """)
        self.theme_btn.clicked.connect(self._toggle_theme)
        banner_layout.addWidget(self.theme_btn)

        main_layout.addWidget(banner)

        # --- Scrollable showcase body ---
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(16)
        scroll_layout.setContentsMargins(4, 4, 4, 4)

        # 1. Standalone JavaFX TitledPane (Expanded by default)
        self.pane1 = CollapsiblePane("1. General Configuration (Standalone TitledPane)", expanded=True)
        self.pane1.apply_modena_style(dark=False)
        self.pane1.set_item_count(3)

        # Add a custom graphic icon (JavaFX setGraphic equivalent)
        icon_lbl = QLabel("⚙")
        icon_lbl.setStyleSheet("font-size: 14px; color: #0096C9; padding-right: 2px;")
        self.pane1.set_graphic(icon_lbl)

        content1 = QWidget()
        c1_layout = QVBoxLayout(content1)
        c1_layout.setSpacing(8)
        c1_layout.addWidget(QLabel("Project Title:"))
        c1_layout.addWidget(QLineEdit("JavaFX Modern Desktop App"))
        c1_layout.addWidget(QCheckBox("Enable Hardware Acceleration (-Dprism.order=d3d,sw)"))
        c1_layout.addWidget(QCheckBox("Auto-check for updates on launch"))
        self.pane1.set_content_widget(content1)
        scroll_layout.addWidget(self.pane1)

        # 2. Non-Collapsible TitledPane (JavaFX collapsible=false)
        self.pane2 = CollapsiblePane("2. System Information (collapsible=False)", collapsible=False, expanded=True)
        self.pane2.apply_modena_style(dark=False)
        content2 = QWidget()
        c2_layout = QVBoxLayout(content2)
        c2_layout.addWidget(QLabel("This pane has <b>collapsible=False</b>. The arrow is hidden and it is locked open."))
        c2_layout.addWidget(QLabel("JavaFX Runtime: OpenJFX 21+ / Python PySide6"))
        self.pane2.set_content_widget(content2)
        scroll_layout.addWidget(self.pane2)

        # 3. JavaFX Accordion (Mutually exclusive group)
        acc_header = QLabel("3. JavaFX Accordion Container (At most one expanded at a time)")
        acc_header.setStyleSheet("font-size: 14px; font-weight: bold; color: #24292f; margin-top: 8px;")
        scroll_layout.addWidget(acc_header)

        self.accordion = Accordion(self)

        self.acc_pane_a = CollapsiblePane("User Profile & Authentication")
        self.acc_pane_a.apply_modena_style(dark=False)
        content_a = QWidget()
        ca_layout = QVBoxLayout(content_a)
        ca_layout.addWidget(QLabel("Username:"))
        ca_layout.addWidget(QLineEdit("alex_developer"))
        ca_layout.addWidget(QLabel("Role:"))
        role_combo = QComboBox()
        role_combo.addItems(["Administrator", "Developer", "Analyst", "Guest"])
        ca_layout.addWidget(role_combo)
        self.acc_pane_a.set_content_widget(content_a)

        self.acc_pane_b = CollapsiblePane("Network & Proxy Settings")
        self.acc_pane_b.apply_modena_style(dark=False)
        content_b = QWidget()
        cb_layout = QVBoxLayout(content_b)
        cb_layout.addWidget(QRadioButton("Direct Connection (No proxy)"))
        cb_layout.addWidget(QRadioButton("Use System Proxy"))
        cb_layout.addWidget(QRadioButton("Manual HTTP/SOCKS Proxy"))
        self.acc_pane_b.set_content_widget(content_b)

        self.acc_pane_c = CollapsiblePane("Notification & Alert Rules")
        self.acc_pane_c.apply_modena_style(dark=False)
        content_c = QWidget()
        cc_layout = QVBoxLayout(content_c)
        cc_layout.addWidget(QCheckBox("Desktop push notifications"))
        cc_layout.addWidget(QCheckBox("Sound effect on critical errors"))
        cc_layout.addWidget(QCheckBox("Daily digest emails"))
        self.acc_pane_c.set_content_widget(content_c)

        self.accordion.add_pane(self.acc_pane_a)
        self.accordion.add_pane(self.acc_pane_b)
        self.accordion.add_pane(self.acc_pane_c)

        # Expand the first accordion pane by default
        self.accordion.set_expanded_pane(self.acc_pane_a)
        scroll_layout.addWidget(self.accordion)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # Keep references to all panes for theme switching
        self.all_panes = [self.pane1, self.pane2, self.acc_pane_a, self.acc_pane_b, self.acc_pane_c]

    def _toggle_theme(self):
        self.dark_mode = not self.dark_mode
        theme = Theme.MODENA_DARK if self.dark_mode else Theme.MODENA
        self.theme_btn.setText("Switch to Modena Light" if self.dark_mode else "Switch to Modena Dark")

        for p in self.all_panes:
            p.apply_modena_style(dark=self.dark_mode)

        if self.dark_mode:
            self.setStyleSheet("QMainWindow { background-color: #1e1e1e; color: #e0e0e0; }")
        else:
            self.setStyleSheet("QMainWindow { background-color: #fcfcfc; color: #1f2328; }")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JavaFXShowcase()
    window.show()
    sys.exit(app.exec())
