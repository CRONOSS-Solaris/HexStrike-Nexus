"""
Modern Cyberpunk-inspired Dark Theme for HexStrike Nexus
"""


class HexStyle:
    # ==================== COLOR PALETTE ====================
    
    # Base / Background Colors - Deep Dark Mode
    BG_MAIN = "#0a0a0f"           # Deepest background
    BG_SECONDARY = "#131318"      # Sidebar, secondary panels
    BG_TERTIARY = "#1a1a24"       # Cards, elevated elements
    BG_QUATERNARY = "#252530"     # Input fields, hover states
    
    # Accent Colors - Vibrant Cyberpunk
    ACCENT_PRIMARY = "#7c3aed"    # Violet - main brand color
    ACCENT_SECONDARY = "#06b6d4"  # Cyan - secondary actions
    ACCENT_TERTIARY = "#ec4899"   # Pink - highlights, special
    ACCENT_QUATERNARY = "#8b5cf6" # Light violet - hover states
    
    # Status Colors
    STATUS_SUCCESS = "#10b981"    # Emerald green
    STATUS_ERROR = "#ef4444"      # Red
    STATUS_WARNING = "#f59e0b"    # Amber
    STATUS_INFO = "#3b82f6"       # Blue
    STATUS_ONLINE = "#22c55e"     # Bright green
    STATUS_OFFLINE = "#64748b"    # Gray
    
    # Text Colors
    TEXT_PRIMARY = "#f8f9fa"      # Almost white - main text
    TEXT_SECONDARY = "#9ca3af"    # Gray - secondary text
    TEXT_MUTED = "#6b7280"        # Muted gray - hints, placeholders
    TEXT_INVERSE = "#0a0a0f"      # Dark text on light backgrounds
    
    # Border & Divider Colors
    BORDER_LIGHT = "#252530"
    BORDER_MEDIUM = "#3f3f46"
    BORDER_HEAVY = "#52525b"
    BORDER_ACCENT = "#7c3aed"
    
    # Gradient Definitions
    GRADIENT_PRIMARY = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7c3aed, stop:1 #ec4899)"
    GRADIENT_SECONDARY = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #06b6d4, stop:1 #7c3aed)"
    GRADIENT_SUCCESS = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #06b6d4)"
    GRADIENT_DARK = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1a1a24, stop:1 #0a0a0f)"
    
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
        border-right: 1px solid {BORDER_LIGHT};
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
        background: {GRADIENT_PRIMARY};
        color: {TEXT_PRIMARY};
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 14px;
    }}
    
    QPushButton:hover {{
        background: {ACCENT_QUATERNARY};
    }}
    
    QPushButton:pressed {{
        background: {ACCENT_TERTIARY};
    }}
    
    QPushButton:disabled {{
        background-color: {BG_QUATERNARY};
        color: {TEXT_MUTED};
    }}
    
    /* Secondary / Ghost Button */
    QPushButton#SecondaryButton {{
        background-color: transparent;
        border: 2px solid {BORDER_MEDIUM};
        color: {TEXT_PRIMARY};
    }}
    
    QPushButton#SecondaryButton:hover {{
        border-color: {ACCENT_PRIMARY};
        background-color: rgba(124, 58, 237, 0.1);
        color: {ACCENT_PRIMARY};
    }}
    
    /* Icon Button / Small Button */
    QPushButton#IconButton {{
        padding: 8px;
        min-width: 36px;
        max-width: 36px;
        min-height: 36px;
        max-height: 36px;
        border-radius: 6px;
        background-color: {BG_QUATERNARY};
    }}
    
    QPushButton#IconButton:hover {{
        background-color: {ACCENT_PRIMARY};
    }}
    
    /* === INPUT FIELDS === */
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background-color: {BG_QUATERNARY};
        border: 2px solid {BORDER_LIGHT};
        border-radius: 8px;
        padding: 10px 14px;
        color: {TEXT_PRIMARY};
        selection-background-color: {ACCENT_PRIMARY};
        selection-color: {TEXT_PRIMARY};
    }}
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border: 2px solid {ACCENT_PRIMARY};
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
        border: 1px solid {BORDER_LIGHT};
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
            
            /* User Messages */
            .user-container {{
                align-items: flex-end;
            }}
            
            .user-bubble {{
                background: linear-gradient(135deg, {ACCENT_PRIMARY}, {ACCENT_TERTIARY});
                color: {TEXT_PRIMARY};
                border-bottom-right-radius: 4px;
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
