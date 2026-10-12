"""
CollapsiblePane Showcase & Demo
Demonstrates:
  1. Standard colors applied via application / pane stylesheet (QSS)
  2. Programmatic configuration via Python code API
  3. Interactive theme switching (Dark & Light)
  4. Smooth, bug-free expand/collapse animations wrapping content perfectly
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QCheckBox, QRadioButton, QSlider,
    QProgressBar, QSpinBox, QDateEdit, QTextEdit, QPushButton,
    QScrollArea, QFrame, QButtonGroup
)
from PySide6.QtCore import Qt, QDate
from collapsiblepane import CollapsiblePane, Theme, get_theme_stylesheet


# Complete professional stylesheet for demo form widgets
DARK_APP_STYLESHEET = """
QMainWindow, QWidget#central_widget {
    background-color: #0b1120;
    color: #f8fafc;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

QScrollArea#main_scroll {
    background: transparent;
    border: none;
}

QWidget#scroll_container {
    background: transparent;
}

/* Header Banner */
QFrame#banner_frame {
    background-color: #111827;
    border: 1px solid #1f2937;
    border-radius: 12px;
    padding: 16px 20px;
}

QLabel#app_title {
    color: #f8fafc;
    font-size: 20px;
    font-weight: 700;
}

QLabel#app_subtitle {
    color: #94a3b8;
    font-size: 13px;
}

/* Action Buttons */
QPushButton {
    background-color: #4f46e5;
    color: #ffffff;
    font-size: 13px;
    font-weight: 600;
    border: 1px solid #4338ca;
    border-radius: 6px;
    padding: 7px 16px;
}

QPushButton:hover {
    background-color: #4338ca;
}

QPushButton:pressed {
    background-color: #3730a3;
}

QPushButton#theme_btn {
    background-color: #1e293b;
    color: #cbd5e1;
    border: 1px solid #334155;
}

QPushButton#theme_btn:hover {
    background-color: #283548;
    color: #f8fafc;
}

QPushButton#ghost_btn {
    background-color: transparent;
    color: #94a3b8;
    border: 1px solid #334155;
}

QPushButton#ghost_btn:hover {
    background-color: #1e293b;
    color: #f8fafc;
}

/* Form Inputs */
QLabel.field_label {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 600;
    margin-top: 4px;
}

QLineEdit, QComboBox, QSpinBox, QDateEdit, QTextEdit {
    background-color: #111827;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
    selection-background-color: #4f46e5;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDateEdit:focus, QTextEdit:focus {
    border: 1px solid #6366f1;
}

QLineEdit::placeholder {
    color: #64748b;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
    border-left: 1px solid #334155;
}

QComboBox QAbstractItemView {
    background-color: #111827;
    color: #f8fafc;
    border: 1px solid #334155;
    selection-background-color: #4f46e5;
}

/* Checkboxes and Radio Buttons */
QCheckBox, QRadioButton {
    color: #e2e8f0;
    font-size: 13px;
    spacing: 8px;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #475569;
    border-radius: 4px;
    background-color: #111827;
}

QRadioButton::indicator {
    border-radius: 8px;
}

QCheckBox::indicator:checked, QRadioButton::indicator:checked {
    background-color: #4f46e5;
    border-color: #6366f1;
}

/* Slider */
QSlider::groove:horizontal {
    border: none;
    height: 6px;
    background: #334155;
    border-radius: 3px;
}

QSlider::sub-page:horizontal {
    background: #4f46e5;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #ffffff;
    border: 2px solid #4f46e5;
    width: 16px;
    margin-top: -5px;
    margin-bottom: -5px;
    border-radius: 8px;
}

QSlider::handle:horizontal:hover {
    background: #e0e7ff;
}

/* Progress Bar */
QProgressBar {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    text-align: center;
    color: #f8fafc;
    font-size: 11px;
    font-weight: 600;
    height: 18px;
}

QProgressBar::chunk {
    background-color: #4f46e5;
    border-radius: 5px;
}

/* ScrollBars */
QScrollBar:vertical {
    border: none;
    background: #0f172a;
    width: 8px;
    margin: 0;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #334155;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #475569;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
"""

LIGHT_APP_STYLESHEET = """
QMainWindow, QWidget#central_widget {
    background-color: #f1f5f9;
    color: #0f172a;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

QScrollArea#main_scroll {
    background: transparent;
    border: none;
}

QWidget#scroll_container {
    background: transparent;
}

/* Header Banner */
QFrame#banner_frame {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px 20px;
}

QLabel#app_title {
    color: #0f172a;
    font-size: 20px;
    font-weight: 700;
}

QLabel#app_subtitle {
    color: #64748b;
    font-size: 13px;
}

/* Action Buttons */
QPushButton {
    background-color: #4f46e5;
    color: #ffffff;
    font-size: 13px;
    font-weight: 600;
    border: 1px solid #4338ca;
    border-radius: 6px;
    padding: 7px 16px;
}

QPushButton:hover {
    background-color: #4338ca;
}

QPushButton:pressed {
    background-color: #3730a3;
}

QPushButton#theme_btn {
    background-color: #ffffff;
    color: #334155;
    border: 1px solid #cbd5e1;
}

QPushButton#theme_btn:hover {
    background-color: #f8fafc;
    color: #0f172a;
}

QPushButton#ghost_btn {
    background-color: transparent;
    color: #64748b;
    border: 1px solid #cbd5e1;
}

QPushButton#ghost_btn:hover {
    background-color: #ffffff;
    color: #0f172a;
}

/* Form Inputs */
QLabel.field_label {
    color: #475569;
    font-size: 12px;
    font-weight: 600;
    margin-top: 4px;
}

QLineEdit, QComboBox, QSpinBox, QDateEdit, QTextEdit {
    background-color: #ffffff;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
    selection-background-color: #4f46e5;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDateEdit:focus, QTextEdit:focus {
    border: 1px solid #4f46e5;
}

QLineEdit::placeholder {
    color: #94a3b8;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
    border-left: 1px solid #cbd5e1;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    selection-background-color: #4f46e5;
    selection-color: #ffffff;
}

/* Checkboxes and Radio Buttons */
QCheckBox, QRadioButton {
    color: #334155;
    font-size: 13px;
    spacing: 8px;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #94a3b8;
    border-radius: 4px;
    background-color: #ffffff;
}

QRadioButton::indicator {
    border-radius: 8px;
}

QCheckBox::indicator:checked, QRadioButton::indicator:checked {
    background-color: #4f46e5;
    border-color: #4338ca;
}

/* Slider */
QSlider::groove:horizontal {
    border: none;
    height: 6px;
    background: #cbd5e1;
    border-radius: 3px;
}

QSlider::sub-page:horizontal {
    background: #4f46e5;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #ffffff;
    border: 2px solid #4f46e5;
    width: 16px;
    margin-top: -5px;
    margin-bottom: -5px;
    border-radius: 8px;
}

QSlider::handle:horizontal:hover {
    background: #e0e7ff;
}

/* Progress Bar */
QProgressBar {
    background-color: #e2e8f0;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    text-align: center;
    color: #0f172a;
    font-size: 11px;
    font-weight: 600;
    height: 18px;
}

QProgressBar::chunk {
    background-color: #4f46e5;
    border-radius: 5px;
}

/* ScrollBars */
QScrollBar:vertical {
    border: none;
    background: #f1f5f9;
    width: 8px;
    margin: 0;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #cbd5e1;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #94a3b8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CollapsiblePane - Modern Design & Theming Demo")
        self.resize(680, 840)
        self.current_theme = "dark"

        # Central widget with scroll area for responsive layout
        central_widget = QWidget()
        central_widget.setObjectName("central_widget")
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setSpacing(16)

        # -------------------------------------------------------------
        # 1. Top Banner & Toolbar
        # -------------------------------------------------------------
        banner = QFrame()
        banner.setObjectName("banner_frame")
        banner_layout = QVBoxLayout(banner)
        banner_layout.setContentsMargins(16, 14, 16, 14)
        banner_layout.setSpacing(8)

        title_lbl = QLabel("CollapsiblePane Design System")
        title_lbl.setObjectName("app_title")
        subtitle_lbl = QLabel(
            "Unified stylesheets, seamless code customization, and smooth content-wrapping animations."
        )
        subtitle_lbl.setObjectName("app_subtitle")
        subtitle_lbl.setWordWrap(True)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        self.theme_toggle_btn = QPushButton("Switch to Light Mode")
        self.theme_toggle_btn.setObjectName("theme_btn")
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)

        self.toggle_all_btn = QPushButton("Toggle All Sections")
        self.toggle_all_btn.setObjectName("ghost_btn")
        self.toggle_all_btn.clicked.connect(self.toggle_all_sections)

        toolbar.addWidget(self.theme_toggle_btn)
        toolbar.addWidget(self.toggle_all_btn)
        toolbar.addStretch()

        banner_layout.addWidget(title_lbl)
        banner_layout.addWidget(subtitle_lbl)
        banner_layout.addLayout(toolbar)

        root_layout.addWidget(banner)

        # -------------------------------------------------------------
        # 2. Scrollable Section Container
        # -------------------------------------------------------------
        main_scroll = QScrollArea()
        main_scroll.setObjectName("main_scroll")
        main_scroll.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_content.setObjectName("scroll_container")
        self.sections_layout = QVBoxLayout(scroll_content)
        self.sections_layout.setContentsMargins(4, 4, 4, 4)
        self.sections_layout.setSpacing(14)

        # -------------------------------------------------------------
        # Section 1: Styled via Standard Stylesheet (QSS)
        # -------------------------------------------------------------
        self.pane_qss = CollapsiblePane(
            title="User Profile (Styled via Stylesheet)",
            animation_duration=220
        )
        self.pane_qss.set_item_count(12)
        self.pane_qss.set_content_widget(self.create_user_details_widget())
        self.pane_qss.set_collapsed(False)
        self.sections_layout.addWidget(self.pane_qss)

        # -------------------------------------------------------------
        # Section 2: Configured Dynamically via Code API
        # -------------------------------------------------------------
        self.pane_code = CollapsiblePane(
            title="Security & Preferences (Configured by Code)",
            animation_duration=220
        )
        self.apply_code_styling(self.pane_code, is_dark=True)
        self.pane_code.set_item_badge_style(
            text="Protected",
            bg_color="rgba(16, 185, 129, 0.18)",
            text_color="#10b981",
            border_color="rgba(16, 185, 129, 0.35)",
            border_radius=10,
            padding_horizontal=10
        )
        self.pane_code.set_content_widget(self.create_security_widget())
        self.pane_code.set_collapsed(False)
        self.sections_layout.addWidget(self.pane_code)

        self.sections_layout.addStretch()
        main_scroll.setWidget(scroll_content)
        root_layout.addWidget(main_scroll)

        # Apply initial dark stylesheet
        self.apply_app_theme("dark")

    def create_user_details_widget(self) -> QWidget:
        """Create a rich, beautiful user details form."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        # Input row 1: Name and Email
        row1 = QHBoxLayout()
        row1.setSpacing(10)

        col1 = QVBoxLayout()
        lbl_name = QLabel("Full Name:")
        lbl_name.setProperty("class", "field_label")
        name_edit = QLineEdit()
        name_edit.setPlaceholderText("e.g. Alex Morgan")
        col1.addWidget(lbl_name)
        col1.addWidget(name_edit)

        col2 = QVBoxLayout()
        lbl_email = QLabel("Email Address:")
        lbl_email.setProperty("class", "field_label")
        email_edit = QLineEdit()
        email_edit.setPlaceholderText("alex.morgan@example.com")
        col2.addWidget(lbl_email)
        col2.addWidget(email_edit)

        row1.addLayout(col1)
        row1.addLayout(col2)
        layout.addLayout(row1)

        # Category Dropdown
        lbl_cat = QLabel("Role & Department:")
        lbl_cat.setProperty("class", "field_label")
        combo = QComboBox()
        combo.addItems([
            "Senior Software Architect",
            "UI/UX Product Designer",
            "Security & Compliance Lead",
            "DevOps / SRE Engineer",
            "Data Science & AI Specialist"
        ])
        layout.addWidget(lbl_cat)
        layout.addWidget(combo)

        # Bio input
        lbl_bio = QLabel("Professional Bio:")
        lbl_bio.setProperty("class", "field_label")
        bio_edit = QTextEdit()
        bio_edit.setPlaceholderText("Brief overview of background and responsibilities...")
        bio_edit.setMaximumHeight(75)
        layout.addWidget(lbl_bio)
        layout.addWidget(bio_edit)

        # Submit button row
        btn_row = QHBoxLayout()
        btn_save = QPushButton("Save Profile")
        btn_discard = QPushButton("Discard")
        btn_discard.setObjectName("ghost_btn")
        btn_row.addWidget(btn_save)
        btn_row.addWidget(btn_discard)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        return widget

    def create_security_widget(self) -> QWidget:
        """Create preferences & security controls."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        # Checkboxes
        chk_2fa = QCheckBox("Enable Two-Factor Authentication (2FA)")
        chk_2fa.setChecked(True)
        chk_news = QCheckBox("Receive security advisory notifications")
        chk_news.setChecked(True)
        layout.addWidget(chk_2fa)
        layout.addWidget(chk_news)

        # Notification mode radio buttons
        lbl_mode = QLabel("Notification Frequency:")
        lbl_mode.setProperty("class", "field_label")
        layout.addWidget(lbl_mode)

        radio_row = QHBoxLayout()
        radio1 = QRadioButton("Real-time (Instant)")
        radio2 = QRadioButton("Daily Summary Digest")
        radio1.setChecked(True)
        bg = QButtonGroup(widget)
        bg.addButton(radio1)
        bg.addButton(radio2)
        radio_row.addWidget(radio1)
        radio_row.addWidget(radio2)
        radio_row.addStretch()
        layout.addLayout(radio_row)

        # Session slider & progress
        row_metrics = QHBoxLayout()
        row_metrics.setSpacing(12)

        col_slider = QVBoxLayout()
        lbl_session = QLabel("Session Timeout (Minutes):")
        lbl_session.setProperty("class", "field_label")
        slider = QSlider(Qt.Horizontal)
        slider.setRange(5, 120)
        slider.setValue(45)
        col_slider.addWidget(lbl_session)
        col_slider.addWidget(slider)

        col_prog = QVBoxLayout()
        lbl_health = QLabel("Security Score:")
        lbl_health.setProperty("class", "field_label")
        prog = QProgressBar()
        prog.setValue(88)
        col_prog.addWidget(lbl_health)
        col_prog.addWidget(prog)

        row_metrics.addLayout(col_slider)
        row_metrics.addLayout(col_prog)
        layout.addLayout(row_metrics)

        # Numeric inputs row
        row_spin = QHBoxLayout()
        spin_col = QVBoxLayout()
        lbl_spin = QLabel("Max Concurrent Sessions:")
        lbl_spin.setProperty("class", "field_label")
        spin = QSpinBox()
        spin.setValue(3)
        spin_col.addWidget(lbl_spin)
        spin_col.addWidget(spin)

        date_col = QVBoxLayout()
        lbl_date = QLabel("Next Password Audit:")
        lbl_date.setProperty("class", "field_label")
        date_edit = QDateEdit()
        date_edit.setDate(QDate.currentDate().addDays(90))
        date_col.addWidget(lbl_date)
        date_col.addWidget(date_edit)

        row_spin.addLayout(spin_col)
        row_spin.addLayout(date_col)
        layout.addLayout(row_spin)

        # Action button
        btn_apply = QPushButton("Apply Security Policies")
        layout.addWidget(btn_apply)

        return widget

    def apply_code_styling(self, pane: CollapsiblePane, is_dark: bool) -> None:
        """Demonstrate programmatic code customization on Section 2."""
        if is_dark:
            pane.set_header_style(
                background_color="#1e1b4b",  # Deep indigo slate
                text_color="#e0e7ff",
                border_color="#3730a3",
                border_width=1,
                border_radius=8,
                padding_vertical=7,
                padding_horizontal=12,
                font_size=13,
                font_weight="600",
                hover_color="#312e81"
            )
            pane.set_card_style(
                background="#0f172a",
                border="#1e293b",
                radius=8,
                padding=10
            )
            pane.set_content_text_style(color="#cbd5e1", font_size=13)
        else:
            pane.set_header_style(
                background_color="#eef2ff",  # Soft indigo wash
                text_color="#3730a3",
                border_color="#c7d2fe",
                border_width=1,
                border_radius=8,
                padding_vertical=7,
                padding_horizontal=12,
                font_size=13,
                font_weight="600",
                hover_color="#e0e7ff"
            )
            pane.set_card_style(
                background="#ffffff",
                border="#e2e8f0",
                radius=8,
                padding=10
            )
            pane.set_content_text_style(color="#334155", font_size=13)

    def apply_app_theme(self, theme: str) -> None:
        """Apply theme across application, combining app styles and CollapsiblePane styles."""
        self.current_theme = theme
        is_dark = (theme == "dark")

        # Set application stylesheet
        app_css = DARK_APP_STYLESHEET if is_dark else LIGHT_APP_STYLESHEET
        pane_css = get_theme_stylesheet(Theme.DARK if is_dark else Theme.LIGHT)
        QApplication.instance().setStyleSheet(app_css + "\n" + pane_css)

        # Update Section 1 via stylesheet theme preset
        self.pane_qss.apply_theme(Theme.DARK if is_dark else Theme.LIGHT)

        # Update Section 2 via programmatic code API
        self.apply_code_styling(self.pane_code, is_dark=is_dark)

        # Update button text
        if is_dark:
            self.theme_toggle_btn.setText("Switch to Light Mode")
        else:
            self.theme_toggle_btn.setText("Switch to Dark Mode")

    def toggle_theme(self) -> None:
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_app_theme(new_theme)

    def toggle_all_sections(self) -> None:
        """Simultaneously toggle all panes to showcase smooth animation without snapping."""
        target_state = not self.pane_qss.is_expanded
        self.pane_qss.toggle(target_state)
        self.pane_code.toggle(target_state)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
