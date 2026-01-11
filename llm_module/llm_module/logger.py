"""Simple structured logging."""

from datetime import datetime
from typing import Any


class Logger:
    """Simple logger for debugging and tracing."""
    
    def __init__(self, name: str = "LLM", enabled: bool = True):
        self.name = name
        self.enabled = enabled
    
    def _format_message(self, level: str, message: str) -> str:
        """Format a log message with timestamp and level."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        return f"[{timestamp}] {level:8} | {message}"
    
    def info(self, message: str):
        """Log an info message."""
        if self.enabled:
            print(self._format_message("ℹ️  INFO", message))
    
    def warning(self, message: str):
        """Log a warning message."""
        if self.enabled:
            print(self._format_message("⚠️  WARN", message))
    
    def error(self, message: str):
        """Log an error message."""
        if self.enabled:
            print(self._format_message("❌ ERROR", message))
    
    def debug(self, message: str):
        """Log a debug message."""
        if self.enabled:
            print(self._format_message("🔍 DEBUG", message))
    
    def success(self, message: str):
        """Log a success message."""
        if self.enabled:
            print(self._format_message("✅ OK", message))


def get_logger(name: str = "LLM", enabled: bool = True) -> Logger:
    """Get a logger instance."""
    return Logger(name, enabled)
