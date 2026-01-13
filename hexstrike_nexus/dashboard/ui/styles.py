
class HexStyle:
    # Color Palette
    BG_DARK = "#0f111a"
    BG_PANEL = "#1a1d2e"
    ACCENT_CYAN = "#00e5ff"
    ACCENT_PURPLE = "#7c4dff"
    TEXT_WHITE = "#ffffff"
    TEXT_GRAY = "#b0b3c5"
    BORDER_COLOR = "#2f344a"
    SUCCESS = "#00e676"
    ERROR = "#ff1744"

    # Main Stylesheet
    APP_STYLE = f"""
    QMainWindow {{
        background-color: {BG_DARK};
    }}

    QWidget {{
        color: {TEXT_WHITE};
        font-family: 'Segoe UI', 'Roboto', sans-serif;
        font-size: 14px;
    }}

    /* Panels & Containers */
    QFrame, QWidget#ChatWidget, QWidget#TelemetryWidget {{
        background-color: {BG_DARK};
    }}

    QGroupBox {{
        border: 1px solid {BORDER_COLOR};
        border-radius: 6px;
        margin-top: 20px;
        background-color: {BG_PANEL};
        font-weight: bold;
        color: {ACCENT_CYAN};
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 10px;
        color: {ACCENT_CYAN};
    }}

    /* Buttons */
    QPushButton {{
        background-color: {BG_PANEL};
        border: 1px solid {ACCENT_PURPLE};
        border-radius: 4px;
        padding: 8px 16px;
        color: {TEXT_WHITE};
        font-weight: bold;
    }}

    QPushButton:hover {{
        background-color: {ACCENT_PURPLE};
        color: {TEXT_WHITE};
    }}

    QPushButton:pressed {{
        background-color: {ACCENT_CYAN};
        border-color: {ACCENT_CYAN};
        color: {BG_DARK};
    }}

    /* Input Fields */
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background-color: {BG_PANEL};
        border: 1px solid {BORDER_COLOR};
        border-radius: 4px;
        padding: 6px;
        color: {TEXT_WHITE};
        selection-background-color: {ACCENT_PURPLE};
    }}

    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border: 1px solid {ACCENT_CYAN};
    }}

    /* Scrollbars */
    QScrollBar:vertical {{
        border: none;
        background: {BG_DARK};
        width: 10px;
        margin: 0px 0px 0px 0px;
    }}

    QScrollBar::handle:vertical {{
        background: {BORDER_COLOR};
        min-height: 20px;
        border-radius: 5px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {ACCENT_PURPLE};
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    /* Splitter */
    QSplitter::handle {{
        background-color: {BORDER_COLOR};
        width: 2px;
    }}

    QSplitter::handle:hover {{
        background-color: {ACCENT_CYAN};
    }}

    /* Combo Box */
    QComboBox {{
        background-color: {BG_PANEL};
        border: 1px solid {BORDER_COLOR};
        border-radius: 4px;
        padding: 5px;
        color: {TEXT_WHITE};
    }}

    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 15px;
        border-left-width: 0px;
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;
    }}

    /* Progress Bar */
    QProgressBar {{
        border: 1px solid {BORDER_COLOR};
        border-radius: 4px;
        background-color: {BG_PANEL};
        text-align: center;
        color: {TEXT_WHITE};
    }}

    QProgressBar::chunk {{
        background-color: {ACCENT_CYAN};
        border-radius: 3px;
    }}

    /* List Views / Tables */
    QListWidget, QTableWidget {{
        background-color: {BG_PANEL};
        border: 1px solid {BORDER_COLOR};
        gridline-color: {BORDER_COLOR};
    }}

    QHeaderView::section {{
        background-color: {BG_DARK};
        padding: 4px;
        border: 1px solid {BORDER_COLOR};
        color: {TEXT_GRAY};
    }}

    QListWidget::item:selected, QTableWidget::item:selected {{
        background-color: {ACCENT_PURPLE};
        color: {TEXT_WHITE};
    }}

    /* Labels */
    QLabel {{
        color: {TEXT_WHITE};
    }}

    QLabel#TitleLabel {{
        color: {ACCENT_CYAN};
        font-size: 18px;
        font-weight: bold;
    }}

    QLabel#StatusLabel {{
        color: {TEXT_GRAY};
        font-style: italic;
    }}
    """
