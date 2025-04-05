# config.py
import os

class Config:
    def __init__(self):
        # Required configurations (raise error if not provided)
        self.jira_server = os.environ["JIRA_SERVER"]
        self.jira_user = os.environ["JIRA_USER"]
        self.jira_api_token = os.environ["JIRA_API_TOKEN"]
        self.openai_api_key = os.environ["OPENAI_API_KEY"]
        # Optional configurations with defaults
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.mode = os.getenv("MODE", "development").lower()
        # Determine debug mode and log level
        self.debug = self.mode == "development"
        self.log_level = os.getenv("LOG_LEVEL", "DEBUG" if self.debug else "INFO")
        # Output paths
        self.output_dir = os.getenv("REPORT_OUTPUT_DIR", "output")
        os.makedirs(self.output_dir, exist_ok=True)

def load_config():
    """Load configuration from environment and return a Config object."""
    return Config()
