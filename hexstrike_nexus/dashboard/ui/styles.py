"""
Modern Cyberpunk-inspired Dark Theme for HexStrike Nexus
"""


class HexStyle:
    # ==================== COLOR PALETTE ====================
    # VS Code Inspired Theme
    
    # Base / Background Colors - VS Code Dark
    BG_MAIN = "#1e1e1e"           # Editor background
    BG_SECONDARY = "#252526"      # Sidebar background
    BG_TERTIARY = "#2d2d30"       # Elevated elements, hover
    BG_QUATERNARY = "#3e3e42"     # Input fields, selection
    
    # Accent Colors - VS Code Blue
    ACCENT_PRIMARY = "#007acc"    # VS Code blue - main accent
    ACCENT_SECONDARY = "#4ec9b0"  # Teal - secondary highlights
    ACCENT_TERTIARY = "#569cd6"   # Light blue - tertiary
    ACCENT_QUATERNARY = "#0098ff" # Bright blue - active states
    
    # Status Colors - VS Code
    STATUS_SUCCESS = "#4ec9b0"   # Teal - success, online
    STATUS_WARNING = "#dcdcaa"   # Yellow - warnings  
    STATUS_ERROR = "#f48771"     # Coral red - errors
    STATUS_INFO = "#569cd6"      # Light blue - information   STATUS_ONLINE = "#22c55e"     # Bright green
    STATUS_OFFLINE = "#64748b"    # Gray
    
    # Text Colors - VS Code
    TEXT_PRIMARY = "#cccccc"      # Main text
    TEXT_SECONDARY = "#9cdcfe"    # Secondary text - light blue
    TEXT_TERTIARY = "#808080"     # Tertiary text - gray
    TEXT_MUTED = "#6a6a6a"        # Muted - hints, placeholders
    TEXT_INVERSE = "#1e1e1e"      # Dark text
    
    # Border & Divider Colors - VS Code
    BORDER_LIGHT = "#2d2d30"
    BORDER_MEDIUM = "#3e3e42"
    BORDER_HEAVY = "#454545"
    BORDER_ACCENT = "#007acc"
    
    # No gradients in VS Code style - using solid accent color
    ACCENT_SOLID = "#007acc"  # Use for buttons instead of gradients
    
    # Backward compatibility aliases for legacy components
    BG_SIDEBAR = BG_SECONDARY  # Old name compatibility
    BG_CARD = BG_TERTIARY      # Old name compatibility
    BG_INPUT = BG_QUATERNARY   # Old name compatibility
    ACCENT_HOVER = ACCENT_QUATERNARY  # Old name compatibility
    BORDER_FOCUS = ACCENT_PRIMARY     # Old name compatibility

    
    # ==================== MAIN APPLICATION STYLE ====================
    
    APP_STYLE = f"""
    /* === GLOBAL STYLES === */
    QMainWindow {{
        background-color: {BG_MAIN};
    }}
    
    QWidget {{
        color: {TEXT_PRIMARY};
        font-family: 'Segoe UI', 'Inter', 'Roboto', sans-serif;
        font-size: 14px;
        background-color: transparent;
    }}
    
    /* === SIDEBAR === */
    QListWidget#Sidebar {{
        background-color: {BG_SECONDARY};
        border: none;
        outline: none;
        border-right: 1px solid {BORDER_MEDIUM};
        padding: 10px 5px;
    }}
    
    QListWidget#Sidebar::item {{
        padding: 12px 16px;
        margin: 4px 6px;
        border-radius: 10px;
        color: {TEXT_SECONDARY};
        font-weight: 500;
    }}
    
    QListWidget#Sidebar::item:hover {{
        background-color: {BG_TERTIARY};
        color: {TEXT_PRIMARY};
    }}
    
    QListWidget#Sidebar::item:selected {{
        background: {GRADIENT_PRIMARY};
        color: {TEXT_PRIMARY};
        font-weight: 600;
    }}
    
    /* === CONVERSATION SIDEBAR === */
    QListWidget#ConversationList {{
        background-color: {BG_SECONDARY};
        border: none;
        outline: none;
        padding: 5px;
    }}
    
    QListWidget#ConversationList::item {{
        padding: 14px 12px;
        margin: 3px 5px;
        border-radius: 8px;
        background-color: {BG_TERTIARY};
        border-left: 3px solid transparent;
        min-height: 50px;
    }}
    
    QListWidget#ConversationList::item:hover {{
        background-color: {BG_QUATERNARY};
        border-left-color: {ACCENT_SECONDARY};
    }}
    
    QListWidget#ConversationList::item:selected {{
        background-color: {BG_QUATERNARY};
        border-left-color: {ACCENT_PRIMARY};
    }}
    
    /* === BUTTONS === */
    QPushButton {{
        background-color: {BG_TERTIARY};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER_MEDIUM};
        border-radius: 2px;
        padding: 6px 14px;
        font-size: 13px;
        font-weight: normal;
    }}
    
    QPushButton:hover {{
        background-color: {BG_QUATERNARY};
        border-color: {BORDER_HEAVY};
    }}
    
    QPushButton:pressed {{
        background-color: {BG_SECONDARY};
    }}
    
    QPushButton:disabled {{
        background-color: {BG_SECONDARY};
        color: {TEXT_MUTED};
        border-color: {BORDER_LIGHT};
    }}
    
    /* Primary Button - VS Code Blue */
    QPushButton#PrimaryButton {{
        background-color: {ACCENT_PRIMARY};
        color: #ffffff;
        border: none;
        font-weight: 500;
    }}
    
    QPushButton#PrimaryButton:hover {{
        background-color: {ACCENT_QUATERNARY};
    }}
    
    /* Secondary / Ghost Button */
    QPushButton#SecondaryButton {{
        background-color: transparent;
        border: 1px solid {BORDER_MEDIUM};
        color: {TEXT_PRIMARY};
    }}
    
    QPushButton#SecondaryButton:hover {{
        border-color: {ACCENT_PRIMARY};
        background-color: rgba(0, 122, 204, 0.1); /* VS Code blue with transparency */
        color: {ACCENT_PRIMARY};
    }}
    
    /* Icon Button / Small Button */
    QPushButton#IconButton {{
        padding: 4px;
        min-width: 28px;
        max-width: 28px;
        min-height: 28px;
        max-height: 28px;
        border-radius: 2px;
        background-color: {BG_QUATERNARY};
        border: 1px solid {BORDER_MEDIUM};
    }}
    
    QPushButton#IconButton:hover {{
        background-color: {ACCENT_PRIMARY};
        border-color: {ACCENT_PRIMARY};
        color: #ffffff;
    }}
    
    /* === INPUT FIELDS === */
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background-color: {BG_QUATERNARY};
        border: 1px solid {BORDER_LIGHT};
        border-radius: 2px;
        padding: 6px 8px;
        color: {TEXT_PRIMARY};
        selection-background-color: {ACCENT_PRIMARY};
        selection-color: #ffffff;
    }}
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border-color: {ACCENT_PRIMARY};
        background-color: {BG_TERTIARY};
    }}
    
    QLineEdit:disabled, QTextEdit:disabled {{
        background-color: {BG_TERTIARY};
        color: {TEXT_MUTED};
        border-color: {BORDER_LIGHT};
    }}
    
    /* === COMBO BOX === */
    QComboBox {{
        background-color: {BG_QUATERNARY};
        border: 2px solid {BORDER_LIGHT};
        border-radius: 8px;
        padding: 8px 14px;
        color: {TEXT_PRIMARY};
        min-height: 20px;
    }}
    
    QComboBox:hover {{
        border-color: {ACCENT_SECONDARY};
    }}
    
    QComboBox:focus {{
        border-color: {ACCENT_PRIMARY};
    }}
    
    QComboBox::drop-down {{
        border: none;
        width: 30px;
    }}
    
    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid {TEXT_SECONDARY};
        margin-right: 8px;
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {BG_TERTIARY};
        border: 1px solid {BORDER_MEDIUM};
        border-radius: 8px;
        selection-background-color: {ACCENT_PRIMARY};
        selection-color: {TEXT_PRIMARY};
        padding: 5px;
    }}
    
    /* === SCROLLBARS === */
    QScrollBar:vertical {{
        background: {BG_MAIN};
        width: 10px;
        margin: 0;
        border-radius: 5px;
    }}
    
    QScrollBar::handle:vertical {{
        background: {BORDER_MEDIUM};
        min-height: 30px;
        border-radius: 5px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background: {ACCENT_PRIMARY};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    
    QScrollBar:horizontal {{
        background: {BG_MAIN};
        height: 10px;
        margin: 0;
        border-radius: 5px;
    }}
    
    QScrollBar::handle:horizontal {{
        background: {BORDER_MEDIUM};
        min-width: 30px;
        border-radius: 5px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background: {ACCENT_PRIMARY};
    }}
    
   QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}
    
    /* === GROUP BOX === */
    QGroupBox {{
        background-color: {BG_TERTIARY};
        border: 1px solid {BORDER_MEDIUM};
        border-radius: 12px;
        margin-top: 20px;
        padding-top: 10px;
        font-weight: 600;
        color: {ACCENT_SECONDARY};
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 4px 12px;
        left: 10px;
        background-color: {BG_TERTIARY};
        border-radius: 6px;
        color: {ACCENT_SECONDARY};
    }}
    
    /* === LABELS === */
    QLabel#HeaderTitle {{
        font-size: 26px;
        font-weight: 700;
        color: {TEXT_PRIMARY};
        padding: 5px 0;
    }}
    
    QLabel#SectionTitle {{
        font-size: 18px;
        font-weight: 600;
        color: {ACCENT_SECONDARY};
        padding: 8px 0;
    }}
    
    QLabel#SubTitle {{
        font-size: 14px;
        color: {TEXT_SECONDARY};
        font-weight: 500;
    }}
    
    /* === TEXT BROWSER (Chat Display) === */
    QTextBrowser {{
        background-color: {BG_MAIN};
        border: none;
        color: {TEXT_PRIMARY};
    }}
    
    /* === TOOLTIPS === */
    QToolTip {{
        background-color: {BG_TERTIARY};
        color: {TEXT_PRIMARY};
        border: 1px solid {ACCENT_PRIMARY};
        border-radius: 6px;
        padding: 6px 10px;
        font-size: 12px;
    }}
    
    /* === CHECKBOX & RADIO === */
    QCheckBox, QRadioButton {{
        color: {TEXT_PRIMARY};
        spacing: 8px;
    }}
    
    QCheckBox::indicator, QRadioButton::indicator {{
        width: 18px;
        height: 18px;
        border-radius: 4px;
        border: 2px solid {BORDER_MEDIUM};
        background-color: {BG_QUATERNARY};
    }}
    
    QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
        background-color: {ACCENT_PRIMARY};
        border-color: {ACCENT_PRIMARY};
    }}
    
    QCheckBox::indicator:hover, QRadioButton::indicator:hover {{
        border-color: {ACCENT_SECONDARY};
    }}
    """
    
    # ==================== CHAT HTML TEMPLATE ====================
    
    CHAT_HTML_TEMPLATE = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', 'Inter', sans-serif;
                background-color: {BG_MAIN};
                color: {TEXT_PRIMARY};
                padding: 20px;
                line-height: 1.6;
            }}
            
            .message-container {{
                margin-bottom: 20px;
                display: flex;
                flex-direction: column;
                animation: slideIn 0.3s ease-out;
            }}
            
            @keyframes slideIn {{
                from {{
                    opacity: 0;
                    transform: translateY(10px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            
            .message-header {{
                font-size: 12px;
                font-weight: 600;
                margin-bottom: 6px;
                color: {TEXT_SECONDARY};
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            
            .message-bubble {{
                padding: 14px 18px;
                border-radius: 12px;
                max-width: 85%;
                line-height: 1.5;
                word-wrap: break-word;
                position: relative;
            }}
            
            /* User Messages - VS Code blue */
            .user-container {{
                align-items: flex-end;
            }}
            
            .user-bubble {{
                background-color: {ACCENT_PRIMARY};
                color: #ffffff;
                border-bottom-right-radius: 2px;
            }}
            
            /* AI Messages */
            .ai-container {{
                align-items: flex-start;
            }}
            
            .ai-bubble {{
                background-color: {BG_TERTIARY};
                border: 1px solid {BORDER_LIGHT};
                border-bottom-left-radius: 4px;
            }}
            
            /* System Messages */
            .system-container {{
                align-items: center;
            }}
            
            .system-bubble {{
                background-color: transparent;
                color: {TEXT_SECONDARY};
                font-style: italic;
                font-size: 13px;
                text-align: center;
                border: 1px dashed {BORDER_LIGHT};
                border-radius: 8px;
            }}
            
            /* Code Blocks */
            code {{
                background-color: rgba(0, 0, 0, 0.4);
                padding: 3px 6px;
                border-radius: 4px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
                color: {ACCENT_SECONDARY};
            }}
            
            pre {{
                background-color: #000;
                padding: 14px;
                border-radius: 8px;
                overflow-x: auto;
                border-left: 3px solid {ACCENT_PRIMARY};
                margin: 10px 0;
            }}
            
            pre code {{
                background: none;
                padding: 0;
                color: {TEXT_PRIMARY};
            }}
            
            /* Links */
            a {{
                color: {ACCENT_SECONDARY};
                text-decoration: none;
                font-weight: 500;
            }}
            
            a:hover {{
                color: {ACCENT_PRIMARY};
                text-decoration: underline;
            }}
            
            /* Lists */
            ul, ol {{
                margin-left: 20px;
                margin-top: 8px;
            }}
            
            li {{
                margin-bottom: 4px;
            }}
            
            /* Headings */
            h1, h2, h3, h4 {{
                color: {ACCENT_SECONDARY};
                margin-top: 16px;
                margin-bottom: 10px;
            }}
            
            /* Horizontal Rule */
            hr {{
                border: none;
                border-top: 1px solid {BORDER_LIGHT};
                margin: 16px 0;
            }}
        </style>
    </head>
    <body id='chat-body'>
    <!-- Messages will be appended here -->
    """
    
    @classmethod
    def get_message_html(cls, role: str, content: str, username: str = None) -> str:
        """
        Generate HTML for a chat message
        
        Args:
            role: 'user', 'assistant', or 'system'
            content: Message content
            username: Optional username to display
            
        Returns:
            HTML string for the message
        """
        if role == "user":
            header_name = username or "You"
            return f"""
            <div class='message-container user-container'>
                <div class='message-header'>👤 {header_name}</div>
                <div class='message-bubble user-bubble'>{content}</div>
            </div>
            """
        elif role == "assistant":
            return f"""
            <div class='message-container ai-container'>
                <div class='message-header'>🤖 HexStrike Nexus</div>
                <div class='message-bubble ai-bubble'>{content}</div>
            </div>
            """
        else:  # system
            return f"""
            <div class='message-container system-container'>
                <div class='message-bubble system-bubble'>{content}</div>
            </div>
            """
