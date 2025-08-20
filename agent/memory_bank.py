"""
Memory Bank for Travel Advisor Agent
Manages persistent memory, user profiles, and conversation history
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import uuid

@dataclass
class ConversationEntry:
    """Single conversation entry"""
    id: str
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: str
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class UserProfile:
    """User profile with travel preferences"""
    user_id: str
    name: Optional[str] = None
    preferences: Dict[str, Any] = None
    travel_history: List[Dict[str, Any]] = None
    payment_info: Dict[str, Any] = None
    emergency_contacts: List[Dict[str, str]] = None
    created_at: str = None
    last_updated: str = None
    
    def __post_init__(self):
        if self.preferences is None:
            self.preferences = {}
        if self.travel_history is None:
            self.travel_history = []
        if self.payment_info is None:
            self.payment_info = {}
        if self.emergency_contacts is None:
            self.emergency_contacts = []
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.last_updated is None:
            self.last_updated = datetime.now().isoformat()

class MemoryBank:
    """
    Persistent memory system for the travel agent
    Stores conversations, user profiles, and learned information
    """
    
    def __init__(self, storage_path: str = "agent_memory"):
        self.storage_path = storage_path
        self.conversations: Dict[str, List[ConversationEntry]] = {}
        self.user_profiles: Dict[str, UserProfile] = {}
        self.global_knowledge: Dict[str, Any] = {}
        self.current_session_id: Optional[str] = None
        
        # Create storage directory
        os.makedirs(storage_path, exist_ok=True)
        
        # Load existing memory
        self._load_memory()
    
    def start_session(self, user_id: str = None) -> str:
        """Start a new conversation session"""
        if user_id is None:
            user_id = f"user_{uuid.uuid4().hex[:8]}"
        
        session_id = f"session_{uuid.uuid4().hex[:12]}"
        self.current_session_id = session_id
        
        # Initialize conversation for this session
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        # Create user profile if doesn't exist
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = UserProfile(user_id=user_id)
        
        return session_id
    
    def add_message(self, role: str, content: str, metadata: Dict[str, Any] = None) -> str:
        """Add message to current session"""
        if self.current_session_id is None:
            self.start_session()
        
        entry = ConversationEntry(
            id=uuid.uuid4().hex,
            role=role,
            content=content,
            timestamp=datetime.now().isoformat(),
            metadata=metadata or {}
        )
        
        self.conversations[self.current_session_id].append(entry)
        self._save_conversations()
        return entry.id
    
    def get_conversation_history(self, session_id: str = None, limit: int = None) -> List[ConversationEntry]:
        """Get conversation history for a session"""
        if session_id is None:
            session_id = self.current_session_id
        
        if session_id not in self.conversations:
            return []
        
        history = self.conversations[session_id]
        if limit:
            return history[-limit:]
        return history
    
    def update_user_profile(self, user_id: str, updates: Dict[str, Any]):
        """Update user profile information"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = UserProfile(user_id=user_id)
        
        profile = self.user_profiles[user_id]
        
        # Update specific fields
        if 'name' in updates:
            profile.name = updates['name']
        if 'preferences' in updates:
            profile.preferences.update(updates['preferences'])
        if 'travel_history' in updates:
            profile.travel_history.extend(updates['travel_history'])
        if 'payment_info' in updates:
            profile.payment_info.update(updates['payment_info'])
        if 'emergency_contacts' in updates:
            profile.emergency_contacts.extend(updates['emergency_contacts'])
        
        profile.last_updated = datetime.now().isoformat()
        self._save_user_profiles()
    
    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get user profile by ID"""
        return self.user_profiles.get(user_id)
    
    def store_knowledge(self, key: str, value: Any, source: str = "user"):
        """Store global knowledge/facts"""
        self.global_knowledge[key] = {
            "value": value,
            "source": source,
            "timestamp": datetime.now().isoformat()
        }
        self._save_global_knowledge()
    
    def get_knowledge(self, key: str) -> Any:
        """Retrieve stored knowledge"""
        return self.global_knowledge.get(key, {}).get("value")
    
    def search_conversations(self, query: str, session_id: str = None) -> List[ConversationEntry]:
        """Search conversation history for specific content"""
        results = []
        sessions_to_search = [session_id] if session_id else self.conversations.keys()
        
        for sid in sessions_to_search:
            for entry in self.conversations.get(sid, []):
                if query.lower() in entry.content.lower():
                    results.append(entry)
        
        return results
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        total_messages = sum(len(conv) for conv in self.conversations.values())
        
        return {
            "total_sessions": len(self.conversations),
            "total_messages": total_messages,
            "total_users": len(self.user_profiles),
            "knowledge_entries": len(self.global_knowledge),
            "current_session": self.current_session_id,
            "storage_path": self.storage_path
        }
    
    def clear_session(self, session_id: str = None):
        """Clear specific session data"""
        if session_id is None:
            session_id = self.current_session_id
        
        if session_id in self.conversations:
            del self.conversations[session_id]
            self._save_conversations()
    
    def export_data(self, file_path: str):
        """Export all memory data to JSON file"""
        export_data = {
            "conversations": {
                sid: [asdict(entry) for entry in entries]
                for sid, entries in self.conversations.items()
            },
            "user_profiles": {
                uid: asdict(profile)
                for uid, profile in self.user_profiles.items()
            },
            "global_knowledge": self.global_knowledge,
            "export_timestamp": datetime.now().isoformat()
        }
        
        with open(file_path, 'w') as f:
            json.dump(export_data, f, indent=2)
    
    def _load_memory(self):
        """Load memory from storage"""
        # Load conversations
        conv_file = os.path.join(self.storage_path, "conversations.json")
        if os.path.exists(conv_file):
            try:
                with open(conv_file, 'r') as f:
                    data = json.load(f)
                    for sid, entries in data.items():
                        self.conversations[sid] = [
                            ConversationEntry(**entry) for entry in entries
                        ]
            except Exception as e:
                print(f"Error loading conversations: {e}")
        
        # Load user profiles
        profiles_file = os.path.join(self.storage_path, "user_profiles.json")
        if os.path.exists(profiles_file):
            try:
                with open(profiles_file, 'r') as f:
                    data = json.load(f)
                    for uid, profile_data in data.items():
                        self.user_profiles[uid] = UserProfile(**profile_data)
            except Exception as e:
                print(f"Error loading user profiles: {e}")
        
        # Load global knowledge
        knowledge_file = os.path.join(self.storage_path, "global_knowledge.json")
        if os.path.exists(knowledge_file):
            try:
                with open(knowledge_file, 'r') as f:
                    self.global_knowledge = json.load(f)
            except Exception as e:
                print(f"Error loading global knowledge: {e}")
    
    def _save_conversations(self):
        """Save conversations to storage"""
        conv_file = os.path.join(self.storage_path, "conversations.json")
        try:
            data = {
                sid: [asdict(entry) for entry in entries]
                for sid, entries in self.conversations.items()
            }
            with open(conv_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving conversations: {e}")
    
    def _save_user_profiles(self):
        """Save user profiles to storage"""
        profiles_file = os.path.join(self.storage_path, "user_profiles.json")
        try:
            data = {
                uid: asdict(profile)
                for uid, profile in self.user_profiles.items()
            }
            with open(profiles_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving user profiles: {e}")
    
    def _save_global_knowledge(self):
        """Save global knowledge to storage"""
        knowledge_file = os.path.join(self.storage_path, "global_knowledge.json")
        try:
            with open(knowledge_file, 'w') as f:
                json.dump(self.global_knowledge, f, indent=2)
        except Exception as e:
            print(f"Error saving global knowledge: {e}")

# Example usage
if __name__ == "__main__":
    # Test the memory bank
    memory = MemoryBank("test_memory")
    
    # Start session
    session_id = memory.start_session("test_user")
    print(f"Started session: {session_id}")
    
    # Add some messages
    memory.add_message("user", "Hello, I want to plan a trip to Tokyo")
    memory.add_message("assistant", "Great! I'd love to help you plan your Tokyo trip. What time of year are you thinking?")
    memory.add_message("user", "I prefer spring season, and I love sushi restaurants")
    
    # Update user profile
    memory.update_user_profile("test_user", {
        "name": "Alice",
        "preferences": {
            "season": "spring",
            "cuisine": "Japanese",
            "food_preference": "sushi"
        }
    })
    
    # Store some knowledge
    memory.store_knowledge("tokyo_best_sushi", "Tsukiji Market has the best sushi spots")
    
    # Get conversation history
    history = memory.get_conversation_history()
    print(f"\nConversation history ({len(history)} messages):")
    for entry in history:
        print(f"{entry.role}: {entry.content}")
    
    # Get memory stats
    stats = memory.get_memory_stats()
    print(f"\nMemory stats: {stats}")
    
    # Export data
    memory.export_data("memory_export.json")
    print("Memory exported to memory_export.json")