
class HexStyle:
    # --- Modern Dark Palette ---
    BG_MAIN = "#09090b"        # Deepest black/gray
    BG_SIDEBAR = "#18181b"     # Slightly lighter for sidebar
    BG_CARD = "#27272a"        # Card background
    BG_INPUT = "#3f3f46"       # Input field background
    
    ACCENT_PRIMARY = "#8b5cf6"  # Violet/Purple
    ACCENT_SECONDARY = "#06b6d4" # Cyan/Blue
    ACCENT_HOVER = "#7c3aed"    # Darker violet for hover
    
    TEXT_PRIMARY = "#f4f4f5"   # Near white
    TEXT_SECONDARY = "#a1a1aa" # Muted gray
    
    BORDER_LIGHT = "#3f3f46"
    BORDER_FOCUS = "#8b5cf6"
    
    STATUS_SUCCESS = "#10b981" # Emerald
    STATUS_ERROR = "#ef4444"   # Red
    STATUS_WARNING = "#f59e0b" # Amber
    
    # --- Stylesheet ---
    APP_STYLE = f"""
    QMainWindow {{
        background-color: {BG_MAIN};
    }}
    
    QWidget {{
        color: {TEXT_PRIMARY};
        font-family: 'Segoe UI', 'Roboto', sans-serif;
        font-size: 14px;
    }}
    
    /* --- Sidebar --- */
    QListWidget#Sidebar {{
        background-color: {BG_SIDEBAR};
        border: none;
        outline: none;
        padding-top: 20px;
    }}
    
    QListWidget#Sidebar::item {{
        height: 50px;
        padding-left: 10px;
        margin: 4px 10px;
        border-radius: 8px;
        color: {TEXT_SECONDARY};
    }}
    
    QListWidget#Sidebar::item:hover {{
        background-color: {BG_CARD};
        color: {TEXT_PRIMARY};
    }}
    
    QListWidget#Sidebar::item:selected {{
        background-color: {ACCENT_PRIMARY};
        color: {TEXT_PRIMARY};
    }}
    
    /* --- Cards / Containers --- */
    QFrame#Card, QWidget#ContentArea {{
        background-color: {BG_MAIN}; /* Transparent/Main BG since cards will have their own styling if needed, or just clean layout */
    }}

    QGroupBox {{
        background-color: {BG_CARD};
        border: 1px solid {BORDER_LIGHT};
        border-radius: 12px;
        margin-top: 1.5em; /* Leave space for title */
        font-weight: bold;
        color: {ACCENT_SECONDARY};
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 10px;
        left: 10px;
        color: {ACCENT_SECONDARY};
    }}

    /* --- Buttons --- */
    QPushButton {{
        background-color: {ACCENT_PRIMARY};
        color: {TEXT_PRIMARY};
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: 600;
    }}
    QPushButton:hover {{
        background-color: {ACCENT_HOVER};
    }}
    QPushButton:pressed {{
        background-color: {ACCENT_SECONDARY};
        color: {BG_MAIN};
    }}
    
    /* Ghost/Secondary Button */
    QPushButton#SecondaryButton {{
        background-color: transparent;
        border: 1px solid {BORDER_LIGHT};
        color: {TEXT_PRIMARY};
    }}
    QPushButton#SecondaryButton:hover {{
        border-color: {ACCENT_PRIMARY};
        color: {ACCENT_PRIMARY};
    }}

    /* --- Inputs --- */
    QLineEdit, QTextEdit, QPlainTextEdit, QComboBox {{
        background-color: {BG_INPUT};
        border: 1px solid {BORDER_LIGHT};
        border-radius: 6px;
        padding: 8px;
        color: {TEXT_PRIMARY};
        selection-background-color: {ACCENT_PRIMARY};
    }}
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus {{
        border: 1px solid {BORDER_FOCUS};
    }}
    
    /* --- Scrollbars (Modern Thin) --- */
    QScrollBar:vertical {{
        background: {BG_MAIN};
        width: 8px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {BORDER_LIGHT};
        min-height: 20px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {ACCENT_PRIMARY};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    
    /* --- Chat Special --- */
    QTextBrowser {{
        background-color: {BG_MAIN}; /* Chat background */
        border: none;
    }}

    /* --- Labels --- */
    QLabel#HeaderTitle {{
        font-size: 24px;
        font-weight: bold;
        color: {TEXT_PRIMARY};
        margin-bottom: 10px;
    }}
    QLabel#SectionTitle {{
        font-size: 18px;
        font-weight: 600;
        color: {TEXT_SECONDARY};
        margin-top: 10px;
    }}
    """
    
    # HTML Template for Chat Messages to match the theme
    CHAT_HTML_TEMPLATE = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background-color: {BG_MAIN}; color: {TEXT_PRIMARY}; margin: 0; padding: 10px; }}
            .message-container {{ margin-bottom: 15px; display: flex; flex-direction: column; }}
            .message-header {{ font-size: 12px; margin-bottom: 4px; color: {TEXT_SECONDARY}; }}
            .message-bubble {{ padding: 10px 15px; border-radius: 12px; max-width: 85%; line-height: 1.4; word-wrap: break-word; }}
            
            .user-container {{ align-items: flex-end; }}
            .user-bubble {{ background-color: {ACCENT_PRIMARY}; color: {TEXT_PRIMARY}; border-bottom-right-radius: 2px; }}
            
            .ai-container {{ align-items: flex-start; }}
            .ai-bubble {{ background-color: {BG_CARD}; border: 1px solid {BORDER_LIGHT}; border-bottom-left-radius: 2px; }}
            
            .system-container {{ align-items: center; }}
            .system-bubble {{ background-color: transparent; color: {TEXT_SECONDARY}; italic; font-size: 13px; text-align: center; border: 1px dashed {BORDER_LIGHT}; }}
            
            code {{ background-color: rgba(0,0,0,0.3); padding: 2px 4px; border-radius: 4px; font-family: 'Consolas', monospace; }}
            pre {{ background-color: #000; padding: 10px; border-radius: 8px; overflow-x: auto; }}
        </style>
    </head>
    <body id='chat-body'>
    """
