import sqlite3
import os
import time
import json
import uuid
from typing import Optional, List, Dict, Tuple
from .config import Config

class DatabaseManager:
    def __init__(self):
        # Store db in the same dir as config or user home
        # For now, let's put it in the base dir
        self.db_path = os.path.join(Config.BASE_DIR, "hexstrike_nexus.db")
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Legacy table - kept for backward compatibility
        c.execute('''CREATE TABLE IF NOT EXISTS chat_history
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      role TEXT,
                      message TEXT,
                      timestamp REAL,
                      agent TEXT)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS results_cache
                     (target TEXT,
                      analysis_type TEXT,
                      result_json TEXT,
                      timestamp REAL,
                      PRIMARY KEY (target, analysis_type))''')
        
        # New tables for modern conversation system
        c.execute('''CREATE TABLE IF NOT EXISTS conversations
                     (id TEXT PRIMARY KEY,
                      title TEXT NOT NULL,
                      created_at REAL NOT NULL,
                      updated_at REAL NOT NULL,
                      agent_type TEXT,
                      is_archived INTEGER DEFAULT 0)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS messages
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      conversation_id TEXT NOT NULL,
                      role TEXT NOT NULL,
                      content TEXT NOT NULL,
                      timestamp REAL NOT NULL,
                      metadata TEXT,
                      FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS ai_provider_configs
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT UNIQUE NOT NULL,
                      api_key_encrypted TEXT,
                      model TEXT,
                      is_active INTEGER DEFAULT 0,
                      config_json TEXT,
                      created_at REAL,
                      updated_at REAL)''')
        
        # Create indexes for performance
        c.execute('''CREATE INDEX IF NOT EXISTS idx_messages_conversation 
                     ON messages(conversation_id, timestamp)''')
        c.execute('''CREATE INDEX IF NOT EXISTS idx_conversations_updated 
                     ON conversations(updated_at DESC)''')
        
        conn.commit()
        
        # Migrate legacy data if needed
        self._migrate_legacy_data(conn)
        
        conn.close()

    def _migrate_legacy_data(self, conn):
        """Migrate old chat_history to new conversation system"""
        c = conn.cursor()
        
        # Check if migration is needed
        c.execute("SELECT COUNT(*) FROM chat_history")
        legacy_count = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM conversations")
        new_count = c.fetchone()[0]
        
        # If we have legacy data but no new conversations, migrate
        if legacy_count > 0 and new_count == 0:
            # Create a default conversation for legacy messages
            conv_id = str(uuid.uuid4())
            c.execute('''INSERT INTO conversations 
                        (id, title, created_at, updated_at, agent_type) 
                        VALUES (?, ?, ?, ?, ?)''',
                     (conv_id, "Migrated Chat History", time.time(), time.time(), "BugBountyWorkflowManager"))
            
            # Migrate all messages
            c.execute("SELECT role, message, timestamp, agent FROM chat_history ORDER BY timestamp ASC")
            for role, message, timestamp, agent in c.fetchall():
                c.execute('''INSERT INTO messages 
                            (conversation_id, role, content, timestamp, metadata) 
                            VALUES (?, ?, ?, ?, ?)''',
                         (conv_id, role, message, timestamp, json.dumps({"agent": agent})))
            
            conn.commit()

    # ========== Conversation Management ==========
    
    def create_conversation(self, title: str = "New Chat", agent_type: str = "BugBountyWorkflowManager") -> str:
        """Create new conversation and return ID"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        conv_id = str(uuid.uuid4())
        now = time.time()
        
        c.execute('''INSERT INTO conversations 
                    (id, title, created_at, updated_at, agent_type, is_archived) 
                    VALUES (?, ?, ?, ?, ?, ?)''',
                 (conv_id, title, now, now, agent_type, 0))
        
        conn.commit()
        conn.close()
        return conv_id

    def get_all_conversations(self, archived: bool = False) -> List[Dict]:
        """Get list of all conversations with metadata"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''SELECT id, title, created_at, updated_at, agent_type, is_archived 
                    FROM conversations 
                    WHERE is_archived = ? 
                    ORDER BY updated_at DESC''', (1 if archived else 0,))
        
        conversations = []
        for row in c.fetchall():
            conv_id, title, created_at, updated_at, agent_type, is_archived = row
            
            # Get last message preview
            c.execute('''SELECT content FROM messages 
                        WHERE conversation_id = ? 
                        ORDER BY timestamp DESC LIMIT 1''', (conv_id,))
            last_msg = c.fetchone()
            last_message = last_msg[0][:100] if last_msg else ""
            
            # Count messages
            c.execute('SELECT COUNT(*) FROM messages WHERE conversation_id = ?', (conv_id,))
            message_count = c.fetchone()[0]
            
            conversations.append({
                'id': conv_id,
                'title': title,
                'created_at': created_at,
                'updated_at': updated_at,
                'agent_type': agent_type,
                'is_archived': bool(is_archived),
                'last_message': last_message,
                'message_count': message_count
            })
        
        conn.close()
        return conversations

    def get_conversation_messages(self, conversation_id: str, limit: int = 100) -> List[Dict]:
        """Get messages for a specific conversation"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''SELECT id, role, content, timestamp, metadata 
                    FROM messages 
                    WHERE conversation_id = ? 
                    ORDER BY timestamp ASC 
                    LIMIT ?''', (conversation_id, limit))
        
        messages = []
        for row in c.fetchall():
            msg_id, role, content, timestamp, metadata_json = row
            metadata = json.loads(metadata_json) if metadata_json else {}
            
            messages.append({
                'id': msg_id,
                'role': role,
                'content': content,
                'timestamp': timestamp,
                'metadata': metadata
            })
        
        conn.close()
        return messages

    def add_message_to_conversation(self, conversation_id: str, role: str, content: str, metadata: Dict = None):
        """Add message to conversation"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        now = time.time()
        metadata_json = json.dumps(metadata) if metadata else None
        
        c.execute('''INSERT INTO messages 
                    (conversation_id, role, content, timestamp, metadata) 
                    VALUES (?, ?, ?, ?, ?)''',
                 (conversation_id, role, content, now, metadata_json))
        
        # Update conversation updated_at
        c.execute('UPDATE conversations SET updated_at = ? WHERE id = ?', (now, conversation_id))
        
        conn.commit()
        conn.close()

    def update_conversation_title(self, conversation_id: str, title: str):
        """Update conversation title"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('UPDATE conversations SET title = ?, updated_at = ? WHERE id = ?',
                 (title, time.time(), conversation_id))
        
        conn.commit()
        conn.close()

    def delete_conversation(self, conversation_id: str):
        """Delete conversation and all its messages"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Messages will be deleted automatically due to CASCADE
        c.execute('DELETE FROM conversations WHERE id = ?', (conversation_id,))
        
        conn.commit()
        conn.close()

    def archive_conversation(self, conversation_id: str, archived: bool = True):
        """Archive or unarchive conversation"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('UPDATE conversations SET is_archived = ? WHERE id = ?',
                 (1 if archived else 0, conversation_id))
        
        conn.commit()
        conn.close()

    # ========== AI Provider Configuration ==========
    
    def save_ai_provider_config(self, name: str, api_key: str, model: str, 
                               is_active: bool = False, config: Dict = None):
        """Save or update AI provider configuration"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        now = time.time()
        config_json = json.dumps(config) if config else None
        
        # Simple encryption placeholder - in production, use proper encryption
        # For now, we'll store as base64 encoded (NOT SECURE, just obfuscated)
        import base64
        api_key_encrypted = base64.b64encode(api_key.encode()).decode() if api_key else None
        
        # If setting as active, deactivate all others first
        if is_active:
            c.execute('UPDATE ai_provider_configs SET is_active = 0')
        
        c.execute('''INSERT OR REPLACE INTO ai_provider_configs 
                    (name, api_key_encrypted, model, is_active, config_json, created_at, updated_at) 
                    VALUES (?, ?, ?, ?, ?, 
                           COALESCE((SELECT created_at FROM ai_provider_configs WHERE name = ?), ?), 
                           ?)''',
                 (name, api_key_encrypted, model, 1 if is_active else 0, config_json, name, now, now))
        
        conn.commit()
        conn.close()

    def get_ai_provider_config(self, name: str) -> Optional[Dict]:
        """Get specific AI provider configuration"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''SELECT name, api_key_encrypted, model, is_active, config_json 
                    FROM ai_provider_configs WHERE name = ?''', (name,))
        
        row = c.fetchone()
        conn.close()
        
        if not row:
            return None
        
        name, api_key_encrypted, model, is_active, config_json = row
        
        # Decrypt API key (simple base64 decode)
        import base64
        api_key = base64.b64decode(api_key_encrypted).decode() if api_key_encrypted else None
        
        return {
            'name': name,
            'api_key': api_key,
            'model': model,
            'is_active': bool(is_active),
            'config': json.loads(config_json) if config_json else {}
        }

    def get_active_ai_provider(self) -> Optional[Dict]:
        """Get currently active AI provider configuration"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''SELECT name, api_key_encrypted, model, config_json 
                    FROM ai_provider_configs WHERE is_active = 1 LIMIT 1''')
        
        row = c.fetchone()
        conn.close()
        
        if not row:
            return None
        
        name, api_key_encrypted, model, config_json = row
        
        # Decrypt API key
        import base64
        api_key = base64.b64decode(api_key_encrypted).decode() if api_key_encrypted else None
        
        return {
            'name': name,
            'api_key': api_key,
            'model': model,
            'config': json.loads(config_json) if config_json else {}
        }

    def get_all_ai_providers(self) -> List[Dict]:
        """Get all configured AI providers"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''SELECT name, model, is_active FROM ai_provider_configs 
                    ORDER BY is_active DESC, name ASC''')
        
        providers = []
        for row in c.fetchall():
            name, model, is_active = row
            providers.append({
                'name': name,
                'model': model,
                'is_active': bool(is_active)
            })
        
        conn.close()
        return providers
    
    def get_configured_providers(self) -> List[Dict]:
        """Get list of providers that have API keys configured"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''SELECT DISTINCT name FROM ai_provider_configs 
                    WHERE api_key_encrypted IS NOT NULL''')
        
        providers = []
        for row in c.fetchall():
            providers.append(row[0])
        
        conn.close()
        return providers

    # ========== Legacy Methods (Backward Compatibility) ==========

    def add_message(self, role, message, agent="System"):
        """Legacy method - kept for backward compatibility"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO chat_history (role, message, timestamp, agent) VALUES (?, ?, ?, ?)",
                  (role, message, time.time(), agent))
        conn.commit()
        conn.close()

    def get_history(self, limit=50):
        """Legacy method - returns old format"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT role, message, agent, timestamp FROM chat_history ORDER BY timestamp ASC LIMIT ?", (limit,))
        rows = c.fetchall()
        conn.close()
        return rows

    def cache_result(self, target, analysis_type, result_json):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO results_cache (target, analysis_type, result_json, timestamp) VALUES (?, ?, ?, ?)",
                  (target, analysis_type, result_json, time.time()))
        conn.commit()
        conn.close()

    def get_cached_result(self, target, analysis_type):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT result_json FROM results_cache WHERE target=? AND analysis_type=?", (target, analysis_type))
        row = c.fetchone()
        conn.close()
        if row:
            return row[0]
        return None
