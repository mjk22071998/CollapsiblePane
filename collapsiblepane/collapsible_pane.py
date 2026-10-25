from typing import Optional, Union, Dict, Any, List
from PySide6.QtCore import (
    Qt, QPropertyAnimation, QParallelAnimationGroup,
    QEasingCurve, Signal, QSize, QAbstractAnimation
)
from PySide6.QtWidgets import (
    QWidget, QScrollArea, QGridLayout, QSizePolicy,
    QGraphicsOpacityEffect, QFrame, QLabel,
    QHBoxLayout, QVBoxLayout, QGraphicsDropShadowEffect
)
from PySide6.QtGui import QColor, QIcon, QPixmap, QMouseEvent, QKeyEvent


class Theme:
    """Predefined themes and design tokens for CollapsiblePane."""
    DARK = "dark"
    LIGHT = "light"
    INDIGO = "indigo"
    SLATE = "slate"
    MODENA = "modena"
    MODENA_DARK = "modena_dark"
    CASPIAN = "caspian"


THEME_PALETTES: Dict[str, Dict[str, Any]] = {
    "dark": {
        "header_bg": "#1e293b",
        "header_hover": "#283548",
        "header_text": "#f8fafc",
        "header_border": "#334155",
        "header_border_width": 1,
        "border_radius": 8,
        "focus_border": "#6366f1",
        "chevron_color": "#94a3b8",
        "badge_bg": "rgba(99, 102, 241, 0.18)",
        "badge_text": "#a5b4fc",
        "badge_border": "rgba(99, 102, 241, 0.35)",
        "card_bg": "#0f172a",
        "card_border": "#1e293b",
        "card_text": "#cbd5e1",
        "unified_box": False,
    },
    "light": {
        "header_bg": "#f8fafc",
        "header_hover": "#f1f5f9",
        "header_text": "#0f172a",
        "header_border": "#e2e8f0",
        "header_border_width": 1,
        "border_radius": 8,
        "focus_border": "#4f46e5",
        "chevron_color": "#64748b",
        "badge_bg": "#e0e7ff",
        "badge_text": "#4338ca",
        "badge_border": "#c7d2fe",
        "card_bg": "#ffffff",
        "card_border": "#e2e8f0",
        "card_text": "#334155",
        "unified_box": False,
    },
    "indigo": {
        "header_bg": "#4f46e5",
        "header_hover": "#4338ca",
        "header_text": "#ffffff",
        "header_border": "#4338ca",
        "header_border_width": 1,
        "border_radius": 8,
        "focus_border": "#ffffff",
        "chevron_color": "rgba(255, 255, 255, 0.85)",
        "badge_bg": "rgba(255, 255, 255, 0.2)",
        "badge_text": "#ffffff",
        "badge_border": "rgba(255, 255, 255, 0.35)",
        "card_bg": "#f8fafc",
        "card_border": "#e2e8f0",
        "card_text": "#334155",
        "unified_box": False,
    },
    "slate": {
        "header_bg": "#334155",
        "header_hover": "#475569",
        "header_text": "#f8fafc",
        "header_border": "#475569",
        "header_border_width": 1,
        "border_radius": 8,
        "focus_border": "#60a5fa",
        "chevron_color": "#cbd5e1",
        "badge_bg": "rgba(255, 255, 255, 0.15)",
        "badge_text": "#f8fafc",
        "badge_border": "rgba(255, 255, 255, 0.25)",
        "card_bg": "#1e293b",
        "card_border": "#334155",
        "card_text": "#e2e8f0",
        "unified_box": False,
    },
    "modena": {
        "header_bg": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #fcfcfc, stop:0.08 #f5f5f5, stop:1 #e2e2e2)",
        "header_hover": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:0.08 #fafafa, stop:1 #ebebeb)",
        "header_text": "#222222",
        "header_border": "#b5b5b5",
        "header_border_width": 1,
        "border_radius": 4,
        "focus_border": "#0096C9",
        "chevron_color": "#4a5568",
        "collapsed_icon": "▶",
        "expanded_icon": "▼",
        "badge_bg": "rgba(0, 150, 201, 0.15)",
        "badge_text": "#007ba6",
        "badge_border": "rgba(0, 150, 201, 0.35)",
        "card_bg": "#ffffff",
        "card_border": "#b5b5b5",
        "card_text": "#2d3748",
        "unified_box": True,
    },
    "modena_dark": {
        "header_bg": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3c3f41, stop:0.08 #383a3c, stop:1 #2f3133)",
        "header_hover": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #474a4d, stop:0.08 #404345, stop:1 #353739)",
        "header_text": "#e0e0e0",
        "header_border": "#26282a",
        "header_border_width": 1,
        "border_radius": 4,
        "focus_border": "#389fd6",
        "chevron_color": "#9e9e9e",
        "collapsed_icon": "▶",
        "expanded_icon": "▼",
        "badge_bg": "rgba(56, 159, 214, 0.2)",
        "badge_text": "#7cc4ef",
        "badge_border": "rgba(56, 159, 214, 0.4)",
        "card_bg": "#2b2b2b",
        "card_border": "#26282a",
        "card_text": "#cccccc",
        "unified_box": True,
    },
    "caspian": {
        "header_bg": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #e8ecf0, stop:0.15 #d8dfe6, stop:1 #bdc8d4)",
        "header_hover": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f0f4f8, stop:0.15 #e2e8ef, stop:1 #cad4df)",
        "header_text": "#1a202c",
        "header_border": "#8ea3b8",
        "header_border_width": 1,
        "border_radius": 4,
        "focus_border": "#1c75bc",
        "chevron_color": "#2d3748",
        "collapsed_icon": "▶",
        "expanded_icon": "▼",
        "badge_bg": "rgba(28, 117, 188, 0.15)",
        "badge_text": "#1c75bc",
        "badge_border": "rgba(28, 117, 188, 0.35)",
        "card_bg": "#f7fafc",
        "card_border": "#8ea3b8",
        "card_text": "#2d3748",
        "unified_box": True,
    },
}


def get_theme_stylesheet(
    theme: Union[str, Dict[str, Any]] = "dark",
    unified_box: bool = False,
    is_expanded: bool = False
) -> str:
    """
    Generate a standard QSS stylesheet for the given theme preset or custom token dict.
    Supports JavaFX Modena styling with unified box borders, gradient headers, and focus rings.
    """
    if isinstance(theme, str):
        tokens = THEME_PALETTES.get(theme.lower(), THEME_PALETTES["dark"])
    elif isinstance(theme, dict):
        base = THEME_PALETTES["dark"].copy()
        base.update(theme)
        tokens = base
    else:
        tokens = THEME_PALETTES["dark"]

    is_unified = unified_box or tokens.get("unified_box", False)
    radius = tokens.get("border_radius", 8)
    border_w = tokens.get("header_border_width", 1)
    header_border = tokens.get("header_border", "#334155")
    card_border = tokens.get("card_border", header_border)
    focus_border = tokens.get("focus_border", "#0096C9")

    if is_unified:
        if is_expanded:
            header_radius_rules = f"""
                border-top-left-radius: {radius}px;
                border-top-right-radius: {radius}px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
                border-bottom: {border_w}px solid {header_border};
            """
            content_radius_rules = f"""
                border-top: none;
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
                border-bottom-left-radius: {radius}px;
                border-bottom-right-radius: {radius}px;
            """
        else:
            header_radius_rules = f"border-radius: {radius}px;"
            content_radius_rules = f"border-radius: {radius}px;"
    else:
        header_radius_rules = f"border-radius: {radius}px;"
        content_radius_rules = f"border-radius: {radius}px;"

    return f"""
        CollapsiblePane {{
            background: transparent;
        }}
        QFrame#header_frame {{
            background: {tokens['header_bg']};
            border: {border_w}px solid {header_border};
            {header_radius_rules}
            padding: 6px 10px;
            outline: none;
        }}
        QFrame#header_frame:hover {{
            background: {tokens['header_hover']};
        }}
        QFrame#header_frame:focus {{
            border: {border_w}px solid {focus_border};
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
            border: {border_w}px solid {card_border};
            {content_radius_rules}
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
    Supports standard stylesheet styling (QSS), full programmatic configuration,
    and the authentic JavaFX Modena look and feel.
    """
    toggled: Signal = Signal(bool)

    def __init__(
        self,
        title: str = "",
        animation_duration: int = 200,
        parent: Optional[QWidget] = None,
        *,
        collapsible: bool = True,
        animated: bool = True,
        unified_box: bool = False,
        expanded: bool = False
    ):
        super().__init__(parent)
        self.setObjectName("collapsible_pane")
        self._text_style: str = ""
        self._card_style: str = ""
        self.animation_duration: int = animation_duration
        self._expanded: bool = False
        self._collapsible: bool = collapsible
        self._animated: bool = animated
        self._unified_box: bool = unified_box
        self._current_theme: Union[str, Dict[str, Any]] = "dark"
        self._custom_icons_set: bool = False
        self._graphic_widget: Optional[QWidget] = None
        self._use_qicon: bool = False
        self._collapsed_icon: Union[str, QIcon] = "▸"
        self._expanded_icon: Union[str, QIcon] = "▾"
        self._target_content_height: int = 0
        self._target_total_height: int = 0

        # --- Header Frame ---
        self.header_frame: QFrame = QFrame(self)
        self.header_frame.setObjectName("header_frame")
        self.header_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.header_frame.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.header_frame.setCursor(Qt.PointingHandCursor if self._collapsible else Qt.ArrowCursor)
        self.header_frame.setAutoFillBackground(False)

        self.header_layout: QHBoxLayout = QHBoxLayout(self.header_frame)
        self.header_layout.setContentsMargins(10, 6, 10, 6)
        self.header_layout.setSpacing(8)

        self.chevron_label: QLabel = QLabel(self._collapsed_icon, self.header_frame)
        self.chevron_label.setObjectName("chevron_label")
        self.chevron_label.setVisible(self._collapsible)

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

        # --- Click & Keyboard handlers ---
        self.header_frame.mousePressEvent = self._on_header_mouse_press
        self.header_frame.keyPressEvent = self._on_header_key_press

        # --- Translucent attributes ---
        self.chevron_label.setAttribute(Qt.WA_TranslucentBackground)
        self.title_label.setAttribute(Qt.WA_TranslucentBackground)

        # Apply default standard stylesheet
        self._refresh_stylesheet()

        # Handle initial expanded state if requested (non-collapsible panes are permanently expanded)
        if expanded or not self._collapsible:
            self._expanded = True
            self.set_collapsed(False)

    def showEvent(self, event) -> None:
        """Ensure an expanded pane is properly dimensioned when first shown."""
        super().showEvent(event)
        if self._expanded and self.content_area.widget() is not None:
            if self.content_area.maximumHeight() == 0:
                self.set_collapsed(False)

    def _on_header_mouse_press(self, event: QMouseEvent) -> None:
        """Handle header click with left-button check and focus acquisition."""
        if event.button() == Qt.LeftButton:
            self.header_frame.setFocus()
            if self._collapsible:
                self.toggle(not self._expanded)
            event.accept()
        else:
            event.ignore()

    def _on_header_key_press(self, event: QKeyEvent) -> None:
        """Handle keyboard activation (Space, Return, Enter) to toggle."""
        if event.key() in (Qt.Key.Key_Space, Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if self._collapsible:
                self.toggle(not self._expanded)
            event.accept()
        else:
            QFrame.keyPressEvent(self.header_frame, event)

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
    # Properties & JavaFX parity
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
    def is_collapsible(self) -> bool:
        """Return True if the pane can be collapsed by the user (JavaFX collapsibleProperty)."""
        return self._collapsible

    @is_collapsible.setter
    def is_collapsible(self, collapsible: bool) -> None:
        self.set_collapsible(collapsible)

    def set_collapsible(self, collapsible: bool) -> None:
        """
        Set whether this pane can be collapsed by the user.
        Matches JavaFX's TitledPane.setCollapsible(boolean).
        If False, locks the pane in an expanded state and hides the chevron.
        """
        self._collapsible = collapsible
        if not collapsible:
            self._expanded = True
            self.set_collapsed(False)
            self.chevron_label.setVisible(False)
            self.header_frame.setCursor(Qt.ArrowCursor)
        else:
            self.chevron_label.setVisible(True)
            self.header_frame.setCursor(Qt.PointingHandCursor)

    @property
    def is_animated(self) -> bool:
        """Return True if expand/collapse transitions are animated (JavaFX animatedProperty)."""
        return self._animated

    @is_animated.setter
    def is_animated(self, animated: bool) -> None:
        self.set_animated(animated)

    def set_animated(self, animated: bool) -> None:
        """
        Set whether expand/collapse transitions are animated.
        Matches JavaFX's TitledPane.setAnimated(boolean).
        """
        self._animated = animated

    @property
    def unified_box(self) -> bool:
        """Return True if unified box mode is enabled (seamless JavaFX container border)."""
        return self._unified_box

    @unified_box.setter
    def unified_box(self, enabled: bool) -> None:
        self.set_unified_box(enabled)

    def set_unified_box(self, enabled: bool = True) -> None:
        """
        Configure whether header and content share a unified container border
        with dynamic corner rounding, matching JavaFX's single-panel visual design.
        """
        self._unified_box = enabled
        self._refresh_stylesheet()

    @property
    def graphic(self) -> Optional[QWidget]:
        """Return the current header graphic widget, if any (JavaFX graphicProperty)."""
        return self._graphic_widget

    def set_graphic(self, widget: Optional[QWidget]) -> None:
        """
        Set a graphic/icon widget inside the header next to the title.
        Directly mirrors JavaFX's TitledPane.setGraphic(Node).
        """
        if self._graphic_widget is not None:
            self.header_layout.removeWidget(self._graphic_widget)
            self._graphic_widget.deleteLater()
            self._graphic_widget = None

        if widget is not None:
            self._graphic_widget = widget
            # Insert at index 1: after chevron_label (0) and before title_label
            self.header_layout.insertWidget(1, widget)

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
        if self._expanded:
            self.set_collapsed(False)
        else:
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
        if self._expanded:
            self.set_collapsed(False)

    # -------------------------------------------------------------------------
    # Theming & Stylesheet API
    # -------------------------------------------------------------------------
    def _refresh_stylesheet(self) -> None:
        """Re-render the active stylesheet taking unified_box and expanded state into account."""
        self.setStyleSheet(
            get_theme_stylesheet(
                self._current_theme,
                unified_box=self._unified_box,
                is_expanded=self._expanded
            )
        )

    def apply_theme(self, theme: Union[str, Dict[str, Any]]) -> None:
        """
        Apply a built-in theme ('dark', 'light', 'indigo', 'slate', 'modena', 'modena_dark', 'caspian')
        or custom token dictionary.
        """
        self._current_theme = theme
        tokens = THEME_PALETTES.get(theme.lower()) if isinstance(theme, str) else theme
        if tokens:
            if "unified_box" in tokens:
                self._unified_box = bool(tokens["unified_box"])
            if not self._custom_icons_set and "collapsed_icon" in tokens and "expanded_icon" in tokens:
                self._collapsed_icon = tokens["collapsed_icon"]
                self._expanded_icon = tokens["expanded_icon"]
                self._use_qicon = False
                self._update_chevron()
        self._refresh_stylesheet()

    def apply_modena_style(self, dark: bool = False) -> None:
        """
        Apply the authentic JavaFX TitledPane look and feel.
        Applies JavaFX Modena styling:
          - Subtle vertical gradients and 1px borders
          - Authentic JavaFX blue focus ring (#0096C9)
          - Solid directional triangle arrows (▶ / ▼)
          - Unified box container layout (seamless contiguous border)
          - Full keyboard accessibility (Tab, Space, Enter)
        """
        self.set_chevron_icons("▶", "▼")
        self.set_unified_box(True)
        self.apply_theme(Theme.MODENA_DARK if dark else Theme.MODENA)

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

    def _update_chevron(self) -> None:
        """Internal helper to refresh chevron label icon or text."""
        if self._use_qicon:
            icon = self._expanded_icon if self._expanded else self._collapsed_icon
            if isinstance(icon, QIcon):
                self.chevron_label.setPixmap(icon.pixmap(16, 16))
            self.chevron_label.setText("")
        else:
            self.chevron_label.setPixmap(QPixmap())
            self.chevron_label.setText(self._expanded_icon if self._expanded else self._collapsed_icon)

    def set_chevron_icons(self, collapsed_icon: Union[str, QIcon], expanded_icon: Union[str, QIcon]) -> None:
        """Set custom icons or text for the chevron."""
        self._custom_icons_set = True
        image_exts = (".svg", ".png", ".jpg", ".jpeg", ".bmp", ".ico")

        if isinstance(collapsed_icon, QIcon) and isinstance(expanded_icon, QIcon):
            self._use_qicon = True
            self._collapsed_icon = collapsed_icon
            self._expanded_icon = expanded_icon
        elif isinstance(collapsed_icon, str) and collapsed_icon.lower().endswith(image_exts):
            self._use_qicon = True
            self._collapsed_icon = QIcon(collapsed_icon)
            self._expanded_icon = QIcon(expanded_icon)
        else:
            self._use_qicon = False
            self._collapsed_icon = collapsed_icon
            self._expanded_icon = expanded_icon

        self._update_chevron()

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
        if not self._collapsible and collapsed:
            return

        self._expanded = not collapsed
        self._update_chevron()

        if self._unified_box:
            self._refresh_stylesheet()

        collapsed_height = self.header_frame.sizeHint().height()

        if collapsed:
            self.content_area.setMaximumHeight(0)
            self.content_area.setMinimumHeight(0)
            self.setMaximumHeight(collapsed_height)
            self.setMinimumHeight(collapsed_height)
            self.opacity_effect.setOpacity(0.0)
        else:
            content = self.content_area.widget()
            if content:
                content.adjustSize()
            content_height = content.sizeHint().height() if content else 0
            max_h = self.content_area.max_content_height()
            if max_h is not None and max_h > 0:
                content_height = min(content_height, max_h)

            total_height = collapsed_height + content_height + self.main_layout.verticalSpacing()
            self._target_content_height = content_height
            self._target_total_height = total_height
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
        """Animate expanding or collapsing smoothly (or instantaneous if animated=False)."""
        if self._expanded == expand:
            return

        if not self._collapsible and not expand:
            return

        self._expanded = expand
        self.toggled.emit(expand)
        self._update_chevron()

        if self._unified_box:
            self._refresh_stylesheet()

        if not self._animated:
            self.set_collapsed(not expand)
            return

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
            if self._unified_box:
                self._refresh_stylesheet()
        else:
            self.content_area.setMaximumHeight(self._target_content_height)
            self.setMaximumHeight(self._target_total_height)
            self.setMinimumHeight(collapsed_height)
            if self._unified_box:
                self._refresh_stylesheet()
        self.updateGeometry()


class Accordion(QWidget):
    """
    A container that manages multiple CollapsiblePane instances.
    Matches javafx.scene.control.Accordion behavior where at most
    one pane is expanded at any given time.
    """
    expanded_pane_changed: Signal = Signal(object)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName("accordion")
        self._panes: List[CollapsiblePane] = []
        self._expanded_pane: Optional[CollapsiblePane] = None
        self._layout: QVBoxLayout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(2)

    def add_pane(self, pane: CollapsiblePane) -> None:
        """Add a CollapsiblePane to this Accordion."""
        if pane in self._panes:
            return
        self._panes.append(pane)
        self._layout.addWidget(pane)
        pane.toggled.connect(lambda expanded, p=pane: self._on_pane_toggled(p, expanded))
        if pane.is_expanded:
            self.set_expanded_pane(pane)

    def remove_pane(self, pane: CollapsiblePane) -> None:
        """Remove a CollapsiblePane from this Accordion."""
        if pane not in self._panes:
            return
        self._panes.remove(pane)
        self._layout.removeWidget(pane)
        if self._expanded_pane is pane:
            self._expanded_pane = None
            self.expanded_pane_changed.emit(None)

    @property
    def panes(self) -> List[CollapsiblePane]:
        """Return a copy of the list of panes in this Accordion."""
        return list(self._panes)

    def get_panes(self) -> List[CollapsiblePane]:
        """Return the list of panes in this Accordion (JavaFX alias)."""
        return self.panes

    @property
    def expanded_pane(self) -> Optional[CollapsiblePane]:
        """Return the currently expanded pane in this Accordion, or None."""
        return self._expanded_pane

    def set_expanded_pane(self, target_pane: Optional[CollapsiblePane]) -> None:
        """Set the single expanded pane in the accordion, collapsing all others."""
        if target_pane is not None and target_pane not in self._panes:
            raise ValueError("Pane must be added to the Accordion before expanding it.")

        self._expanded_pane = target_pane
        for p in self._panes:
            if p is target_pane:
                if not p.is_expanded:
                    p.toggle(True)
            else:
                if p.is_expanded:
                    p.toggle(False)
        self.expanded_pane_changed.emit(target_pane)

    def _on_pane_toggled(self, pane: CollapsiblePane, expanded: bool) -> None:
        if expanded:
            self._expanded_pane = pane
            for other in self._panes:
                if other is not pane and other.is_expanded:
                    other.toggle(False)
            self.expanded_pane_changed.emit(pane)
        else:
            if self._expanded_pane is pane:
                self._expanded_pane = None
                self.expanded_pane_changed.emit(None)
