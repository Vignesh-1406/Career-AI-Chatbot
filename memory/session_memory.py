"""
Session memory management for Career Advisor Chatbot.

Maintains conversation history and session state across multiple turns.
Provides context preservation and memory optimization.
"""

from typing import List, Dict, Tuple
from datetime import datetime
from config import Config
from utils.logger import ChatbotLogger


class ConversationMessage:
    """
    Represents a single message in the conversation.
    
    Attributes:
        role: Either "user" or "assistant"
        content: The message text
        timestamp: When the message was created
        metadata: Optional additional information
    """
    
    def __init__(
        self,
        role: str,
        content: str,
        metadata: Dict = None
    ):
        """
        Initialize a conversation message.
        
        Args:
            role: "user" or "assistant"
            content: Message text
            metadata: Optional metadata dictionary
        """
        self.role = role
        self.content = content
        self.timestamp = datetime.now()
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict:
        """
        Convert message to dictionary format.
        
        Returns:
            Dictionary representation of the message.
        """
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }
    
    def get_formatted_text(self) -> str:
        """
        Get formatted text for display.
        
        Returns:
            Formatted message string.
        """
        return f"[{self.timestamp.strftime('%H:%M:%S')}] {self.role.upper()}: {self.content}"


class SessionMemory:
    """
    Manages conversation history and session state.
    
    Provides:
    - Multi-turn conversation support
    - Context preservation
    - Memory optimization (truncation of old messages)
    - Conversation statistics
    """
    
    def __init__(self):
        """Initialize session memory."""
        self.messages: List[ConversationMessage] = []
        self.session_start = datetime.now()
        self.logger = ChatbotLogger.get_logger(__name__)
    
    def add_user_message(self, content: str, metadata: Dict = None):
        """
        Add a user message to the conversation.
        
        Args:
            content: User's message text
            metadata: Optional metadata
        """
        message = ConversationMessage("user", content, metadata)
        self.messages.append(message)
        self.logger.debug(f"Added user message: {len(content)} characters")
    
    def add_assistant_message(self, content: str, metadata: Dict = None):
        """
        Add an assistant message to the conversation.
        
        Args:
            content: Assistant's response text
            metadata: Optional metadata (e.g., token counts, model info)
        """
        message = ConversationMessage("assistant", content, metadata)
        self.messages.append(message)
        self.logger.debug(f"Added assistant message: {len(content)} characters")
    
    def get_conversation_history(self) -> List[Dict]:
        """
        Get the complete conversation history in API format.
        
        Returns:
            List of message dictionaries with roles and content.
        """
        return [
            {"role": msg.role, "content": msg.content}
            for msg in self.messages
        ]
    
    def get_recent_messages(self, count: int = 5) -> List[ConversationMessage]:
        """
        Get the most recent messages from the conversation.
        
        Args:
            count: Number of recent messages to retrieve.
            
        Returns:
            List of recent ConversationMessage objects.
        """
        return self.messages[-count:] if self.messages else []
    
    def get_conversation_summary(self) -> str:
        """
        Generate a summary of the conversation so far.
        
        Returns:
            String summary of conversation topics and progress.
        """
        if not self.messages:
            return "No conversation yet."
        
        user_messages = [m for m in self.messages if m.role == "user"]
        assistant_messages = [m for m in self.messages if m.role == "assistant"]
        
        total_length = sum(len(m.content) for m in self.messages)
        avg_user_msg = (
            sum(len(m.content) for m in user_messages) / len(user_messages)
            if user_messages else 0
        )
        avg_assistant_msg = (
            sum(len(m.content) for m in assistant_messages) / len(assistant_messages)
            if assistant_messages else 0
        )
        
        return (
            f"Conversation Summary:\n"
            f"- User Messages: {len(user_messages)}\n"
            f"- Assistant Messages: {len(assistant_messages)}\n"
            f"- Total Characters: {total_length}\n"
            f"- Avg User Message: {avg_user_msg:.0f} chars\n"
            f"- Avg Assistant Message: {avg_assistant_msg:.0f} chars"
        )
    
    def optimize_memory(self):
        """
        Optimize session memory by removing old messages if limit exceeded.
        
        Keeps the most recent messages up to MAX_CONVERSATION_HISTORY.
        Preserves initial system context.
        """
        max_history = Config.MAX_CONVERSATION_HISTORY
        
        if len(self.messages) > max_history:
            removed = len(self.messages) - max_history
            self.messages = self.messages[-max_history:]
            self.logger.info(f"Optimized memory: removed {removed} old messages")
    
    def clear_history(self):
        """
        Clear all conversation history.
        
        Use with caution - this will reset the session state.
        """
        self.messages = []
        self.session_start = datetime.now()
        self.logger.info("Conversation history cleared")
    
    def get_session_stats(self) -> Dict:
        """
        Get statistics about the current session.
        
        Returns:
            Dictionary with session statistics.
        """
        user_messages = [m for m in self.messages if m.role == "user"]
        assistant_messages = [m for m in self.messages if m.role == "assistant"]
        
        session_duration = (datetime.now() - self.session_start).total_seconds()
        
        return {
            "total_messages": len(self.messages),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "total_characters": sum(len(m.content) for m in self.messages),
            "session_duration_seconds": session_duration,
            "session_start": self.session_start.isoformat()
        }
    
    def export_conversation(self) -> List[Dict]:
        """
        Export the entire conversation as a list of dictionaries.
        
        Useful for saving, analyzing, or sharing conversations.
        
        Returns:
            List of message dictionaries with all metadata.
        """
        return [msg.to_dict() for msg in self.messages]
    
    def display_conversation(self) -> str:
        """
        Generate a formatted display of the conversation.
        
        Returns:
            Formatted string representation of the conversation.
        """
        if not self.messages:
            return "Conversation is empty."
        
        formatted = []
        for msg in self.messages:
            formatted.append(msg.get_formatted_text())
        
        return "\n".join(formatted)
    
    def get_context_window(self, max_tokens: int = 4000) -> Tuple[List[Dict], int]:
        """
        Get conversation history limited by token window for API calls.
        
        This helps prevent exceeding API token limits by including
        only recent messages that fit within the token budget.
        
        Args:
            max_tokens: Maximum tokens allowed for the context.
            
        Returns:
            Tuple of (conversation_history, estimated_tokens)
        """
        # Rough estimation: 1 token ≈ 4 characters
        estimated_tokens = 0
        context = []
        
        # Include messages from most recent backwards
        for msg in reversed(self.messages):
            msg_tokens = len(msg.content) // 4 + 10  # Rough estimate
            
            if estimated_tokens + msg_tokens > max_tokens:
                break
            
            context.insert(0, msg.to_dict())
            estimated_tokens += msg_tokens
        
        return context, estimated_tokens
