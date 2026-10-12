from typing import Optional, Union, Dict, Any
from PySide6.QtCore import (
    Qt, QPropertyAnimation, QParallelAnimationGroup,
    QEasingCurve, Signal, QSize, QAbstractAnimation
)
from PySide6.QtWidgets import (
    QWidget, QScrollArea, QGridLayout, QSizePolicy,
    QGraphicsOpacityEffect, QFrame, QLabel,
    QHBoxLayout, QGraphicsDropShadowEffect
)
from PySide6.QtGui import QColor, QIcon, QPixmap, QMouseEvent


class Theme:
    """Predefined themes and design tokens for CollapsiblePane."""
    DARK = "dark"
    LIGHT = "light"
    INDIGO = "indigo"
    SLATE = "slate"


THEME_PALETTES: Dict[str, Dict[str, Any]] = {
    "dark": {
        "header_bg": "#1e293b",
        "header_hover": "#283548",
        "header_text": "#f8fafc",
        "header_border": "#334155",
        "header_border_width": 1,
        "border_radius": 8,
        "chevron_color": "#94a3b8",
        "badge_bg": "rgba(99, 102, 241, 0.18)",
        "badge_text": "#a5b4fc",
        "badge_border": "rgba(99, 102, 241, 0.35)",
        "card_bg": "#0f172a",
        "card_border": "#1e293b",
        "card_text": "#cbd5e1",
    },
    "light": {
        "header_bg": "#f8fafc",
        "header_hover": "#f1f5f9",
        "header_text": "#0f172a",
        "header_border": "#e2e8f0",
        "header_border_width": 1,
        "border_radius": 8,
        "chevron_color": "#64748b",
        "badge_bg": "#e0e7ff",
        "badge_text": "#4338ca",
        "badge_border": "#c7d2fe",
        "card_bg": "#ffffff",
        "card_border": "#e2e8f0",
        "card_text": "#334155",
    },
    "indigo": {
        "header_bg": "#4f46e5",
        "header_hover": "#4338ca",
        "header_text": "#ffffff",
        "header_border": "#4338ca",
        "header_border_width": 1,
        "border_radius": 8,
        "chevron_color": "rgba(255, 255, 255, 0.85)",
        "badge_bg": "rgba(255, 255, 255, 0.2)",
        "badge_text": "#ffffff",
        "badge_border": "rgba(255, 255, 255, 0.35)",
        "card_bg": "#f8fafc",
        "card_border": "#e2e8f0",
        "card_text": "#334155",
    },
    "slate": {
        "header_bg": "#334155",
        "header_hover": "#475569",
        "header_text": "#f8fafc",
        "header_border": "#475569",
        "header_border_width": 1,
        "border_radius": 8,
        "chevron_color": "#cbd5e1",
        "badge_bg": "rgba(255, 255, 255, 0.15)",
        "badge_text": "#f8fafc",
        "badge_border": "rgba(255, 255, 255, 0.25)",
        "card_bg": "#1e293b",
        "card_border": "#334155",
        "card_text": "#e2e8f0",
    },
}


def get_theme_stylesheet(theme: Union[str, Dict[str, Any]] = "dark") -> str:
    """
    Generate a standard QSS stylesheet for the given theme preset or custom token dict.
    Styles apply to standard object names:
      - QFrame#header_frame
      - QLabel#title_label
      - QLabel#chevron_label
      - QLabel#count_label
      - QScrollArea#content_area
    """
    if isinstance(theme, str):
        tokens = THEME_PALETTES.get(theme.lower(), THEME_PALETTES["dark"])
    elif isinstance(theme, dict):
        base = THEME_PALETTES["dark"].copy()
        base.update(theme)
        tokens = base
    else:
        tokens = THEME_PALETTES["dark"]

    return f"""
        CollapsiblePane {{
            background: transparent;
        }}
        QFrame#header_frame {{
            background-color: {tokens['header_bg']};
            border: {tokens['header_border_width']}px solid {tokens['header_border']};
            border-radius: {tokens['border_radius']}px;
            padding: 6px 10px;
        }}
        QFrame#header_frame:hover {{
            background-color: {tokens['header_hover']};
        }}
        QLabel#title_label {{
            color: {tokens['header_text']};
            font-size: 13px;
            font-weight: 600;
        }}
        QLabel#chevron_label {{
            color: {tokens['chevron_color']};
            font-size: 14px;
            font-weight: bold;
        }}
        QLabel#count_label {{
            background-color: {tokens['badge_bg']};
            color: {tokens['badge_text']};
            border: 1px solid {tokens['badge_border']};
            border-radius: 10px;
            padding: 2px 8px;
            font-size: 11px;
            font-weight: 600;
            min-width: 24px;
        }}
        QScrollArea#content_area {{
            background-color: {tokens['card_bg']};
            border: 1px solid {tokens['card_border']};
            border-radius: {tokens['border_radius']}px;
            padding: 8px;
        }}
    """


DEFAULT_STYLESHEET = get_theme_stylesheet("dark")


class _CollapsibleScrollArea(QScrollArea):
    """
    Custom QScrollArea tailored for CollapsiblePane.
    Accurately computes its sizeHint based on the contained widget,
    preventing Qt's default 384px height clamp from collapsing the layout.
    """
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._max_content_height: Optional[int] = None
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def set_max_content_height(self, max_height: Optional[int]) -> None:
        """Set an optional maximum height for the content area before scrollbars appear."""
        self._max_content_height = max_height
        self.updateGeometry()

    def max_content_height(self) -> Optional[int]:
        """Return the maximum content height constraint, if configured."""
        return self._max_content_height

    def sizeHint(self) -> QSize:
        w = self.widget()
        if w is not None:
            w_hint = w.sizeHint()
            target_h = w_hint.height()
            if self._max_content_height is not None and self._max_content_height > 0:
                target_h = min(target_h, self._max_content_height)
            return QSize(w_hint.width(), target_h)
        return super().sizeHint()

    def minimumSizeHint(self) -> QSize:
        return QSize(0, 0)


class CollapsiblePane(QWidget):
    """
    A sleek, customizable, animated collapsible container widget for PySide6.
    Inspired by JavaFX's TitledPane.
    Supports standard stylesheet styling (QSS) as well as full programmatic configuration.
    """
    toggled: Signal = Signal(bool)

    def __init__(self, title: str = "", animation_duration: int = 200, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName("collapsible_pane")
        self._text_style: str = ""
        self._card_style: str = ""
        self.animation_duration: int = animation_duration
        self._expanded: bool = False
        self._use_qicon: bool = False
        self._collapsed_icon: Union[str, QIcon] = "▸"
        self._expanded_icon: Union[str, QIcon] = "▾"
        self._target_content_height: int = 0
        self._target_total_height: int = 0

        # --- Header Frame ---
        self.header_frame: QFrame = QFrame(self)
        self.header_frame.setObjectName("header_frame")
        self.header_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.header_frame.setCursor(Qt.PointingHandCursor)
        self.header_frame.setAutoFillBackground(False)

        self.header_layout: QHBoxLayout = QHBoxLayout(self.header_frame)
        self.header_layout.setContentsMargins(10, 6, 10, 6)
        self.header_layout.setSpacing(8)

        self.chevron_label: QLabel = QLabel(self._collapsed_icon, self.header_frame)
        self.chevron_label.setObjectName("chevron_label")

        self.title_label: QLabel = QLabel(title, self.header_frame)
        self.title_label.setObjectName("title_label")

        self.count_label: QLabel = QLabel("", self.header_frame)
        self.count_label.setObjectName("count_label")
        self.count_label.setAlignment(Qt.AlignCenter)
        self.count_label.setVisible(False)

        self.header_layout.addWidget(self.chevron_label)
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.count_label)

        # --- Content Area ---
        self.content_area: _CollapsibleScrollArea = _CollapsibleScrollArea(self)
        self.content_area.setObjectName("content_area")
        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.content_area.setMaximumHeight(0)
        self.content_area.setMinimumHeight(0)

        # --- Opacity effect on viewport for smooth fade ---
        self.opacity_effect: QGraphicsOpacityEffect = QGraphicsOpacityEffect(self.content_area.viewport())
        self.content_area.viewport().setGraphicsEffect(self.opacity_effect)
        self.opacity_animation: QPropertyAnimation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(self.animation_duration)

        # --- Main Layout ---
        self.main_layout: QGridLayout = QGridLayout(self)
        self.main_layout.setVerticalSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.header_frame, 0, 0)
        self.main_layout.addWidget(self.content_area, 1, 0)

        # --- Height Animations ---
        self._anim_self_min: QPropertyAnimation = QPropertyAnimation(self, b"minimumHeight")
        self._anim_self_max: QPropertyAnimation = QPropertyAnimation(self, b"maximumHeight")
        self._anim_content_max: QPropertyAnimation = QPropertyAnimation(self.content_area, b"maximumHeight")

        self.toggle_animation: QParallelAnimationGroup = QParallelAnimationGroup(self)
        self.toggle_animation.addAnimation(self._anim_self_max)
        self.toggle_animation.addAnimation(self._anim_content_max)
        self.toggle_animation.addAnimation(self.opacity_animation)
        self.toggle_animation.finished.connect(self._on_animation_finished)

        # --- Click handler ---
        self.header_frame.mousePressEvent = self._on_header_mouse_press

        # --- Translucent attributes ---
        self.chevron_label.setAttribute(Qt.WA_TranslucentBackground)
        self.title_label.setAttribute(Qt.WA_TranslucentBackground)

        # Apply default standard stylesheet
        self.setStyleSheet(DEFAULT_STYLESHEET)

    def _on_header_mouse_press(self, event: QMouseEvent) -> None:
        """Handle header click with left-button check."""
        if event.button() == Qt.LeftButton:
            self.toggle(not self._expanded)
            event.accept()
        else:
            event.ignore()

    def sizeHint(self) -> QSize:
        """Provide accurate size hint reflecting header and current content height."""
        header_hint = self.header_frame.sizeHint()
        if not self._expanded:
            return header_hint
        content_hint = self.content_area.sizeHint()
        spacing = self.main_layout.verticalSpacing()
        h = header_hint.height() + self.content_area.maximumHeight() + spacing
        return QSize(max(header_hint.width(), content_hint.width()), h)

    def minimumSizeHint(self) -> QSize:
        """Minimum size hint is at least the header frame."""
        return self.header_frame.sizeHint()

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------
    @property
    def is_expanded(self) -> bool:
        """Return True if the pane is currently expanded."""
        return self._expanded

    @is_expanded.setter
    def is_expanded(self, expand: bool) -> None:
        """Set the expanded state (animated)."""
        self.toggle(expand)

    @property
    def content_widget(self) -> Optional[QWidget]:
        """Return the current child widget inside the content area, if any."""
        return self.content_area.widget()

    @property
    def title(self) -> str:
        """Return the header title text."""
        return self.title_label.text()

    @title.setter
    def title(self, title: str) -> None:
        """Set the header title text."""
        self.set_title(title)

    # -------------------------------------------------------------------------
    # Content and header management
    # -------------------------------------------------------------------------
    def set_content_widget(self, widget: QWidget) -> None:
        """Attach content widget inside the collapsible area."""
        self.clear_widget()
        self.content_area.setWidget(widget)
        if self._text_style:
            widget.setStyleSheet(self._text_style)
        widget.adjustSize()
        self.updateGeometry()

    def clear_widget(self) -> None:
        """Remove and delete the content widget if present."""
        old = self.content_area.takeWidget()
        if old is not None:
            old.deleteLater()
        self.updateGeometry()

    def set_title(self, title: str) -> None:
        """Update header title."""
        self.title_label.setText(title)

    def set_max_content_height(self, max_height: Optional[int]) -> None:
        """Set maximum height constraint for expanded content before scrollbars appear."""
        self.content_area.set_max_content_height(max_height)

    # -------------------------------------------------------------------------
    # Theming & Stylesheet API
    # -------------------------------------------------------------------------
    def apply_theme(self, theme: Union[str, Dict[str, Any]]) -> None:
        """Apply a built-in theme ('dark', 'light', 'indigo', 'slate') or custom token dictionary."""
        self.setStyleSheet(get_theme_stylesheet(theme))

    def set_header_style(
        self,
        background_color: str = "#1e293b",
        text_color: str = "#f8fafc",
        border_color: str = "#334155",
        border_width: int = 1,
        border_radius: int = 8,
        padding_vertical: int = 6,
        padding_horizontal: int = 10,
        font_size: int = 13,
        font_weight: str = "600",
        hover_color: Optional[str] = "#283548"
    ) -> None:
        """Customize the header look dynamically via code."""
        hover_block = f"""
        QFrame#header_frame:hover {{
            background-color: {hover_color};
        }}
        """ if hover_color else ""

        self.header_frame.setStyleSheet(f"""
            QFrame#header_frame {{
                background-color: {background_color};
                border: {border_width}px solid {border_color};
                border-radius: {border_radius}px;
                padding: {padding_vertical}px {padding_horizontal}px;
                background-clip: border;
            }}
            {hover_block}
        """)

        self.title_label.setStyleSheet(
            f"color: {text_color}; font-size: {font_size}px; font-weight: {font_weight};"
        )

    # Backward compatibility alias
    set_title_bar_style = set_header_style

    def set_chevron_icons(self, collapsed_icon: Union[str, QIcon], expanded_icon: Union[str, QIcon]) -> None:
        """Set custom icons or text for the chevron."""
        image_exts = (".svg", ".png", ".jpg", ".jpeg", ".bmp", ".ico")

        if isinstance(collapsed_icon, QIcon) and isinstance(expanded_icon, QIcon):
            self._use_qicon = True
            self._collapsed_icon = collapsed_icon
            self._expanded_icon = expanded_icon
            active_icon = self._expanded_icon if self._expanded else self._collapsed_icon
            self.chevron_label.setText("")
            self.chevron_label.setPixmap(active_icon.pixmap(16, 16))

        elif isinstance(collapsed_icon, str) and collapsed_icon.lower().endswith(image_exts):
            self._use_qicon = True
            self._collapsed_icon = QIcon(collapsed_icon)
            self._expanded_icon = QIcon(expanded_icon)
            active_icon = self._expanded_icon if self._expanded else self._collapsed_icon
            self.chevron_label.setText("")
            self.chevron_label.setPixmap(active_icon.pixmap(16, 16))

        else:
            self._use_qicon = False
            self._collapsed_icon = collapsed_icon
            self._expanded_icon = expanded_icon
            self.chevron_label.setPixmap(QPixmap())
            self.chevron_label.setText(self._expanded_icon if self._expanded else self._collapsed_icon)

    def set_card_style(
        self,
        background: str = "#0f172a",
        border: str = "#1e293b",
        radius: int = 8,
        padding: int = 8,
        shadow_only: bool = False
    ) -> None:
        """Customize expanded content card style dynamically via code."""
        if shadow_only:
            self.content_area.setAutoFillBackground(True)
            self.content_area.setAttribute(Qt.WA_TranslucentBackground, True)

        self._card_style = f"""
            QScrollArea#content_area {{
                background-color: {background};
                border: 1px solid {border};
                border-radius: {radius}px;
                padding: {padding}px;
            }}
        """
        self.content_area.setStyleSheet(self._card_style)

    # Backward compatibility alias
    set_content_style = set_card_style

    def set_card_shadow(self, color: str = "#000000", blur: int = 20, offset_y: int = 4) -> None:
        """Add a drop shadow under the expanded content."""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blur)
        shadow.setOffset(0, offset_y)
        shadow.setColor(QColor(color))
        self.content_area.setGraphicsEffect(shadow)

    def set_content_text_style(self, color: str = "#cbd5e1", font_size: int = 13) -> None:
        """Change default text styling for the content area."""
        self._text_style = f"color: {color}; font-size: {font_size}px;"
        content = self.content_area.widget()
        if content:
            content.setStyleSheet(self._text_style)

    def set_title_style(
        self,
        color: str = "#f8fafc",
        font_size: int = 13,
        font_weight: str = "600",
        italic: bool = False
    ) -> None:
        """Style the title text dynamically."""
        style = f"""
            color: {color};
            font-size: {font_size}px;
            font-weight: {font_weight};
            {'font-style: italic;' if italic else ''}
        """
        self.title_label.setStyleSheet(style)

    def set_item_count(self, count: Optional[int], show_badge: bool = True) -> None:
        """Display an item count badge."""
        if count is None or not show_badge:
            self.count_label.setText("")
            self.count_label.setVisible(False)
            return

        self.count_label.setVisible(True)
        self.count_label.setText(str(count))

    def set_item_badge_style(
        self,
        text: Optional[str] = None,
        bg_color: str = "rgba(99, 102, 241, 0.18)",
        text_color: str = "#a5b4fc",
        border_color: str = "rgba(99, 102, 241, 0.35)",
        border_radius: int = 10,
        padding_vertical: int = 2,
        padding_horizontal: int = 8,
        font_size: int = 11,
        font_weight: str = "600",
        shadow: bool = False,
        min_width: int = 24
    ) -> None:
        """Dynamically style the badge (count label) via code."""
        if text is not None:
            self.count_label.setText(str(text))
            self.count_label.setVisible(True)

        style = f"""
            QLabel#count_label {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: {border_radius}px;
                border: 1px solid {border_color};
                padding: {padding_vertical}px {padding_horizontal}px;
                font-size: {font_size}px;
                font-weight: {font_weight};
                min-width: {min_width}px;
                qproperty-alignment: AlignCenter;
            }}
        """
        self.count_label.setStyleSheet(style)

        if shadow:
            shadow_effect = QGraphicsDropShadowEffect(self.count_label)
            shadow_effect.setBlurRadius(10)
            shadow_effect.setOffset(0, 2)
            shadow_effect.setColor(QColor(0, 0, 0, 40))
            self.count_label.setGraphicsEffect(shadow_effect)
        else:
            self.count_label.setGraphicsEffect(None)

    # -------------------------------------------------------------------------
    # Behavior controls
    # -------------------------------------------------------------------------
    def set_collapsed(self, collapsed: bool = True) -> None:
        """Force collapse/expand state immediately without animation."""
        self._expanded = not collapsed

        # Update chevron
        if self._use_qicon:
            icon = self._collapsed_icon if collapsed else self._expanded_icon
            if isinstance(icon, QIcon):
                self.chevron_label.setPixmap(icon.pixmap(16, 16))
            self.chevron_label.setText("")
        else:
            self.chevron_label.setPixmap(QPixmap())
            self.chevron_label.setText(self._collapsed_icon if collapsed else self._expanded_icon)

        collapsed_height = self.header_frame.sizeHint().height()

        if collapsed:
            self.content_area.setMaximumHeight(0)
            self.content_area.setMinimumHeight(0)
            self.setMaximumHeight(collapsed_height)
            self.setMinimumHeight(collapsed_height)
            self.opacity_effect.setOpacity(0.0)
        else:
            content = self.content_area.widget()
            content_height = content.sizeHint().height() if content else 0
            max_h = self.content_area.max_content_height()
            if max_h is not None and max_h > 0:
                content_height = min(content_height, max_h)

            total_height = collapsed_height + content_height + self.main_layout.verticalSpacing()
            self.content_area.setMaximumHeight(content_height)
            self.content_area.setMinimumHeight(0)
            self.setMaximumHeight(total_height)
            self.setMinimumHeight(collapsed_height)
            self.opacity_effect.setOpacity(1.0)

        self.updateGeometry()

    # -------------------------------------------------------------------------
    # Animation toggle
    # -------------------------------------------------------------------------
    def toggle(self, expand: bool) -> None:
        """Animate expanding or collapsing smoothly without overshoot or bounce-back."""
        if self._expanded == expand:
            return

        self._expanded = expand
        self.toggled.emit(expand)

        # Update chevron
        if self._use_qicon:
            icon = self._expanded_icon if expand else self._collapsed_icon
            if isinstance(icon, QIcon):
                self.chevron_label.setPixmap(icon.pixmap(16, 16))
            self.chevron_label.setText("")
        else:
            self.chevron_label.setPixmap(QPixmap())
            self.chevron_label.setText(self._expanded_icon if expand else self._collapsed_icon)

        content = self.content_area.widget()
        if not content:
            return

        content.adjustSize()
        content_height = content.sizeHint().height()
        max_h = self.content_area.max_content_height()
        if max_h is not None and max_h > 0:
            content_height = min(content_height, max_h)

        collapsed_height = self.header_frame.sizeHint().height()
        total_target_height = collapsed_height + content_height + self.main_layout.verticalSpacing()

        self._target_content_height = content_height
        self._target_total_height = total_target_height

        # Stop ongoing animation cleanly if active
        if self.toggle_animation.state() == QAbstractAnimation.State.Running:
            self.toggle_animation.stop()

        curr_self_height = self.height()
        curr_content_height = self.content_area.height()
        curr_opacity = self.opacity_effect.opacity()

        target_self_height = total_target_height if expand else collapsed_height
        target_content_height = content_height if expand else 0
        target_opacity = 1.0 if expand else 0.0

        # Animate self maximum height
        self._anim_self_max.setStartValue(curr_self_height)
        self._anim_self_max.setEndValue(target_self_height)
        self._anim_self_max.setDuration(self.animation_duration)
        self._anim_self_max.setEasingCurve(QEasingCurve.OutCubic)

        # Animate content area maximum height
        self._anim_content_max.setStartValue(curr_content_height)
        self._anim_content_max.setEndValue(target_content_height)
        self._anim_content_max.setDuration(self.animation_duration)
        self._anim_content_max.setEasingCurve(QEasingCurve.OutCubic)

        # Animate opacity
        self.opacity_animation.setStartValue(curr_opacity)
        self.opacity_animation.setEndValue(target_opacity)
        self.opacity_animation.setDuration(self.animation_duration)
        self.opacity_animation.setEasingCurve(QEasingCurve.OutCubic)

        self.toggle_animation.start()

    def _on_animation_finished(self) -> None:
        """Handle animation completion cleanly."""
        collapsed_height = self.header_frame.sizeHint().height()
        if not self._expanded:
            self.content_area.setMaximumHeight(0)
            self.setMaximumHeight(collapsed_height)
            self.setMinimumHeight(collapsed_height)
        else:
            self.content_area.setMaximumHeight(self._target_content_height)
            self.setMaximumHeight(self._target_total_height)
            self.setMinimumHeight(collapsed_height)
        self.updateGeometry()
