# CollapsiblePane (PySide6)

[![PyPI Version](https://img.shields.io/pypi/v/collapsiblepane.svg)](https://pypi.org/project/collapsiblepane/)
[![PyPI Downloads](https://static.pepy.tech/badge/collapsiblepane)](https://pepy.tech/projects/collapsiblepane)
[![Python Versions](https://img.shields.io/pypi/pyversions/collapsiblepane.svg)](https://pypi.org/project/collapsiblepane/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A sleek, customizable, and animated collapsible container widget for **PySide6**, inspired by JavaFX's `TitledPane`. It wraps child widgets cleanly with smooth height & opacity transitions, customizable headers, badges, drop shadows, and chevron controls.

---

## Features

- **Smooth Animated Transitions**: Expanding and collapsing with configurable duration, cubic easing, and opacity fading.
- **Interruptible Animations**: Mid-flight reverse transitions smoothly from the current height without jumping or flickering.
- **Customizable Header**: Set background color, text color, border, padding, hover styles, and fonts.
- **Customizable Chevron / Icons**: Supports Unicode glyphs (e.g., `▸`, `▾`) and image icons (`.svg`, `.png`, `QIcon`).
- **Card-Style Container**: Rounded borders, background fills, and drop shadows on the collapsible card.
- **Badge / Item Count Support**: Built-in counter or status badge with pill styling and shadows.
- **Pythonic Properties**: Intuitive access via `is_expanded`, `content_widget`, and `title`.
- **Qt Signals**: Emits `toggled(bool)` whenever the pane expands or collapses.

---

## Installation

```bash
pip install collapsiblepane
```

---

## Screenshots

| Collapsed View | Expanded View |
| :---: | :---: |
| ![Collapsed View](https://raw.githubusercontent.com/mjk22071998/CollapsiblePane/refs/heads/main/screenshot/collapsed.PNG) | ![Expanded View](https://raw.githubusercontent.com/mjk22071998/CollapsiblePane/refs/heads/main/screenshot/expanded.PNG) |

---

## Quick Start

```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from collapsiblepane import CollapsiblePane

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CollapsiblePane Demo")
        self.resize(500, 400)

        # 1. Create the pane
        pane = CollapsiblePane("User Details", animation_duration=220)

        # 2. Style via modern presets or custom code
        pane.set_header_style(
            background_color="#1e293b",
            text_color="#f8fafc",
            hover_color="#283548",
            border_color="#334155",
            border_radius=8
        )
        pane.set_card_style(background="#0f172a", border="#1e293b", radius=8, padding=12)
        pane.set_item_count(12)

        # 3. Create content widget
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(QLineEdit())
        layout.addWidget(QPushButton("Save"))

        pane.set_content_widget(content)

        # 4. Add to window layout
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.addWidget(pane)
        main_layout.addStretch()
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

---

## API Reference

### Constructor

```python
CollapsiblePane(title: str = "", animation_duration: int = 150, parent: Optional[QWidget] = None)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `title` | `str` | `""` | Initial header title. |
| `animation_duration` | `int` | `150` | Duration of expand/collapse animation in milliseconds. |
| `parent` | `Optional[QWidget]` | `None` | Parent Qt widget. |

---

### Properties

| Property | Type | Access | Description |
| :--- | :--- | :--- | :--- |
| `is_expanded` | `bool` | `get / set` | Whether the pane is currently expanded. Setting this animates the change. |
| `content_widget` | `Optional[QWidget]` | `get` | Returns the currently attached content widget. |
| `title` | `str` | `get / set` | Header title string. |

---

### Methods

#### State & Content
* **`toggle(expand: bool) -> None`**
  Animates expanding (`True`) or collapsing (`False`).
* **`set_collapsed(collapsed: bool = True) -> None`**
  Instantly sets collapsed (`True`) or expanded (`False`) without animation.
* **`set_content_widget(widget: QWidget) -> None`**
  Attaches `widget` to the content area, deleting any previous content widget.
* **`clear_widget() -> None`**
  Removes and deletes the current content widget.
* **`set_title(title: str) -> None`**
  Updates the header title.

#### Styling & Appearance
* **`set_header_style(...) -> None`**
  Customizes the header frame:
  `background_color`, `text_color`, `border_color`, `border_width`, `border_radius`, `padding_vertical`, `padding_horizontal`, `font_size`, `font_weight`, `hover_color`.
* **`set_chevron_icons(collapsed_icon, expanded_icon) -> None`**
  Accepts strings (glyphs like `"▸"`, `"▾"` or file paths like `"icon.svg"`) or `QIcon` objects.
* **`set_card_style(background, border, radius, padding, shadow_only) -> None`**
  Styles the expanded content container scroll area.
* **`set_card_shadow(color, blur, offset_y) -> None`**
  Adds a soft drop shadow beneath the content area.
* **`set_content_text_style(color, font_size) -> None`**
  Applies uniform typography styling to text inside the content area.
* **`set_title_style(color, font_size, font_weight, italic) -> None`**
  Fine-tunes header title typography.
* **`set_item_count(count: Optional[int], show_badge: bool = True) -> None`**
  Displays or hides a numeric count badge.
* **`set_item_badge_style(...) -> None`**
  Styles the badge: `text`, `bg_color`, `text_color`, `border_color`, `border_radius`, `padding_vertical`, `padding_horizontal`, `font_size`, `font_weight`, `shadow`, `min_width`.
* **`apply_theme(theme: Union[str, dict]) -> None`**
  Applies a built-in theme (`"dark"`, `"light"`, `"indigo"`, `"slate"`) or custom token dictionary.
* **`set_max_content_height(max_height: Optional[int]) -> None`**
  Sets maximum height constraint for expanded content before scrollbars appear.

---

### Stylesheet (QSS) Theming

Every component has standardized Qt object names for direct QSS customization:

```css
CollapsiblePane {
    background: transparent;
}
QFrame#header_frame {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
}
QFrame#header_frame:hover {
    background-color: #283548;
}
QLabel#title_label {
    color: #f8fafc;
    font-size: 13px;
    font-weight: 600;
}
QLabel#chevron_label {
    color: #94a3b8;
}
QLabel#count_label {
    background-color: rgba(99, 102, 241, 0.18);
    color: #a5b4fc;
    border: 1px solid rgba(99, 102, 241, 0.35);
    border-radius: 10px;
    padding: 2px 8px;
}
QScrollArea#content_area {
    background-color: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 8px;
}
```

---

### Signals

* **`toggled(bool)`**: Emits `True` when expanded and `False` when collapsed.

---

## Running the Demo

Clone the repository and run:

```bash
python example.py
```

---

## Running Tests

Run the test suite using `unittest` or `pytest`:

```bash
python -m unittest discover tests/
# or
pytest
```

---

## License

This project is licensed under the [MIT License](LICENSE).
