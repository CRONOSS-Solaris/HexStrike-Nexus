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
    /* === GLOBAL STYLES - MINIMALIST CLEAN === */
    QMainWindow {{
        background-color: {BG_MAIN};
    }}
    
    QWidget {{
        color: {TEXT_PRIMARY};
        font-family: 'Segoe UI', 'Inter', 'Roboto', sans-serif;
        font-size: 14px;
        background-color: {BG_MAIN};  /* Ensure all widgets have background */
    }}
    
    /* Frames and containers */
    QFrame {{
        background-color: {BG_MAIN};
        border: none;
    }}
    
    
    /* === SIDEBAR - MINIMAL === */
    QListWidget#Sidebar {{
        background-color: {BG_SECONDARY};
        border: none;
        outline: none;
        border-right: 1px solid {BORDER_MEDIUM};
        padding: 8px;
    }}
    
    QListWidget#Sidebar::item {{
        padding: 10px 14px;
        margin: 2px 4px;
        border-radius: 4px;
        color: {TEXT_SECONDARY};
        background-color: transparent;
    }}
    
    QListWidget#Sidebar::item:hover {{
        background-color: {BG_TERTIARY};
        color: {TEXT_PRIMARY};
    }}
    
    QListWidget#Sidebar::item:selected {{
        background-color: {ACCENT_PRIMARY};
        color: #ffffff;
    }}
    
    /* === CONVERSATION SIDEBAR - MINIMAL === */
    QListWidget#ConversationList {{
        background-color: {BG_SECONDARY};
        border: none;
        outline: none;
        padding: 6px;
    }}
    
    QListWidget#ConversationList::item {{
        padding: 12px 10px;
        margin: 2px 4px;
        border-radius: 4px;
        background-color: {BG_TERTIARY};
        border-left: 2px solid transparent;
        min-height: 45px;
    }}
    
    QListWidget#ConversationList::item:hover {{
        background-color: {BG_QUATERNARY};
        border-left-color: {ACCENT_SECONDARY};
    }}
    
    QListWidget#ConversationList::item:selected {{
        background-color: {BG_QUATERNARY};
        border-left-color: {ACCENT_PRIMARY};
    }}
    
    
    /* === BUTTONS - MINIMAL FLAT === */
    QPushButton {{
        background-color: {BG_TERTIARY};
        color: {TEXT_PRIMARY};
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-size: 13px;
        font-weight: normal;
    }}
    
    QPushButton:hover {{
        background-color: {BG_QUATERNARY};
    }}
    
    QPushButton:pressed {{
        background-color: {ACCENT_PRIMARY};
        color: #ffffff;
    }}
    
    QPushButton:disabled {{
        background-color: {BG_SECONDARY};
        color: {TEXT_MUTED};
    }}
    
    /* Primary Button - Clean Accent */
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
        background-color: {BG_SECONDARY};
        border: 1px solid {BORDER_MEDIUM};
        color: {TEXT_PRIMARY};
    }}
    
    QPushButton#SecondaryButton:hover {{
        border-color: {ACCENT_PRIMARY};
        background-color: {BG_TERTIARY};
        color: {ACCENT_PRIMARY};
    }}
    
    /* Icon Button - Small and Minimal */
    QPushButton#IconButton {{
        padding: 6px;
        min-width: 32px;
        max-width: 32px;
        min-height: 32px;
        max-height: 32px;
        border-radius: 4px;
        background-color: {BG_TERTIARY};
        border: none;
    }}
    
    QPushButton#IconButton:hover {{
        background-color: {ACCENT_PRIMARY};
        color: #ffffff;
    }}
    
    /* === INPUT FIELDS - MINIMAL === */
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background-color: {BG_TERTIARY};
        border: 1px solid {BORDER_MEDIUM};
        border-radius: 4px;
        padding: 8px 10px;
        color: {TEXT_PRIMARY};
        selection-background-color: {ACCENT_PRIMARY};
        selection-color: #ffffff;
    }}
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border-color: {ACCENT_PRIMARY};
    }}
    
    QLineEdit:disabled, QTextEdit:disabled {{
        background-color: {BG_SECONDARY};
        color: {TEXT_MUTED};
        border-color: {BORDER_LIGHT};
    }}
    
    
    /* === COMBO BOX - MINIMAL === */
    QComboBox {{
        background-color: {BG_TERTIARY};
        border: 1px solid {BORDER_MEDIUM};
        border-radius: 4px;
        padding: 6px 12px;
        color: {TEXT_PRIMARY};
        min-height: 24px;
    }}
    
    QComboBox:hover {{
        border-color: {ACCENT_PRIMARY};
        background-color: {BG_QUATERNARY};
    }}
    
    QComboBox:focus {{
        border-color: {ACCENT_PRIMARY};
    }}
    
    QComboBox::drop-down {{
        border: none;
        width: 24px;
    }}
    
    QComboBox::down-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 5px solid {TEXT_SECONDARY};
        margin-right: 6px;
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {BG_TERTIARY};
        border: 1px solid {BORDER_MEDIUM};
        border-radius: 4px;
        selection-background-color: {ACCENT_PRIMARY};
        selection-color: #ffffff;
        padding: 4px;
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
                padding: 24px;
                line-height: 1.65;
            }}
            
            .message-container {{
                margin-bottom: 24px;
                display: flex;
                flex-direction: column;
                animation: slideIn 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            
            @keyframes slideIn {{
                from {{
                    opacity: 0;
                    transform: translateY(12px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            
            .message-header {{
                font-size: 12px;
                font-weight: 600;
                margin-bottom: 8px;
                color: {TEXT_SECONDARY};
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            
            .message-bubble {{
                padding: 16px 20px;
                border-radius: 14px;
                max-width: 85%;
                line-height: 1.65;
                word-wrap: break-word;
                position: relative;
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
            }}
            
            
            /* User Messages - Blue accent */
            .user-container {{
                align-items: flex-end;
            }}
            
            .user-bubble {{
                background: {ACCENT_PRIMARY};
                color: #ffffff;
                border-bottom-right-radius: 4px;
            }}
            
            
            /* AI Messages - Clearly visible with different background */
            .ai-container {{
                align-items: flex-start;
            }}
            
            .ai-bubble {{
                background-color: {BG_SECONDARY};
                border: 1px solid {BORDER_HEAVY};
                border-bottom-left-radius: 4px;
                color: {TEXT_PRIMARY};
            }}
            
            /* System Messages */
            .system-container {{
                align-items: center;
            }}
            
            .system-bubble {{
                background-color: transparent;
                color: {TEXT_SECONDARY};
                font-style: italic;
                font-size: 14px;
                text-align: center;
                border: 1px dashed {BORDER_MEDIUM};
                border-radius: 10px;
                padding: 12px 16px;
            }}
            
            /* Code Blocks */
            code {{
                background-color: rgba(0, 0, 0, 0.5);
                padding: 3px 8px;
                border-radius: 5px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 13px;
                color: {ACCENT_SECONDARY};
            }}
            
            pre {{
                background-color: #0d0d0d;
                padding: 16px;
                border-radius: 10px;
                overflow-x: auto;
                border-left: 4px solid {ACCENT_PRIMARY};
                margin: 12px 0;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
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
                border-bottom: 1px dotted {ACCENT_SECONDARY};
                transition: all 0.2s;
            }}
            
            a:hover {{
                color: {ACCENT_PRIMARY};
                border-bottom-color: {ACCENT_PRIMARY};
            }}
            
            /* Lists */
            ul, ol {{
                margin-left: 24px;
                margin-top: 10px;
            }}
            
            li {{
                margin-bottom: 6px;
            }}
            
            /* Headings */
            h1, h2, h3, h4 {{
                color: {ACCENT_SECONDARY};
                margin-top: 20px;
                margin-bottom: 12px;
                font-weight: 600;
            }}
            
            h1 {{ font-size: 24px; }}
            h2 {{ font-size: 20px; }}
            h3 {{ font-size: 17px; }}
            h4 {{ font-size: 15px; }}
            
            /* Horizontal Rule */
            hr {{
                border: none;
                border-top: 2px solid {BORDER_MEDIUM};
                margin: 20px 0;
            }}
            
            /* Tables */
            table {{
                border-collapse: collapse;
                margin: 12px 0;
                width: 100%;
            }}
            
            th, td {{
                border: 1px solid {BORDER_MEDIUM};
                padding: 10px 14px;
                text-align: left;
            }}
            
            th {{
                background-color: {BG_TERTIARY};
                font-weight: 600;
                color: {ACCENT_SECONDARY};
            }}
            
            /* Blockquotes */
            blockquote {{
                border-left: 4px solid {ACCENT_SECONDARY};
                padding-left: 16px;
                margin: 12px 0;
                font-style: italic;
                color: {TEXT_SECONDARY};
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
            role: 'user', 'assistant', 'system', or 'typing'
            content: Message content
            username: Optional username to display
            
        Returns:
            HTML string for the message
        """
        if role == "typing":
            # Special typing indicator
            return cls.get_typing_indicator_html()
        elif role == "user":
            header_name = username or "You"
            return f"""
            <div class='message-container user-container'>
                <div class='message-header'>{header_name}</div>
                <div class='message-bubble user-bubble'>{content}</div>
            </div>
            """
        elif role == "assistant":
            return f"""
            <div class='message-container ai-container'>
                <div class='message-header'>HexStrike Nexus</div>
                <div class='message-bubble ai-bubble'>{content}</div>
            </div>
            """
        else:  # system
            return f"""
            <div class='message-container system-container'>
                <div class='message-bubble system-bubble'>{content}</div>
            </div>
            """
    
    @classmethod
    def get_typing_indicator_html(cls) -> str:
        """Generate HTML for typing indicator with bouncing dots"""
        return f'''
        <div class='message-container ai-container' id='typing-indicator'>
            <div class='message-header'>HexStrike Nexus</div>
            <div class='message-bubble ai-bubble typing-bubble'>
                <span class='typing-text'>AI is thinking</span>
                <span class='typing-dots'>
                    <span class='dot'></span>
                    <span class='dot'></span>
                    <span class='dot'></span>
                </span>
            </div>
        </div>
        <style>
            .typing-bubble {{
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            
            .typing-text {{
                color: {cls.TEXT_SECONDARY};
                font-style: italic;
                font-size: 13px;
            }}
            
            .typing-dots {{
                display: flex;
                gap: 4px;
            }}
            
            .typing-dots .dot {{
                width: 6px;
                height: 6px;
                background-color: {cls.ACCENT_PRIMARY};
                border-radius: 50%;
                animation: bounce 1.4s infinite ease-in-out;
            }}
            
            .typing-dots .dot:nth-child(1) {{
                animation-delay: -0.32s;
            }}
            
            .typing-dots .dot:nth-child(2) {{
                animation-delay: -0.16s;
            }}
            
            @keyframes bounce {{
                0%, 80%, 100% {{
                    transform: scale(0);
                    opacity: 0.5;
                }}
                40% {{
                    transform: scale(1);
                    opacity: 1;
                }}
            }}
        </style>
        '''
