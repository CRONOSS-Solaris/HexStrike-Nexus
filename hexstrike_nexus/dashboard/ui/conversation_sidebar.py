"""
Conversation Sidebar Widget - manages conversation list
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QListWidget, QListWidgetItem, QLineEdit, QLabel,
                             QMenu, QInputDialog, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QCursor
from .styles import HexStyle
from ..core.conversation_manager import ConversationManager
from ...i18n.manager import i18n
import time


class ConversationSidebar(QWidget):
    """Sidebar widget for managing conversations"""
    
    # Signals
    conversation_selected = pyqtSignal(str)  # conversation_id
    conversation_deleted = pyqtSignal(str)   # conversation_id
    
    def __init__(self, conversation_manager: ConversationManager):
        super().__init__()
        self.conversation_manager = conversation_manager
        self.current_conversation_id = None
        self.init_ui()
        self.refresh_conversations()
        
    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        self.setLayout(layout)
        
        # Header with New Chat button
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 15, 10, 10)
        
        title_label = QLabel("💬 Conversations")
        title_label.setObjectName("SectionTitle")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        new_chat_btn = QPushButton("+ New")
        new_chat_btn.setObjectName("IconButton")
        new_chat_btn.clicked.connect(self.create_new_conversation)
        new_chat_btn.setToolTip("Create new conversation")
        header_layout.addWidget(new_chat_btn)
        
        layout.addWidget(header)
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Search conversations...")
        self.search_box.textChanged.connect(self.filter_conversations)
        self.search_box.setContentsMargins(10, 0, 10, 0)
        layout.addWidget(self.search_box)
        
        # Conversation list
        self.conversation_list = QListWidget()
        self.conversation_list.setObjectName("ConversationList")
        self.conversation_list.itemClicked.connect(self.on_conversation_clicked)
        self.conversation_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.conversation_list.customContextMenuRequested.connect(self.show_context_menu)
        layout.addWidget(self.conversation_list)
        
    def refresh_conversations(self):
        """Refresh conversation list from database"""
        self.conversation_list.clear()
        conversations = self.conversation_manager.get_all_conversations(archived=False)
        
        for conv in conversations:
            self.add_conversation_item(conv)
    
    def add_conversation_item(self, conv: dict):
        """Add conversation to list"""
        item = QListWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, conv['id'])
        
        # Format display text
        title = conv.get('title', 'Untitled')
        agent = conv.get('agent_type', 'General')
        last_msg = conv.get('last_message', '')
        msg_count = conv.get('message_count', 0)
        
        # Agent icon
        agent_icons = {
            'BugBountyWorkflowManager': '🎯',
            'CTFWorkflowManager': '🏴',
            'CVEIntelligenceManager': '🐛',
            'AIExploitGenerator': '💣',
            'General': '💬'
        }
        icon = agent_icons.get(agent, '💬')
        
        # Format timestamp
        updated_at = conv.get('updated_at', time.time())
        time_str = self.format_time(updated_at)
        
        # Create rich text for item
        display_text = f"{icon} {title}\n"
        display_text += f"{last_msg[:50]}{'...' if len(last_msg) > 50 else ''}\n"
        display_text += f"💬 {msg_count} • {time_str}"
        
        item.setText(display_text)
        item.setSizeHint(QSize(0, 70))
        
        self.conversation_list.addItem(item)
    
    def format_time(self, timestamp: float) -> str:
        """Format timestamp to relative time"""
        now = time.time()
        diff = now - timestamp
        
        if diff < 60:
            return "Just now"
        elif diff < 3600:
            mins = int(diff / 60)
            return f"{mins}m ago"
        elif diff < 86400:
            hours = int(diff / 3600)
            return f"{hours}h ago"
        elif diff < 604800:
            days = int(diff / 86400)
            return f"{days}d ago"
        else:
            return time.strftime("%b %d", time.localtime(timestamp))
    
    def create_new_conversation(self):
        """Create new conversation"""
        # Ask for title
        title, ok = QInputDialog.getText(
            self,
            "New Conversation",
            "Conversation title:",
            text="New Chat"
        )
        
        if ok and title:
            # Ask for agent type
            agents = [
                'BugBountyWorkflowManager',
                'CTFWorkflowManager',
                'CVEIntelligenceManager',
                'AIExploitGenerator',
                'General'
            ]
            
            agent, ok = QInputDialog.getItem(
                self,
                "Select Agent",
                "Choose agent type:",
                agents,
                0,
                False
            )
            
            if ok:
                conv_id = self.conversation_manager.create_conversation(title, agent)
                self.refresh_conversations()
                
                # Select the new conversation
                for i in range(self.conversation_list.count()):
                    item = self.conversation_list.item(i)
                    if item.data(Qt.ItemDataRole.UserRole) == conv_id:
                        self.conversation_list.setCurrentItem(item)
                        self.on_conversation_clicked(item)
                        break
    
    def on_conversation_clicked(self, item: QListWidgetItem):
        """Handle conversation selection"""
        conv_id = item.data(Qt.ItemDataRole.UserRole)
        if conv_id != self.current_conversation_id:
            self.current_conversation_id = conv_id
            self.conversation_selected.emit(conv_id)
    
    def filter_conversations(self, text: str):
        """Filter conversations by search text"""
        search_text = text.lower()
        
        for i in range(self.conversation_list.count()):
            item = self.conversation_list.item(i)
            item_text = item.text().lower()
            
            # Show/hide based on search
            item.setHidden(search_text not in item_text)
    
    def show_context_menu(self, position):
        """Show context menu for conversation"""
        item = self.conversation_list.itemAt(position)
        if not item:
            return
        
        conv_id = item.data(Qt.ItemDataRole.UserRole)
        
        menu = QMenu(self)
        
        rename_action = menu.addAction("✏️ Rename")
        delete_action = menu.addAction("🗑️ Delete")
        menu.addSeparator()
        archive_action = menu.addAction("📦 Archive")
        
        action = menu.exec(self.conversation_list.mapToGlobal(position))
        
        if action == rename_action:
            self.rename_conversation(conv_id, item)
        elif action == delete_action:
            self.delete_conversation(conv_id)
        elif action == archive_action:
            self.archive_conversation(conv_id)
    
    def rename_conversation(self, conv_id: str, item: QListWidgetItem):
        """Rename conversation"""
        conv_info = self.conversation_manager.get_conversation_info(conv_id)
        current_title = conv_info.get('title', 'Untitled')
        
        new_title, ok = QInputDialog.getText(
            self,
            "Rename Conversation",
            "New title:",
            text=current_title
        )
        
        if ok and new_title:
            self.conversation_manager.update_conversation_title(conv_id, new_title)
            self.refresh_conversations()
    
    def delete_conversation(self, conv_id: str):
        """Delete conversation with confirmation"""
        reply = QMessageBox.question(
            self,
            "Delete Conversation",
            "Are you sure you want to delete this conversation?\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.conversation_manager.delete_conversation(conv_id)
            self.conversation_deleted.emit(conv_id)
            self.refresh_conversations()
            
            # Select first conversation if available
            if self.conversation_list.count() > 0:
                first_item = self.conversation_list.item(0)
                self.conversation_list.setCurrentItem(first_item)
                self.on_conversation_clicked(first_item)
    
    def archive_conversation(self, conv_id: str):
        """Archive conversation"""
        self.conversation_manager.archive_conversation(conv_id, True)
        self.refresh_conversations()
    
    def get_current_conversation_id(self) -> str:
        """Get currently selected conversation ID"""
        return self.current_conversation_id
    
    def set_current_conversation(self, conv_id: str):
        """Programmatically select a conversation"""
        for i in range(self.conversation_list.count()):
            item = self.conversation_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == conv_id:
                self.conversation_list.setCurrentItem(item)
                self.current_conversation_id = conv_id
                break
