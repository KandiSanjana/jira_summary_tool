"""
Configuration management for the Jira Summary Tool.

This module handles loading and validating configuration from environment variables.
It provides a Config class that centralizes all application settings.
"""

import os
from typing import Optional


class Config:
    """Configuration class for the Jira Summary Tool.
    
    This class handles loading and validating all configuration settings from
    environment variables. It provides both required and optional settings with
    appropriate defaults.
    """
    
    def __init__(self) -> None:
        """Initialize configuration from environment variables.
        
        Raises:
            KeyError: If any required environment variable is missing.
        """
        # Required configurations
        self._load_required_configs()
        
        # Optional configurations with defaults
        self._load_optional_configs()
        
        # Derived configurations
        self._set_derived_configs()
    
    def _load_required_configs(self) -> None:
        """Load required configuration values from environment.
        
        Raises:
            KeyError: If any required environment variable is missing.
        """
        self.jira_server = os.environ["JIRA_SERVER"]
        self.jira_user = os.environ["JIRA_USER"]
        self.jira_api_token = os.environ["JIRA_API_TOKEN"]
        self.cohere_api_key = os.environ["COHERE_API_KEY"]
    
    def _load_optional_configs(self) -> None:
        """Load optional configuration values with defaults."""
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.mode = os.getenv("MODE", "development").lower()
        self.log_level = os.getenv("LOG_LEVEL", "DEBUG" if self.mode == "development" else "INFO")
    
    def _set_derived_configs(self) -> None:
        """Set derived configuration values based on other settings."""
        self.debug = self.mode == "development"
        self.output_dir = "/outputs"


def load_config() -> Config:
    """Load and validate configuration from environment variables.
    
    Returns:
        Config: A configured Config instance.
        
    Raises:
        KeyError: If any required environment variable is missing.
    """
    return Config()
